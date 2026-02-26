import pyshark
import os
from config import TSHARK_PATH

def load_pcap(directory, display_filter=None):
    captures = []

    for file in os.listdir(directory):
        if file.endswith((".pcap", ".pcapng")):
            path = os.path.join(directory, file)

            cap = pyshark.FileCapture(
                path,
                display_filter=display_filter,
                tshark_path=TSHARK_PATH,
            )

            captures.append((file, cap))

    return captures