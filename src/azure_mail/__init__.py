"""azure_mail package."""

from ._version import __version__  # noqa: F401
from .main import (
    create_email,
    create_calendar_ics,
)