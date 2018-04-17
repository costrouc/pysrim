"""Utility functions that are used to construct Target and Ion

"""

def check_input(input_type, condition, value):
    value = input_type(value)
    if not condition(value):
        raise ValueError('type of argument does not satisfy condition')
    return value

is_zero = lambda value: True if value == 0 else False
is_zero_or_one = lambda value: True if value in range(2) else False
is_zero_to_two = lambda value: True if value in range(3) else False
is_zero_to_five = lambda value: True if value in range(6) else False
is_one_to_seven = lambda value: True if value in range(1,8) else False
is_one_to_eight = lambda value: True if value in range(1,9) else False
is_srim_degrees = lambda value: True if 0.0 <= value < 90.0 else False
is_positive = lambda value: True if value >= 0.0 else False
is_greater_than_zero = lambda value: True if value > 0.0 else False
is_quoteless = lambda value: True if '"' not in value else False
