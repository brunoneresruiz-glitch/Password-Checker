#PasswordChecker 

import re
import math
import string

COMMON_PASSWORDS = {
    "0123456", "password", "123456789", "987654321",
    "12345","12345678", "0123456789", "qwerty", "abc123",
    "111111", "admin123", "letmein", "welcome", "monkey",
    "dragon", "master", "sunshine", "princess", "shadow",
    "superman", "password", "password1" "password123", "ilovefootball",
    "senha", "senha123", "ilovemydog", "michaeljackson"
    "ilovelasagna", "iloveitaly", "ilovecarbonara", "ilovedublin",
    "guinness123",
}

def calculate_entropy(password):
    alphabet_size = 0
    if re.search(r'[a-z]', password):
        alphabet_size += 26
    if re.search(r'[A-Z]', password):
        alphabet_size += 26
    if re.search(r'\d', password):
        alphabet_size += 10
    if re.search(r'[!@#$%^&*(),.?":;{}|<>_/-/[\+-]£~`¬]', password):
        alphabet_size += 32
    if alphabet_size == 0:
        return 0 
    
    return len(password) * math.log2(alphabet_size)


def check_password(password):
    is_common = password.lower() in COMMON_PASSWORDS

    length = len(password)
    length_ok = length >= 8

    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_lowercase = bool(re.search(r'[a-z]', password))

    has_number = bool(re.search(r'\d', password))

    has_special = bool(re.search(r'[!@#$%^&*(),.?":;{}|<>_/-/[\+-]£~`¬]', password))

    entropy = calculate_entropy(password)

    score = 0

    if not is_common: score += 20
    if length >= 8:   score += 10
    if length >= 12:  score += 10
    if length >= 16:  score += 10
    if has_uppercase: score += 10
    if has_lowercase: score += 10
    if has_number:    score += 10
    if has_special:   score += 10 

    if entropy >= 40: score += 5
    if entropy >= 60: score += 5
    if entropy >= 80: score += 5

    score = max(0, min(100, score))

    if is_common:
        score = 0

    if score == 0 or is_common:
        level = " :-( Very Weak Password, Sorry"
    elif score < 40:
        level = " :-( Weak Password, Sorry)"
    elif score < 60:
        level = " :-) Medium Password"
    elif score < 80:
        level = ";-) Good Password"
    else:
        level = " :D Strong Password, well done! "

    suggestions = []

    if is_common:
        suggestions.append(" Be careful, and protect your privacy. This password is on the world's most used list - Please change it!")
    if not length_ok:
        suggestions.append("Use at least 8 characters")
    if not has_uppercase:
        suggestions.append("Please Add uppercase letters")
    if not has_lowercase:
        suggestions.append("Please Add lowercase letters ")
    if not has_number:
        suggestions.append("Please Add numbers")
    if not has_special:
        suggestions.append("Please Add special characters (eg. @.$,~,#...)")
    if length < 12 and length_ok:
        suggestions.append ("Try using 12 or more characters for greater security")
    if not suggestions:
        suggestions.appenD("Excellent!")

    return {
        "password":      password,
        "score":         score,
        "level":         level,
        "is_common":     is_common,
        "length":        length,
        "has_uppercase": has_uppercase,
        "has_lowercase": has_lowercase,
        "has_number":    has_number,
        "has_special":   has_special,
        "entropy":       round(entropy, 2),
        "suggestions":   suggestions,
    }

def display_result(result):
    print("\n" + "=" * 55)
    print("PASSWORD STRENGTH CHECKER")
    print("=" * 55)
    print(f" Password analysed : {"*"* len(result["password"])}")
    print(f" Length            : {result["length"]} characters")
    print(f" Entropy           : {result["entropy"]} bits")
    print(f" Score             : {result["score"]}/100")
    print(f" Strength          : {result["level"]}")
    print()

    print("CRITERIA:")
    print(f"{"+" if not result["is_common"] else "-"} Not a common password")
    print(f"{"+" if result ["length"] >= 8  else "-"} Minimum length (8+)") 
    print(f"{"+" if result ["has_uppercase"] else "-"} Uppercase letters")
    print(f"{"+" if result ["has_lowercase"] else "-"} Lowercase letters")
    print(f"{"+" if result ["has_special"]   else "-"} Special characters")
    print(f"{"+" if result ["has_number"]    else "-"} Numbers")
    print(f"{"+" if result ["entropy"] >= 60 else "-"} Strong entropy (60+ bits)")
    print()

    print("SUGGESTIONS")
    for suggestion in result ["suggestions"]:
        print(f"{suggestion}")
    print("=" * 55 + "\n")

if __name__ == "__main__":
    print("\n Password Strength Checker - Cybersecurity Tool")
    print("  Type 'quit' to exit\n")
#infinite loop until user types quit.
    while True: 
        password = input ("Enter a password to analyse:")
        if password.lower() == "quit":
            print("\n Exiting. Stay secure! \n")
            break  #stops the while loop.
        if not  password:
            print(" Please enter a password.\n")
            continue

        result = check_password(password)
        display_result(result)
