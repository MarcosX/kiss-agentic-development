from typing import Dict
import re


class UserRegistration:
    def __init__(self):
        self._users: Dict[str, dict] = {}

    def register_user(self, email: str, name: str) -> dict:
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            raise ValueError("Invalid email format")
        # BUG: No check for existing email before insertion; duplicates overwrite
        user = {"email": email, "name": name, "id": len(self._users) + 1}
        self._users[email] = user
        return user