import re
from django.core.exceptions import ValidationError

def account_number_validator(account_number):

    pattern = re.compile(r'^\d{9,18}$')
    if not pattern.match(account_number):
        raise ValidationError(
            'Invalid Account Number',
            code='invalid_account_number_pattern'
        )

def account_ifsc_code_validator(ifsc_code):
    
    pattern = re.compile(r'^[A-Z]{4}0[A-Z0-9]{6}$')
    if not pattern.match(ifsc_code):
        raise ValidationError(
            'Invalid IFSC Code',
            code='invalid_ifsc_code_pattern'
        )
        
def aadhar_card_number_validator(aadhar_card_number):
    
    pattern = re.compile(r'^[2-9]{1}[0-9]{11}$')
    if not pattern.match(aadhar_card_number):
        raise ValidationError(
            'Invalid Aadhar Card Number',
            code='invalid_aadhar_card_number_pattern'
        )