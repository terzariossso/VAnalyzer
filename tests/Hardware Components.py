import subprocess
import json

"""
==============================================================================
Module: Hardware Components 
==============================================================================
Description:
    Performs a deep scan of the system's physical hardware architecture using 
    WMI (Windows Management Instrumentation) via PowerShell. Extracts and 
    formats detailed specifications for core components.

Target Components:
    1. Processor (CPU): Model, Cores, Threads, Architecture.
    2. Graphics (GPU): Model, VRAM, Driver Version, Current Resolution.
    3. Memory (RAM): Capacity, Speed, Manufacturer, Physical Location.
    4. Storage (Disks): Physical drive status & Logical volume partitioning.
    5. Motherboard: Manufacturer, Product ID, Serial Number.
    6. Network Adapters: MAC Address, Link Speed, Status.
==============================================================================
"""

def cpu_checker():
    powershell_cmd = "Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors, Architecture | ConvertTo-Json"
    result = subprocess.run(
        ["powershell", "-Command", powershell_cmd],
        capture_output= True,
        text = True,
    )
    data = json.loads(result.stdout)

    arch_map = {0: "x86 (32-bit)", 5: "ARM", 9: "x64 (64-bit)", 12: "ARM64"}
    arch_code = data.get("Architecture", 9)
    arch_readable = arch_map.get(arch_code)
    
    return (
        f"--- PROCESSOR --- \n"
        f"CPU: {data.get('Name')}\n"
        f"Number of Cores: {data.get('NumberOfCores')}\n"
        f"Number of Logical Processors: {data.get('NumberOfLogicalProcessors')}\n"
        f"Architecture: {arch_readable}\n\n"
    )

def gpu_checker():
    powershell_cmd = "Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion, CurrentHorizontalResolution, CurrentVerticalResolution, CurrentRefreshRate | ConvertTo-Json"
    result = subprocess.run(
        ["powershell", "-Command", powershell_cmd],
        capture_output= True,
        text = True,
    )

    final_output = ""
    final_output += "--- GRAPHIC INTERFACES ---\n"
    data = json.loads(result.stdout)

    for gpu in data:
        name = gpu.get('Name', 'Unknown')

        if 'Display' in name:
            continue
        raw_ram = gpu.get('AdapterRAM')
        if raw_ram:
            ram_gb = round(raw_ram / (1024**3))
            ram_text = f"{ram_gb} GB"
        else:
            ram_text = "N/A"
        raw_resolution_horizontal = gpu.get('CurrentHorizontalResolution')
        raw_resolution_vertical = gpu.get('CurrentVerticalResolution')

        if not raw_resolution_horizontal or not raw_resolution_vertical:
            final_resolution = "N/A"
        else:
            final_resolution = f"{raw_resolution_horizontal}x{raw_resolution_vertical}"

        final_output += (
            f"GPU: {name}\n"
            f"Adapter RAM: {ram_text}\n"
            f"Driver Version: {gpu.get('DriverVersion')}\n"
            f"Resolution: {final_resolution}\n\n"
        )
        
    return final_output.strip() 

def ram_checker():
    powershell_cmd = 'Get-CimInstance Win32_PhysicalMemory | Select-Object DeviceLocator, @{Name="Capacity (GB)"; Expression={$_.Capacity / 1GB}}, Speed, Manufacturer, PartNumber | ConvertTo-Json'
    result = subprocess.run(
        ["powershell", "-Command", powershell_cmd],
        capture_output= True,
        text = True,
    )

    final_output = ""
    final_output += "--- MEMORY ---\n"
    data = json.loads(result.stdout)
    
    for ram in data:
        final_output += (
            f"RAM Manufacturer: {ram.get('Manufacturer')}\n"
            f"Speed: {ram.get('Speed')}\n"
            f"Capacity (GB): {ram.get('Capacity (GB)')}\n"
            f"Physical Location: {ram.get('DeviceLocator')}\n"
            f"PartNumber: {ram.get('PartNumber')}\n\n"
        )

    return final_output.strip() 

def disks_checker():
    powershell_physical = 'Get-CimInstance Win32_DiskDrive | Select-Object Model, InterfaceType, Status | ConvertTo-Json'
    res_phys = subprocess.run(["powershell", "-Command", powershell_physical], capture_output=True, text=True)
    phys_data = json.loads(res_phys.stdout)
    
    if isinstance(phys_data, dict):
        phys_data = [phys_data]

    final_output = "--- PHYSICAL DRIVES ---\n"
    for disk in phys_data:
        final_output += (
            f"Model: {disk.get('Model')}\n"
            f"Interface: {disk.get('InterfaceType')}\n"
            f"Status: {disk.get('Status')}\n\n"
        )

    powershell_logical = 'Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3 OR DriveType=2" | Select-Object DeviceID, VolumeName, FileSystem, @{Name="Size (GB)"; Expression={[math]::Round($_.Size / 1GB, 2)}}, @{Name="FreeSpace (GB)"; Expression={[math]::Round($_.FreeSpace / 1GB, 2)}} | ConvertTo-Json'
    res_log = subprocess.run(["powershell", "-Command", powershell_logical], capture_output=True, text=True)
    log_data = json.loads(res_log.stdout)
    
    if isinstance(log_data, dict):
        log_data = [log_data]

    final_output += "--- LOGICAL VOLUMES ---\n"
    for vol in log_data:
        vol_name = vol.get('VolumeName') or "Local Disk" 
        final_output += (
            f"Partition: {vol.get('DeviceID')} [{vol.get('FileSystem')}]\n"
            f"Volume Name: {vol_name}\n"
            f"Total Space: {vol.get('Size (GB)')} GB\n"
            f"Free Space: {vol.get('FreeSpace (GB)')} GB\n\n"
        )

    return final_output.strip()

def motherboard_checker():
    powershell_cmd = "Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer, Product, SerialNumber | ConvertTo-Json"
    result = subprocess.run(
        ["powershell", "-Command", powershell_cmd],
        capture_output= True,
        text = True,
    )
    data = json.loads(result.stdout)
    
    return (
        f"--- MOTHERBOARD ---\n"
        f"Manufacturer: {data.get('Manufacturer')}\n"
        f"Model: {data.get('Product')}\n"
        f"Serial Number: {data.get('SerialNumber')}\n\n"
    )

def network_adapters_checker():
    powershell_cmd = 'Get-NetAdapter -Physical | Select-Object Name, InterfaceDescription, Status, LinkSpeed, MacAddress | ConvertTo-Json'
    result = subprocess.run(
        ["powershell", "-Command", powershell_cmd],
        capture_output= True,
        text = True,
    )

    final_output = ""
    final_output += "--- NETWORK ADAPTERS ---\n"
    data = json.loads(result.stdout)
    
    for net in data:
        final_output += (
            f"Name: {net.get('Name')}\n"
            f"Description: {net.get('InterfaceDescription')}\n"
            f"Status: {net.get('Status')}\n"
            f"Link Speed: {net.get('LinkSpeed')}\n"
            f"MAC Address: {net.get('MacAddress')}\n\n"
        )

    return final_output.strip() 

print(cpu_checker().strip())
print() 
print(gpu_checker().strip())
print()
print(ram_checker().strip())
print()
print(disks_checker().strip())
print()
print(motherboard_checker().strip())
print()
print(network_adapters_checker().strip())