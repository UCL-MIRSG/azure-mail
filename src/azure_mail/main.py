"""Create an email to send with an Azure app."""

import atexit
import datetime
import os
import pathlib

import dateutil.parser
import exchangelib
import ics
import msal
import pytz

__all__ = [
    "create_email",
    "create_calendar_ics",
]


def _check_or_set_up_cache() -> msal.SerializableTokenCache:
    """
    Set up MSAL token cache and load existing token.

    Returns
    -------
        msal.SerializableTokenCache: Contains the access token if exists in cache.

    """
    cache = msal.SerializableTokenCache()
    path = pathlib.Path("my_cache.bin")
    if path.exists():
        with path.open() as f:
            cache.deserialize(f.read())
    atexit.register(
        lambda: path.open("w").write(cache.serialize())
        # Hint: The following optional line persists only when state changed
        if cache.has_state_changed
        else None
    )
    return cache


def _get_app_access_token() -> dict:
    """
    Acquire an access token for the Azure app through the MSAL library.

    Returns
    -------
        dict: Contains the access token within the dict.

    """
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
        message = f"Access token could not be acquired {result['error_description']}"
        raise RuntimeError(message)

    return result


def _setup_email_account(
    access_token: dict,
) -> exchangelib.Account:
    """
    Use access token to configure Exchange user account using OAuth2 authorisation.

    Args:
        access_token (dict): Contains the access token within the dict.

    Returns:
    -------
        exchangelib.Account: An exchangelib account object which contains the account
        address, access_type (delegate or impersonation) and configuration for
        exchangelib to connect to the account specified.

    """
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
) -> exchangelib.Message:
    """
    Create an email to send to a list of users as bcc.

    Args:
        recipients (list[str]): A list of strings containing email addresses.
        body (exchangelib.HTMLBody): body of the email.
        subject (str): Subject of the email.
        attachments (list[exchangelib.FileAttachment]): List of email attachments.


    Returns:
    -------
        exchangelib.Message: A message which contains subject, body, sender
        and recipients etc. To send the email, message.send() method can be used.

    """
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


def create_calendar_ics(  # noqa: PLR0913
    subject: str,
    description: str,
    date: str,
    start_hour: int,
    start_minute: int = 0,
    duration_hours: int = 1,
    duration_minutes: int = 0,
    timezone: str = "Europe/London",
) -> exchangelib.FileAttachment:
    """
    Create an ICS calendar file for attaching in an email.

    Args:
        subject (str): Subject line of the mail as title of the event.
        description (str): Description of the event.
        date (str): Date of the event.
        start_hour (int): Hour of the start of the event.
        start_minute (int, optional): Minute of the start of the event.
            Defaults to 0.
        duration_hours (int, optional): Duration of the event in hours.
        duration_minutes (int, optional): Duration of the event in minutes.
            Defaults to 0.
        timezone (str, optional): Timezone of the event. Defaults to "Europe/London".

    Returns:
    -------
        exchangelib.FileAttachment: ICS file attachment for the event.

    """
    date_time = dateutil.parser.parse(date)
    time_start = date_time + datetime.timedelta(
        hours=start_hour,
        minutes=start_hour,
    )
    time_end = date_time + datetime.timedelta(
        hours=start_hour + duration_hours,
        minutes=start_minute + duration_minutes,
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

    return exchangelib.FileAttachment(
        name=f"{subject}.ics",
        content=bytes(calendar.serialize(), "UTF-8"),
    )