from django.forms import CharField
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

def validate_gtin(value):
    VALID_GTIN_LENGTHS = [8, 12, 13, 14]
    nums = [ int(s) for s in value if s.isdigit() ]
    if not ( len(nums) in VALID_GTIN_LENGTHS ):
        raise ValidationError(_("This is not a valid length for a GTIN. It must be 8, 12, 13 or 14 digits long."))
    if not ( validate_checkdigit(value) ):
        raise ValidationError(_("This doesn't seem to be a valid GTIN. The check-digit calculation returned an error."))

def validate_checkdigit(value):
    """
    Recalculates the checkdigit and compares it to the provided number. If they
    match, then it is "valid," and so True is returned. Otherwise false is returned.
    """
    value = [ int(s) for s in value if s.isdigit() ]
    provided_checkdigit = int(value.pop())

    odd_values = 0
    even_values = 0

    for i in value[::2]: # odd calc
        odd_values += int(i)

    for i in value[1::2]: # even calc
        even_values += int(i)

    # If length is even (8, 12, 14)
    if len(value)%2==0: # This gives an even number, but we've pop'd one off, so that's inverted.
        # GTIN-13, so odd numbers are x1, even x3
        total = odd_values + (even_values * 3)
    else:
        # GTIN-8, 12, 14, so odd numbers are x3, even x1
        total = (odd_values * 3) + even_values

    check_digit = 10 - (total % 10)
    if check_digit == 10:
        check_digit = 0

    if check_digit == provided_checkdigit:
        # Its good
        return True
    return False
