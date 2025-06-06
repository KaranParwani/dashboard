import base64
import os

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class PasswordProcessor:

    @staticmethod
    # Static method because it operates solely on the parameter provided to them
    def encrypt_password(
        password: str, salt: bytes = None, iterations: int = 100000
    ) -> str:
        """Encrypts a password using PBKDF2."""
        if salt is None:
            salt = os.urandom(16)  # Generate a random salt if not provided

        kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
            backend=default_backend(),
        )

        # Generate the derived key (password hash)
        hashed_password = base64.urlsafe_b64encode(kdf.derive(password.encode()))

        # Return salt and hashed password as a combined string (for storage)
        return f"{base64.urlsafe_b64encode(salt).decode()}${hashed_password.decode()}"

    @staticmethod
    # Static method because it operates solely on the parameter provided to them
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verifies a password against a hashed password."""
        try:
            salt, stored_hash = hashed_password.split("$")
            salt = base64.urlsafe_b64decode(salt)
            stored_hash = base64.urlsafe_b64decode(stored_hash)

            kdf = PBKDF2HMAC(
                algorithm=SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend(),
            )

            kdf.verify(
                password.encode(), stored_hash
            )  # Raises InvalidKey if mismatched
            return True
        except InvalidKey:
            return False
        except Exception as e:
            print(f"Verification error: {e}")
            return False
