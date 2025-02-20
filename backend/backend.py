import os
import re
import requests

# Groq API Credentials
GROQ_API_KEY = "YOUR GROQ API KEY"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Path where the Mermaid.js file will be saved
MERMAID_FILE_PATH = "/Users/tamilselavans/Downloads/roadmap-GPT/backend/flowchart.mmd"

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

    ### **Example Output Format**
    graph TD;
        
        subgraph "Python Basics"
            A1["Install Python"] -->|Basic Syntax| B["Variables, Data Types & Operators"]
            A2["Control Flow"] -->|Conditional Statements| B
            A2 -->|Loops| C["For, While, List Comprehensions"]
            A2 -->|Functions| D["Defining & Calling Functions"]
        end

        subgraph "Python Advanced"
            C -->|Generators & Iterators| E["yield, next, for-else"]
            C -->|Lambda Functions & Map| F["Anonymous Functions & Higher-Order Functions"]
            D -->|Decorators| G["@decorator syntax"]
            B -->|Complex Data Structures| H["Lists, Tuples, Dictionaries, Sets"]
        end
    """

    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(GROQ_API_URL, json=payload, headers=headers)
    response_json = response.json()

    if "choices" in response_json and len(response_json["choices"]) > 0:
        return response_json["choices"][0]["message"]["content"]
    else:
        return "Error: Groq API did not return a valid response"

def clean_mermaid_code(mermaid_code):
    """Cleans the Mermaid.js code by removing extra text and ensuring proper syntax."""
    # ✅ Remove markdown-style ```mermaid ... ```
    mermaid_code = re.sub(r"```mermaid", "", mermaid_code, flags=re.IGNORECASE).strip()
    mermaid_code = re.sub(r"```", "", mermaid_code).strip()

    # ✅ Remove unwanted explanations, notes, and comments
    mermaid_code = re.sub(r"Note:.*", "", mermaid_code)
    mermaid_code = re.sub(r"This is a suggested.*", "", mermaid_code)

    # ✅ Remove duplicate `end` statements
    mermaid_code = re.sub(r"\n\s*end\s*end", "\nend", mermaid_code)

    # ✅ Ensure Mermaid.js starts with `graph TD;`
    mermaid_lines = mermaid_code.split("\n")
    mermaid_lines = [line for line in mermaid_lines if "graph TD;" in line or "-->" in line or "subgraph" in line or "end" in line]

    if not mermaid_lines[0].startswith("graph TD;"):
        print("❌ Error: Mermaid.js output does not start with 'graph TD;'. Fixing...")
        mermaid_lines.insert(0, "graph TD;")

    cleaned_mermaid_code = "\n".join(mermaid_lines)
    return cleaned_mermaid_code

def save_mermaid_code(mermaid_code):
    """Save Mermaid.js code to the specified file"""
    try:
        with open(MERMAID_FILE_PATH, "w") as file:
            file.write(mermaid_code)
        print(f"✅ Mermaid.js code saved successfully: {MERMAID_FILE_PATH}")
    except Exception as e:
        print(f"❌ Error saving Mermaid.js file: {e}")

# Remove the __main__ block since we'll call these functions from the frontend
if __name__ == "__main__":
    pass
    topic = input("Enter the topic for the roadmap: ")  # Get user input
    mermaid_code = generate_roadmap(topic)

    if not mermaid_code.startswith("Error"):
        clean_code = clean_mermaid_code(mermaid_code)
        if clean_code:
            save_mermaid_code(clean_code)
        else:
            print("❌ Mermaid.js code is not valid for rendering.")
    else:
        print("❌ Failed to generate Mermaid.js code.")
