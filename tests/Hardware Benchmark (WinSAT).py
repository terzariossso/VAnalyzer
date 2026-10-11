import subprocess
import json

"""
==============================================================================
Module: Hardware Benchmark (WinSAT)
==============================================================================
Description:
    Runs native Windows System Assessment Tool (WinSAT) to benchmark 
    raw hardware performance (CPU compression/encryption and Disk I/O).
    
Note: WinSAT requires Administrator privileges to run accurately. 
If run without admin rights, the subprocess will fail gracefully.
==============================================================================
"""

def score_checker():
    result = subprocess.run("winsat formal", shell=True, capture_output=True, text=True)

    if result.returncode != 0 or result.stderr:
        error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
        return f"[!] Failed to perform 'winsat formal'\nReason: {error_msg}"

    else:
        powershell_cmd = "Get-CimInstance Win32_WinSAT | Select-Object CPUScore, MemoryScore, GraphicsScore, D3DScore, DiskScore, WinSPRLevel | ConvertTo-Json"
        ps_result = subprocess.run(
            ["powershell", "-Command", powershell_cmd],
            capture_output=True,
            text=True,
        )
        
        data = json.loads(ps_result.stdout)
        
        return (
            f"=== Windows Experience Index (1.0 - 9.9) ===\n"
            f"CPU Score: {data.get('CPUScore')}\n"
            f"Memory Score: {data.get('MemoryScore')}\n"
            f"Graphics Score: {data.get('GraphicsScore')}\n"
            f"Disk Score: {data.get('DiskScore')}\n"
            f"Final Index (lowest one): {data.get('WinSPRLevel')}\n"
    )

print(score_checker())