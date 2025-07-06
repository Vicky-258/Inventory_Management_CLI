from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from managers.user_manager import UserManager
from utils.session import UserSession

console = Console()
user_manager = UserManager()

auth_completer = WordCompleter(["login", "register", "exit"], ignore_case=True)

def auth_menu():
    while True:
        choice = prompt("🔐 Command (login/register/exit): ", completer=auth_completer).strip().lower()

        if choice == "login":
            username = input("👤 Username: ").strip()
            password = input("🔑 Password: ").strip()
            user = user_manager.login(username, password)
            if user:
                return

        elif choice == "register":
            username = input("👤 Choose Username: ").strip()
            password = input("🔑 Choose Password: ").strip()
            user_manager.register(username, password)
            if UserSession.get_current_user():
                return

        elif choice == "exit":
            console.print("👋 Bye! Stay safe out there.")
            exit()

        else:
            console.print("❌ Invalid command.")