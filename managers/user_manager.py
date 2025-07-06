from models import User
from utils.session import UserSession
import bcrypt
from db import get_db

class UserManager:
    def register(self, username: str, password: str):
        with get_db() as db:
            existing_user = db.query(User).filter_by(username=username).first()
            if existing_user:
                print("🚫 Username already taken.")
                return

            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = User(username=username, password_hash=hashed_pw.decode())
            db.add(user)
            db.commit()
            UserSession.login(user)
            print("✅ Registration successful and logged in.")

    def login(self, username: str, password: str):
        with get_db() as db:
            user = db.query(User).filter_by(username=username).first()
            if not user:
                print("❌ No such user.")
                return None

            if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
                UserSession.login(user)
                print(f"✅ Logged in as {username}")
                return user
            else:
                print("❌ Incorrect password.")
                return None

    def logout(self):
        UserSession.logout()
        print("👋 Logged out.")
