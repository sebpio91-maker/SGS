"""Legt einen Benutzer an, der sich in der App einloggen kann.

Es gibt (noch) keine öffentliche Registrierung – Benutzer werden über
dieses Skript angelegt. Aufruf:

    python -m app.create_user --email a@b.de --name "Max Muster" --password geheim
"""

import argparse

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User


def create_user(email: str, full_name: str, password: str) -> None:
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).one_or_none()
        if existing is not None:
            print(f"Benutzer mit E-Mail '{email}' existiert bereits.")
            return

        user = User(
            email=email,
            full_name=full_name,
            hashed_password=hash_password(password),
        )
        db.add(user)
        db.commit()
        print(f"Benutzer '{email}' wurde angelegt.")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--email", required=True)
    parser.add_argument("--name", required=True, dest="full_name")
    parser.add_argument("--password", required=True)
    args = parser.parse_args()

    create_user(args.email, args.full_name, args.password)
