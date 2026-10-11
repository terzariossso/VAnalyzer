import os


"""
==============================================================================
Module: Junk & Startup Scanner
==============================================================================
Description:
    This module analyzes the system for unnecessary files and startup bloatware 
    that consume disk space and degrade boot performance.

Target Deliverables:
    1. Junk File Analysis:
       - Target locations: Windows %TEMP%, Prefetch, SoftwareDistribution (Update Cache), 
         and Recycle Bin.
       - Logic: Iterate through paths, safely calculate total wasted space (in MB/GB), 
         and handle PermissionErrors for protected directories.
         
    2. Startup Tasks Scanner:
       - Target locations: Registry Run keys (HKCU & HKLM) and Windows Startup folder.
       - Logic: Extract active startup applications and background services that 
         launch on boot.

Future Implementation:
    - Display total junk size to the user.
    - Provide an option or list to identify heavy/unwanted startup programs.
==============================================================================
"""

# Defining the junk containing locations dynamically

system_drive = os.environ.get('SystemDrive', 'C:')
windows_dir = os.environ.get('WINDIR', f'{system_drive}\\Windows')
user_temp = os.environ.get('TEMP')

junk_locations = {
  "User Temp": user_temp,
  "System Temp": os.path.join(windows_dir, 'Temp'),
  "Prefetch": os.path.join(windows_dir, 'Prefetch'),
  "Update Cache": os.path.join(windows_dir, 'SoftwareDistribution', 'Download'),
  "Recycle Bin": f"{system_drive}\\$Recycle.Bin"
}

def get_dir_size(path):
    total_size = 0
    try:
        # os.walk goes though all folders and subfolders
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                file_path = os.path.join(dirpath, f)
                if not os.path.islink(file_path):
                    try:
                        total_size += os.path.getsize(file_path)
                    except (PermissionError, FileNotFoundError):
                        pass
    except PermissionError:
        pass
        
    return total_size

total_junk_bytes = 0

def junk_scan():
    global total_junk_bytes
    
    for name, path in junk_locations.items():
        if os.path.exists(path):
            folder_size_bytes = get_dir_size(path)
            total_junk_bytes += folder_size_bytes

            size_mb = folder_size_bytes / (1024 * 1024)
            print(f"{name}: {size_mb:.1f} MB | Link: {path}")
        else:
            print(f"{name}: Path not found")

    total_mb = total_junk_bytes / (1024 * 1024)
    print(f"---------------------------")
    print(f"Total Junk Found: {total_mb:.1f} MB\n")

if __name__ == "__main__":
    junk_scan()