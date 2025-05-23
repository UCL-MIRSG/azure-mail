"""Get the app access token for Azure Mail API."""

from azure_mail.main import _get_app_access_token

if __name__ == "__main__":
    token = _get_app_access_token()  # print(json.dumps(token))
