from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from menu import DiagnosticMenu
from registry import system_commands, session_log
import os
import signal
import time
import sys
import subprocess

console = Console()

art1 = r""" 
 _    _____                __                     
| |  / /   |  ____  ____ _/ /_  ______  ___  _____
| | / / /| | / __ \/ __ `/ / / / /_  / / _ \/ ___/
| |/ / ___ |/ / / / /_/ / / /_/ / / /_/  __/ /    
|___/_/  |_/_/ /_/\__,_/_/\__, / /___/\___/_/     
                         /____/                                                     
"""

art2 = "VAnalyzer v1.0 | Core System Diagnostic Utility | Last Update: 30/09/2026\n"


console.print(art1, style="bold green", highlight=False)
console.print(art2, style="italic green")

menu = DiagnosticMenu()
test_options_text = menu.show_test_options()
menu_panel = Panel(test_options_text, title="[bold white]Active Modules[/bold white]", border_style="green", expand=False)
console.print(menu_panel)

command_options_text = menu.show_command_options()
command_panel = Panel(command_options_text, title="[bold white]System Commands[/bold white]", border_style="green", expand=False)
console.print(command_panel)

# Create a active prompt that will await for the user's preference and after that if will take from dict the name of the test and run it
while True:
    user_choice = Prompt.ask("\n[green]Your turn, buddy[/green]")
    if user_choice in menu.available_test_options:
        test_name = menu.available_test_options[user_choice]
        
        console.print()
        console.print(f"[bold green][+] Tests may take some time[/bold green]")
        console.print(f"[bold green][+] Initiating module: {test_name}...[/bold green]")
        console.print() 
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.join(current_dir, "tests", f"{test_name}.py")
        result = subprocess.run(f'python "{test_path}"', shell=True, capture_output=True, text=True)
        
        output = result.stdout.strip()
        console.print(f"{result.stdout.strip()}", highlight=False)
        
        session_log.append(output)
        
        console.print()

    elif user_choice in system_commands:
        if user_choice in ['/savereport', '/sendreport']:
            msg = system_commands[user_choice][1](session_log)
            console.print(f"[bold green]{msg}[/bold green]")
        else:
            system_commands[user_choice][1]()

    else:
        console.print("[bold red][!] Invalid input. Choose the number of test or print a command[/bold red]")