import subprocess
import os
import shutil

# Path to the input Mermaid.js file
MERMAID_FILE_PATH = "/Users/tamilselavans/Downloads/roadmap-GPT/backend/flowchart.mmd"
OUTPUT_FILE = "/Users/tamilselavans/Downloads/roadmap-GPT/backend/flowchart.png"  # High-quality output image

def read_mermaid_code(file_path):
    """Reads Mermaid.js code from a file and ensures it's valid."""
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found - {file_path}")
        return None

    with open(file_path, "r") as file:
        mermaid_code = file.read().strip()

    if not mermaid_code:
        print("❌ Error: Mermaid.js file is empty!")
        return None

    # Ensure the first line starts with `graph TD;`
    if not mermaid_code.startswith("graph TD;"):
        print("❌ Error: Mermaid.js code is incorrect! The first line must start with 'graph TD;'.")
        return None

    return mermaid_code

def generate_flowchart(mermaid_code, output_file=OUTPUT_FILE):
    """Generates a high-quality flowchart image from Mermaid code using Mermaid CLI."""
    
    # Save the Mermaid code to a temporary file
    temp_mermaid_file = "temp_flowchart.mmd"
    with open(temp_mermaid_file, "w") as file:
        file.write(mermaid_code)

    # ✅ Ensure `mmdc` is installed
    if not shutil.which("mmdc"):
        print("❌ Error: Mermaid CLI (`mmdc`) is not installed. Install using `npm install -g @mermaid-js/mermaid-cli puppeteer`")
        return None

    # ✅ Run Mermaid CLI with improved resolution
    try:
        subprocess.run(
            ["mmdc", "-i", temp_mermaid_file, "-o", output_file,
             "--scale", "2",
             "--width", "3000",
             "--height", "2000",
             "--backgroundColor", "#ffffff",
             "--theme", "default"],
            check=True
        )
            
        print(f"✅ Flowchart generated successfully: {output_file}")
        
        # Clean up temporary file
        os.remove(temp_mermaid_file)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating flowchart: {e.stderr}")
        print(f"🔍 Debug Info: {e.stderr}")

# Remove the __main__ block since we'll call these functions from the frontend
if __name__ == "__main__":
    pass
    # Read and validate Mermaid.js code
    mermaid_code = read_mermaid_code(MERMAID_FILE_PATH)

    if mermaid_code:
        generate_flowchart(mermaid_code)
    else:
        print("❌ Failed to generate flowchart due to missing or invalid file.")
