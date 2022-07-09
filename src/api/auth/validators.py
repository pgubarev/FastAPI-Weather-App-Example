import re


_user_regex = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
    re.IGNORECASE,
)
_domain_regex = re.compile(
    # max length for domain name labels is 63 characters per RFC 1034
    r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z',
    re.IGNORECASE,
)

_invalid_email_error_message = 'Invalid email address'


def email_validator(email: str) -> str:
    if not email or '@' not in email:
        raise ValueError(_invalid_email_error_message)

    user_part, domain_part = email.rsplit('@', 1)
    if not (_user_regex.match(user_part) and _domain_regex.match(domain_part)):
        raise ValueError(_invalid_email_error_message)

    return email.lower()


def greater_than_zero_validator(value: int) -> int:
    if value <= 0:
        raise ValueError('value must be greater than 0')
    return value
