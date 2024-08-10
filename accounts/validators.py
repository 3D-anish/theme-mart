import re
from django.core.exceptions import ValidationError

def username_validator(username):
    """
    Validator for username field: allows only small letters, numbers, and underscores,dash and dot.
    Requires a minimum length of 3 characters.
    """
    if len(username) < 3:
        raise ValidationError(
            'Username must be at least 3 characters long.',
            code='invalid_username_length'
        )
    
    pattern = re.compile(r'^[a-z][a-z0-9_\-\.]*[a-z0-9]$')
    if not pattern.match(username):
        raise ValidationError(
            'Username can contain only a-z, 0-9 and underscore , dot , dash ',
            code='invalid_username_pattern'
        )

class NumberValidator:
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                "The password must contain at least 1 digit, 0-9.",
                code='password_no_number',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 digit, 0-9."
        

class UppercaseValidator:
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                "The password must contain at least 1 uppercase letter, A-Z.",
                code='password_no_upper',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 uppercase letter, A-Z."

class LowercaseValidator:
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                "The password must contain at least 1 lowercase letter, a-z.",
                code='password_no_lower',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 lowercase letter, a-z."

class SymbolValidator:
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                "The password must contain at least 1 symbol: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?",
                code='password_no_symbol',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 symbol: " + "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"