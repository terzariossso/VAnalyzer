import speedtest

"""
==============================================================================
Module: Network Speed Test
==============================================================================
Description:
    Measures the current network bandwidth and latency by connecting to the 
    optimal Speedtest.net server.

Target Metrics:
    - Ping (Latency in ms)
    - Download Speed (in Mbps)
    - Upload Speed (in Mbps)

Note: This module relies on the external 'speedtest-cli' library and requires 
an active internet connection. Execution time may vary based on network latency.
==============================================================================
"""

def network_speed_checker():
    st = speedtest.Speedtest()
    st.get_best_server()

    download_speed = st.download()
    upload_speed = st.upload()
    ping = st.results.ping

    download_mbps = download_speed / 1_000_000
    upload_mbps = upload_speed / 1_000_000

    return f"Ping: {ping} ms\nDownload: {download_mbps:.2f} Mbps\nUpload: {upload_mbps:.2f} Mbps"

print(network_speed_checker())