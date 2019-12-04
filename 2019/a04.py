"""
You arrive at the Venus fuel depot only to discover it's protected by a
password. The Elves had written the password on a sticky note, but someone
threw it out.

However, they do remember a few key facts about the password:

    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever
    increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet
these criteria?
"""

total = 0
def passes_test(number): 
    number_string = str(number) 
    if not any(f'{digit}{digit}' in number_string for digit in set(number_string)): 
        return False 
    digit = int(number_string[0]) 
    for str_digit in number_string: 
        if int(str_digit) < digit: 
            return False 
        digit = int(str_digit) 
    return True 

for number in range(start, end): 
   if passes_test(number): 
       total += 1 


"""
An Elf just remembered one more important detail: the two adjacent matching
digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the
following are now true:

    112233 meets these criteria because the digits never decrease and all
    repeated digits are exactly two digits long.
    123444 no longer meets the criteria (the repeated 44 is part of a larger
    group of 444).
    111122 meets the criteria (even though 1 is repeated more than twice, it
    still contains a double 22).

How many different passwords within the range given in your puzzle input meet
all of the criteria?
"""

def passes_test(number): 
    number_string = str(number) 
    if not any(len(list(re.finditer(f'(?=({digit}{digit}))', number_string))) == 1 for digit in set(number_string)): 
        return False 
    digit = int(number_string[0]) 
    for str_digit in number_string: 
        if int(str_digit) < digit: 
            return False 
        digit = int(str_digit) 
    return True 

