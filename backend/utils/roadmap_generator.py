import os
import re
import requests

# Get the absolute path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MERMAID_FILE_PATH = os.path.join(current_dir, "flowchart.mmd")

# Groq API Credentials
GROQ_API_KEY = "YOUR GROQ API KEY"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_roadmap(topic):
    """Generate a structured hierarchical roadmap in Mermaid.js syntax using Groq API"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""
    Generate a **structured hierarchical roadmap** for {topic} in **Mermaid.js syntax**.

    ### **Flowchart Requirements**
    - Use `graph TD;` for **top-down** structure.
    - Use **subgraph** blocks to organize sections.
    - **Ensure readable and structured nodes**.
    - **Return ONLY valid Mermaid.js syntax (no extra text, notes, or explanations).**
    - **Every `subgraph` must have exactly one `end` statement.**
    """

    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        response_json = response.json()

        if "choices" in response_json and len(response_json["choices"]) > 0:
            return response_json["choices"][0]["message"]["content"]
        else:
            return "Error: Groq API did not return a valid response"
    except Exception as e:
        return f"Error: {str(e)}"

def clean_mermaid_code(mermaid_code):
    """Cleans the Mermaid.js code by removing extra text and ensuring proper syntax."""
    # Remove markdown-style ```mermaid ... ```
    mermaid_code = re.sub(r"```mermaid", "", mermaid_code, flags=re.IGNORECASE).strip()
    mermaid_code = re.sub(r"```", "", mermaid_code).strip()

    # Remove unwanted explanations, notes, and comments
    mermaid_code = re.sub(r"Note:.*", "", mermaid_code)
    mermaid_code = re.sub(r"This is a suggested.*", "", mermaid_code)

    # Remove duplicate `end` statements
    mermaid_code = re.sub(r"\n\s*end\s*end", "\nend", mermaid_code)

    # Ensure Mermaid.js starts with `graph TD;`
    mermaid_lines = mermaid_code.split("\n")
    mermaid_lines = [line for line in mermaid_lines if "graph TD;" in line or "-->" in line or "subgraph" in line or "end" in line]

    if not mermaid_lines[0].startswith("graph TD;"):
        mermaid_lines.insert(0, "graph TD;")

    cleaned_mermaid_code = "\n".join(mermaid_lines)
    return cleaned_mermaid_code

def save_mermaid_code(mermaid_code):
    """Save Mermaid.js code to the specified file"""
    try:
        with open(MERMAID_FILE_PATH, "w") as file:
            file.write(mermaid_code)
        return True
    except Exception as e:
        print(f"Error saving Mermaid.js file: {e}")
        return False

if __name__ == "__main__":
    pass