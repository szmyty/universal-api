from zoneinfo import available_timezones


def is_valid_iana_timezone(timezone: str) -> bool:
    """Check if the given timezone is a valid IANA timezone."""
    return timezone in available_timezones()
