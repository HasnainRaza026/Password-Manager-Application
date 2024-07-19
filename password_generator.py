import random as rn
import string as st


def generate(length=21, numbers=True, special_chr=True):
    characters = st.ascii_letters
    if numbers:
        characters += st.digits
    if special_chr:
        characters += st.punctuation

    password = ""
    has_digit = False
    has_special = False
    meet_criteria = False

    while not meet_criteria or len(password) < length:
        new_chr = rn.choice(characters)
        while new_chr in ('\\', "'", '"'):
            new_chr = rn.choice(characters)
        password += new_chr

        if new_chr in st.digits:
            has_digit = True
        elif new_chr in st.punctuation:
            has_special = True

        meet_criteria = True
        if numbers:
            meet_criteria = meet_criteria and has_digit
        if special_chr:
            meet_criteria = meet_criteria and has_special

    return password


if __name__ == "__main__":
    pwd_length = int(input("Enter the length of your password: "))
    dig = input("Do you want to add digits (y/n): ").lower() == "y"
    spec_chr = input("Do you want to add special character (y/n): ").lower() == "y"

    print(generate(pwd_length, dig, spec_chr))
