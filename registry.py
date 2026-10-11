import os
import sys
import time
import datetime
import subprocess
import requests
import configparser

def cmd_exit():
    os.system('title Thanks for using, see you later!')
    time.sleep(0.5)
    os.system('taskkill /f /fi "WINDOWTITLE eq Thanks for using, see you later!"')

def cmd_clear():
    os.system('cls')

def cmd_refresh():
    os.system('cls')
    subprocess.call([sys.executable] + sys.argv)
    sys.exit()

# Distinct function

session_log = []
last_saved_report_path = None

def cmd_save_report(log_data):
    global last_saved_report_path
    
    if not log_data:
        return "[!] Session is empty. Run some modules first."

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"VAnalyzer_Report_{timestamp}.txt"
    
    temp_dir = os.environ.get('TEMP')
    report_path = os.path.join(temp_dir, filename)

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("=== VAnalyzer System Report ===\n")
        file.write(f"Generated: {timestamp}\n\n")
        file.write("\n\n".join(log_data))
        
    last_saved_report_path = report_path
    return f"[+] Report successfully saved to TEMP: {report_path}"


### Under the debug: 

def cmd_send_report(log_data):
    global last_saved_report_path
    
    if not last_saved_report_path or not os.path.exists(last_saved_report_path):
        return "[!] Error: No saved report found. Please run /savereport first."

    temp_dir = os.environ.get('TEMP')
    config_path = os.path.join(temp_dir, "vanalyzer_config.ini")
    config = configparser.ConfigParser()
    print(f"[!] NOTE: If you want to change these credentials later, simply edit or delete this file:")
    print(f"{config_path}\n")

    if not os.path.exists(config_path):
        print("\n[i] Telegram Setup: Config not found.")
        bot_token = input("Enter your Telegram BOT_TOKEN: ").strip()
        chat_id = input("Enter your Telegram CHAT_ID: ").strip()
        
        config["Telegram"] = {
            "BOT_TOKEN": bot_token,
            "CHAT_ID": chat_id
        }
        
        with open(config_path, "w") as config_file:
            config.write(config_file)
            
        print(f"[+] Config saved successfully!")
    else:
        config.read(config_path)

    try:
        BOT_TOKEN = config.get("Telegram", "BOT_TOKEN")
        CHAT_ID = config.get("Telegram", "CHAT_ID")
    except (configparser.NoSectionError, configparser.NoOptionError):
        return f"[!] Error: Invalid config format. Please delete {config_path} and try again."

    print(f"[i] Sending {os.path.basename(last_saved_report_path)} to Telegram...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    
    try:
        with open(last_saved_report_path, 'rb') as file:
            files = {'document': file}
            data = {'chat_id': CHAT_ID, 'caption': "🤖 VAnalyzer: New System Report"}
            response = requests.post(url, files=files, data=data)
            
        if response.status_code == 200:
            return "[+] Report successfully delivered to Telegram!"
        else:
            return f"[!] Failed to send. Telegram API response: {response.text}"
            
    except Exception as e:
        return f"[!] Network error: {e}"

system_commands = {
    '/exit': ('Quit the utility', cmd_exit),
    '/clear': ('Clear the terminal screen', cmd_clear),
    '/refresh': ('Reload the dashboard', cmd_refresh),
    '/savereport': ('Save report', cmd_save_report),
    '/sendreport': ('Send report to your Telegram', cmd_send_report)
}