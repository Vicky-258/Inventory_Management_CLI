import time
import os
from db import Base, engine
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from cli.auth_menu import auth_menu
from cli.InventoryCLI import InventoryCLI

console = Console()

def print_splash():
    os.system("cls" if os.name == "nt" else "clear")

    splash_lines = [
        "[bold cyan]Initializing modules...[/bold cyan]",
        "[bold cyan]Connecting to inventory database...[/bold cyan]",
        "[bold cyan]Authenticating CLI interface...[/bold cyan]",
        "[bold green]✅ System ready. Launching Inventory Manager.[/bold green]",
    ]

    for line in splash_lines:
        console.print(line)
        time.sleep(0.6)

    time.sleep(1)
    os.system("cls" if os.name == "nt" else "clear")

def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(engine)

def main():
    print_splash()
    init_db()
    auth_menu()
    InventoryCLI().run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n👋 Exiting gracefully. Take care, terminal warrior!")
        exit()
