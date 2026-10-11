import subprocess
import json
import re
from datetime import datetime

def crash_checker():
    powershell_cmd = "Get-WinEvent -FilterHashtable @{LogName='System'; Id=1001, 41} -MaxEvents 10 -ErrorAction SilentlyContinue | Select-Object Id, TimeCreated, Message | ConvertTo-Json"
    result = subprocess.run(
        ["powershell", "-Command", powershell_cmd],
        capture_output= True,
        text = True,
    )

    if not result.stdout.strip():
        return "--- CRASHES LOG ---\nNo critical crashes found. System is stable."

    data = json.loads(result.stdout)
    
    if isinstance(data, dict):
        data = [data]

    final_output = "--- CRASHES LOG ---\n"

    # id mapping
    id_map = {41: "Unexpected Restart", 1001: "Memory Dump"}
    
    for crash in data:

        id_code = crash.get("Id")
        id_readable = id_map.get(id_code, "Unknown Error")

        raw_time = crash.get("TimeCreated", "")
        readable_time = ""

        match = re.search(r'\d+', raw_time)
        if match:
            timestamp_ms = int(match.group())
            readable_time = datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')

        final_output += (
            f"ID: {id_readable} (Code: {id_code})\n"
            f"Time Created: {readable_time}\n"
            f"Message: {crash.get('Message')}\n\n"
        )

    return final_output.strip() 

print(crash_checker())