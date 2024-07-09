"""Create an email to send with an Azure app
"""
import atexit
import os

import dateutil.parser
import datetime
import msal
import pytz
import exchangelib
import ics

__all__ = [
    "create_email",
    "create_calendar_ics",
]

def _check_or_set_up_cache() -> msal.SerializableTokenCache:
    """Set up MSAL token cache and load existing token"""
    cache = msal.SerializableTokenCache()
    if os.path.exists("my_cache.bin"):
        cache.deserialize(open("my_cache.bin").read())
    atexit.register(
        lambda: open("my_cache.bin", "w").write(cache.serialize())
        # Hint: The following optional line persists only when state changed
        if cache.has_state_changed
        else None
    )
    return cache


def _get_app_access_token() -> dict:
    """Acquire an access token for the Azure app"""
    authority = "https://login.microsoftonline.com/" + os.environ["TENANT_ID"]
    global_token_cache = _check_or_set_up_cache()
    app = msal.ClientApplication(
        os.environ["CLIENT_ID"],
        client_credential=os.environ["CLIENT_SECRET"],
        authority=authority,
        token_cache=global_token_cache,
    )

    accounts = app.get_accounts(username=os.environ["ACCOUNT"])

    if accounts:
        result = app.acquire_token_silent([os.environ["SCOPE"]], account=accounts[0])

    else:
        result = app.acquire_token_by_username_password(
            os.environ["ACCOUNT"], os.environ["USER_PASSWORD"], [os.environ["SCOPE"]]
        )

    if "access_token" not in result:
        raise RuntimeError(
            "Access token could not be acquired", result["error_description"]
        )

    return result


def _setup_email_account(
        access_token: dict,
    ) -> exchangelib.Account:
    """Use access token to configure Exchange server user account."""
    creds = exchangelib.OAuth2AuthorizationCodeCredentials(access_token=access_token)
    conf = exchangelib.Configuration(
        server=os.environ["SERVER"], auth_type=exchangelib.OAUTH2, credentials=creds
    )

    return exchangelib.Account(
        primary_smtp_address=os.environ["ACCOUNT"],
        access_type=exchangelib.DELEGATE,
        config=conf,
        autodiscover=False,
    )


def create_email(
        recipients: list[str],
        body: exchangelib.HTMLBody,
        subject: str,
        attachments: list[exchangelib.FileAttachment],
    ):
    """Create an email to send to a list of users as bcc"""
    access_token = _get_app_access_token()
    account = _setup_email_account(
        access_token=access_token,
    )

    message = exchangelib.Message(
        account=account,
        folder=account.drafts,
        author=os.environ["AUTHOR"],
        subject=subject,
        body=body,
        to_recipients=[exchangelib.Mailbox(email_address=os.environ["AUTHOR"])],
        bcc_recipients=recipients,
    )

    message.attach(
        attachments=attachments,
    )

    return message


def create_calendar_ics(
        subject: str,
        description: str,
        date: str,
        start_hour: int,
        start_minute: int = 0,
        duration_hours: int = 1,
        duration_minutes: int = 0,
        timezone: str = "Europe/London",
    ) -> exchangelib.FileAttachment:
    """Create an ICS calendar file for attaching in an email
    """
    date_time = dateutil.parser.parse(date)
    time_start = date_time + datetime.timedelta(
        hours=start_hour,
        minutes=start_hour,
    )
    time_end = date_time + datetime.timedelta(
        hours=start_hour+duration_hours,
        minutes=start_minute+duration_minutes,
    )

    tz = pytz.timezone(timezone)
    time_start = tz.localize(time_start)
    time_end = tz.localize(time_end)

    event = ics.Event()
    event.name = subject
    event.description = description
    event.begin = time_start
    event.end = time_end

    calendar = ics.Calendar()
    calendar.events.add(event)

    attachment = exchangelib.FileAttachment(
        name=f"{subject}.ics",
        content=bytes(calendar.serialize(), "UTF-8"),
    )

    return attachment
