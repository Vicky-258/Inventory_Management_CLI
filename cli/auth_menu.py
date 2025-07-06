# from managers.user_manager import UserManager
# from rich.console import Console
# from utils.session import UserSession
# import questionary
#
# console = Console()
# user_manager = UserManager()
#
#
# def auth_menu():
#     while True:
#         choice = questionary.select(
#             "🔐 Welcome to Inventory Manager",
#             choices=["Login", "Register", "Exit"]
#         ).ask()
#
#         if choice == "Login":
#             username = input("👤 Username: ").strip()
#             password = input("🔑 Password: ").strip()
#             user = user_manager.login(username, password)
#             if user:
#                 return
#
#         elif choice == "Register":
#             username = input("👤 Choose Username: ").strip()
#             password = input("🔑 Choose Password: ").strip()
#             user_manager.register(username, password)
#             if UserSession.get_current_user():
#                 return
#
#         elif choice == "Exit":
#             console.print("👋 Bye! Stay safe out there.")
#             exit()
#
#
#
#

from managers.user_manager import UserManager
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from utils.session import UserSession
import questionary
import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

console = Console()
user_manager = UserManager()

def auth_menu():
    console.clear()
    console.print(Panel.fit("🔐 [bold magenta]Welcome to Inventory Manager[/]", style="bold blue"), justify="center")

    while True:
        choice = questionary.select(
            "📋 Choose an option:",
            choices=["Login", "Register", "Exit"]
        ).ask()

        if choice == "Login":
            username = Prompt.ask("👤 [bold]Username[/]").strip()
            password = Prompt.ask("🔑 [bold]Password[/]", password=True).strip()

            user = user_manager.login(username, password)
            if user:
                clear_screen()
                console.print(f"\n✅ [green]Logged in as [bold]{username}[/]\n")
                return
            else:
                console.print("❌ [red]Invalid credentials. Please try again.\n")

        elif choice == "Register":
            username = Prompt.ask("👤 [bold]Choose Username[/]").strip()
            password = Prompt.ask("🔑 [bold]Choose Password[/]").strip()

            user_manager.register(username, password)
            if UserSession.get_current_user():
                clear_screen()
                console.print(f"\n✅ [green]Registered and logged in as [bold]{username}[/]\n")
                return

        elif choice == "Exit":
            console.print("\n👋 [cyan]Bye! Stay safe out there.\n")
            exit()
