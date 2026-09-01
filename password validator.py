"""
Password strength validator.

Checks a password against several security rules and reports
whether it is strong, medium, or weak, along with the specific
reasons why it does or doesn't meet each requirement.

Usage:
    python password_validator.py
"""

import re
import getpass


# ----------------------------------------------------------------------
# 1. VALIDATION RULES
# ----------------------------------------------------------------------
MIN_LENGTH = 8
RECOMMENDED_LENGTH = 12

COMMON_PASSWORDS = {
    "123456", "password", "12345678", "qwerty", "123456789",
    "12345", "1234", "111111", "1234567", "dragon",
    "123123", "abc123", "password1", "iloveyou", "admin",
}


def check_length(password: str) -> tuple[bool, str]:
    """Checks whether the password meets the minimum length requirement."""
    if len(password) >= RECOMMENDED_LENGTH:
        return True, f"Length is {len(password)} characters (recommended: {RECOMMENDED_LENGTH}+)"
    elif len(password) >= MIN_LENGTH:
        return True, f"Length is {len(password)} characters (meets minimum of {MIN_LENGTH}, but {RECOMMENDED_LENGTH}+ is better)"
    else:
        return False, f"Too short: {len(password)} characters (minimum required: {MIN_LENGTH})"


def check_uppercase(password: str) -> tuple[bool, str]:
    """Checks whether the password contains at least one uppercase letter."""
    if re.search(r"[A-Z]", password):
        return True, "Contains uppercase letters"
    return False, "Missing uppercase letters (A-Z)"


def check_lowercase(password: str) -> tuple[bool, str]:
    """Checks whether the password contains at least one lowercase letter."""
    if re.search(r"[a-z]", password):
        return True, "Contains lowercase letters"
    return False, "Missing lowercase letters (a-z)"


def check_digits(password: str) -> tuple[bool, str]:
    """Checks whether the password contains at least one digit."""
    if re.search(r"[0-9]", password):
        return True, "Contains numbers"
    return False, "Missing numbers (0-9)"


def check_special_characters(password: str) -> tuple[bool, str]:
    """Checks whether the password contains at least one special character."""
    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        return True, "Contains special characters"
    return False, "Missing special characters (e.g. ! @ # $ % & *)"


def check_common_password(password: str) -> tuple[bool, str]:
    """Checks whether the password is one of the most commonly used weak passwords."""
    if password.lower() in COMMON_PASSWORDS:
        return False, "This is a very common password and is easily guessed"
    return True, "Not found in the common password list"


def check_repeated_characters(password: str) -> tuple[bool, str]:
    """Checks whether the password contains long sequences of the same repeated character."""
    if re.search(r"(.)\1{2,}", password):
        return False, "Contains 3 or more repeated characters in a row (e.g. 'aaa', '111')"
    return True, "No excessive character repetition"


# ----------------------------------------------------------------------
# 2. MAIN EVALUATION FUNCTION
# ----------------------------------------------------------------------
def evaluate_password(password: str) -> dict:
    """
    Runs all validation checks on a password and returns a summary
    with the overall strength level and the details of each check.
    """
    checks = {
        "length": check_length(password),
        "uppercase": check_uppercase(password),
        "lowercase": check_lowercase(password),
        "digits": check_digits(password),
        "special_characters": check_special_characters(password),
        "common_password": check_common_password(password),
        "repeated_characters": check_repeated_characters(password),
    }

    passed_checks = sum(1 for passed, _ in checks.values() if passed)
    total_checks = len(checks)

    # Determine overall strength level
    if not checks["common_password"][0]:
        strength = "WEAK"
    elif passed_checks == total_checks and len(password) >= RECOMMENDED_LENGTH:
        strength = "STRONG"
    elif passed_checks >= total_checks - 1:
        strength = "MEDIUM"
    else:
        strength = "WEAK"

    return {
        "strength": strength,
        "score": f"{passed_checks}/{total_checks}",
        "checks": checks,
    }


# ----------------------------------------------------------------------
# 3. DISPLAY RESULTS
# ----------------------------------------------------------------------
def print_report(password: str):
    """Prints a readable report of the password evaluation."""
    result = evaluate_password(password)

    print("\n--- PASSWORD STRENGTH REPORT ---")
    print(f"Overall strength: {result['strength']}")
    print(f"Checks passed: {result['score']}\n")

    for check_name, (passed, message) in result["checks"].items():
        status = "OK " if passed else "FAIL"
        print(f"[{status}] {check_name.replace('_', ' ').title()}: {message}")

    print()


# ----------------------------------------------------------------------
# 4. MAIN PROGRAM (interactive menu)
# ----------------------------------------------------------------------
def main():
    while True:
        print("--- PASSWORD VALIDATOR ---")
        print("1. Check a password")
        print("2. Exit")

        option = input("Choose an option: ").strip()

        if option == "1":
            # getpass hides the input while typing, for privacy
            password = getpass.getpass("Enter the password to check: ")
            if not password:
                print("Password cannot be empty.\n")
                continue
            print_report(password)

        elif option == "2":
            print("Goodbye!")
            break

        else:
            print("Invalid option, please try again.\n")


if __name__ == "__main__":
    main()