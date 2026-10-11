import os
import subprocess
import xml.etree.ElementTree as ET

"""
==============================================================================
Module: Battery Health
==============================================================================
Description:
    Analyzes the system's battery status by extracting telemetry from the native 
    Windows PowerCfg utility. It parses the generated XML report to calculate 
    real-time battery degradation and health percentage.

Target Metrics:
    - Battery Model
    - Design Capacity (Original factory capacity in mWh)
    - Full Charge Capacity (Current maximum capacity in mWh)
    - Approximate Battery Health (%)

Note: If no physical battery is detected (e.g., running on a desktop), 
the module handles the exception gracefully.
==============================================================================
"""

temp_dir = os.environ.get('TEMP')
file_path = os.path.join(temp_dir, 'battery_report.xml')
subprocess.run(f'powercfg /batteryreport /xml /output "{file_path}"', shell=True, capture_output=True)

try: 
    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {'b': 'http://schemas.microsoft.com/battery/2012'}

    battery = root.find('.//b:Batteries/b:Battery', ns)

    if battery is None:
        print("Desktop System: No battery detected. Test skipped.")

    else:
        design_cap = int(battery.find('b:DesignCapacity', ns).text)
        full_cap = int(battery.find('b:FullChargeCapacity', ns).text)
        battery_model = battery.find('b:Id', ns).text
        health_state = (full_cap / design_cap) * 100
        
        print(f"Battery Model:     {battery_model}")
        print(f"Original Capacity: {design_cap} mWh")
        print(f"Current Capacity:  {full_cap} mWh")
        print(f"Approximate Battery Health:  {health_state:.2f}%")

finally:
    if os.path.exists(file_path):
        os.remove(file_path)