import subprocess
import os
import shutil

# Get the absolute path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MERMAID_FILE_PATH = os.path.join(current_dir, "flowchart.mmd")
OUTPUT_FILE = os.path.join(current_dir, "flowchart.png")

# Rest of your code from flowchart.py remains the same...