'''
Random Password Generator
'''
import random as rn
import string as st

# Get all the letters of English alphabet, digits and specail characters using String module
letter = st.ascii_letters
digits = st.digits
special = st.punctuation

# print(letter,digits,special)


def generate(lenght=15, numbers=True, special_chr=True):
    charachter = letter
    if numbers:
        charachter += digits

        charachter += special

    password = ""
    has_digit = False
    has_special = False
    meet_criteria = False

    while not meet_criteria or len(password) < lenght:
        new_chr = rn.choice(charachter)
        password += new_chr

# Check if the password contain digits, speacial characters or both
        if new_chr in digits:
            has_digit = True
        elif new_chr in special:
            has_special = True

# Check if the password has meat certain certeria set by the user
        meet_criteria = True
        if has_digit:
            meet_criteria = has_digit
        if has_special:
            meet_criteria = meet_criteria and has_special

    return password


if __name__ == "__main__":
    # Ask the user to set the criteria of password
    pwd_length = int(input("Enter the length of your password: "))
    dig = input("Do you want to add digits (y/n): ").lower() == "y"
    spec_chr = input(
        "Do you want to add special character (y/n): ").lower() == "y"

    print(generate(pwd_length, dig, spec_chr))
