"""
Encryption and decryption program using Fernet
(symmetric cryptography from the 'cryptography' library).

Required installation:
    pip install cryptography

Usage:
    python fernet_encryptor.py
"""

from cryptography.fernet import Fernet, InvalidToken
import os


# ----------------------------------------------------------------------
# 1. GENERATE AND SAVE A KEY
# ----------------------------------------------------------------------
def generate_key(key_path="key.key"):
    """
    Generates a new Fernet key and saves it to a file.
    This key is required both to encrypt AND to decrypt,
    so it must be stored somewhere safe.
    """
    key = Fernet.generate_key()
    with open(key_path, "wb") as key_file:
        key_file.write(key)
    print(f"Key generated and saved to '{key_path}'")
    return key


def load_key(key_path="key.key"):
    """Loads an existing key from a file."""
    with open(key_path, "rb") as key_file:
        return key_file.read()


# ----------------------------------------------------------------------
# 2. ENCRYPT AND DECRYPT TEXT
# ----------------------------------------------------------------------
def encrypt_text(text: str, key: bytes) -> bytes:
    """Encrypts a text string and returns the result as bytes."""
    f = Fernet(key)
    encrypted_text = f.encrypt(text.encode("utf-8"))
    return encrypted_text


def decrypt_text(encrypted_text: bytes, key: bytes) -> str:
    """Decrypts previously encrypted bytes and returns the original text."""
    f = Fernet(key)
    original_text = f.decrypt(encrypted_text)
    return original_text.decode("utf-8")


# ----------------------------------------------------------------------
# 3. ENCRYPT AND DECRYPT FILES (bonus)
# ----------------------------------------------------------------------
def encrypt_file(input_path: str, output_path: str, key: bytes):
    """Reads a file, encrypts it, and saves the result to another file."""
    f = Fernet(key)
    with open(input_path, "rb") as file:
        data = file.read()
    encrypted_data = f.encrypt(data)
    with open(output_path, "wb") as file:
        file.write(encrypted_data)
    print(f"File '{input_path}' encrypted as '{output_path}'")


def decrypt_file(input_path: str, output_path: str, key: bytes):
    """Reads an encrypted file, decrypts it, and saves the result."""
    f = Fernet(key)
    with open(input_path, "rb") as file:
        encrypted_data = file.read()
    original_data = f.decrypt(encrypted_data)
    with open(output_path, "wb") as file:
        file.write(original_data)
    print(f"File '{input_path}' decrypted as '{output_path}'")


# ----------------------------------------------------------------------
# 4. MAIN PROGRAM (interactive menu)
# ----------------------------------------------------------------------
def main():
    key_path = "key.key"

    # If a key doesn't exist yet, generate one
    if not os.path.exists(key_path):
        key = generate_key(key_path)
    else:
        key = load_key(key_path)
        print(f"Using existing key from '{key_path}'")

    while True:
        print("\n--- MENU ---")
        print("1. Encrypt text")
        print("2. Decrypt text")
        print("3. Encrypt file")
        print("4. Decrypt file")
        print("5. Exit")

        option = input("Choose an option: ").strip()

        if option == "1":
            text = input("Enter the text to encrypt: ")
            result = encrypt_text(text, key)
            print(f"\nEncrypted text:\n{result.decode('utf-8')}")

        elif option == "2":
            encrypted_text = input("Paste the encrypted text: ").strip()
            try:
                result = decrypt_text(encrypted_text.encode("utf-8"), key)
                print(f"\nDecrypted text:\n{result}")
            except InvalidToken:
                print("Error: the text is invalid or the key doesn't match.")

        elif option == "3":
            input_path = input("Path of the file to encrypt: ").strip()
            output_path = input("Output file name (e.g. output.enc): ").strip()
            if os.path.exists(input_path):
                encrypt_file(input_path, output_path, key)
            else:
                print("That file doesn't exist.")

        elif option == "4":
            input_path = input("Path of the encrypted file: ").strip()
            output_path = input("Output file name: ").strip()
            if os.path.exists(input_path):
                try:
                    decrypt_file(input_path, output_path, key)
                except InvalidToken:
                    print("Error: the file is invalid or the key doesn't match.")
            else:
                print("That file doesn't exist.")

        elif option == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()