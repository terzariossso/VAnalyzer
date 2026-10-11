import subprocess
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
dashboard_path = os.path.join(current_dir, "dashboard.py")

command = f'start cmd.exe /k "python {dashboard_path}"'

subprocess.run(command, shell=True)