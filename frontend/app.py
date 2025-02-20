import streamlit as st
import os
from PIL import Image
import time
import sys

# Add the correct path to backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.utils.roadmap_generator import generate_roadmap, clean_mermaid_code, save_mermaid_code
from backend.utils.flowchart import generate_flowchart, read_mermaid_code

# Page configuration
st.set_page_config(
    page_title="SmartFlow AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2E4B7C;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #2E4B7C;
        color: white;
        padding: 0.5rem 2rem;
        font-size: 1.2rem;
    }
    .stTextInput>div>div>input {
        font-size: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Paths
FLOWCHART_PATH = "/backend/flowchart.png"
MERMAID_FILE_PATH = "/backend/flowchart.mmd"

# App Header
st.title("🚀 SmartFlow AI")
st.markdown("### Transform Your Ideas into Visual Roadmaps")

# Sidebar with options
with st.sidebar:
    st.header("⚙️ Configuration")
    chart_style = st.selectbox(
        "Chart Style",
        ["Default", "Modern", "Forest", "Dark"]
    )
    complexity = st.slider(
        "Complexity Level",
        1, 5, 3,
        help="Adjust the detail level of your roadmap"
    )

# Main content
col1, col2 = st.columns([2, 1])
with col1:
    topic = st.text_input("🎯 Enter your topic:", "", 
                         placeholder="e.g., Machine Learning, Web Development, Project Management")

with col2:
    if st.button("🔮 Generate Flowchart", use_container_width=True):
        if topic:
            with st.spinner("🎨 Creating your roadmap..."):
                # Generate and save mermaid code
                mermaid_code = generate_roadmap(topic)
                if not mermaid_code.startswith("Error"):
                    clean_code = clean_mermaid_code(mermaid_code)
                    if clean_code:
                        save_mermaid_code(clean_code)
                        mermaid_code = read_mermaid_code(MERMAID_FILE_PATH)
                        if mermaid_code:
                            generate_flowchart(mermaid_code)
                            st.success("✨ Your roadmap is ready!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Failed to generate flowchart.")
                    else:
                        st.error("❌ Invalid flowchart structure.")
                else:
                    st.error("❌ Failed to generate roadmap.")
        else:
            st.warning("⚠️ Please enter a topic first.")

# Display the generated flowchart
if os.path.exists(FLOWCHART_PATH):
    st.markdown("---")
    st.markdown("### 📊 Your Generated Roadmap")
    
    # Image display and download in columns
    img_col, btn_col = st.columns([4, 1])
    with img_col:
        image = Image.open(FLOWCHART_PATH)
        st.image(image, caption=f"Roadmap for: {topic}", use_column_width=True)
    
    with btn_col:
        with open(FLOWCHART_PATH, "rb") as file:
            st.download_button(
                label="📥 Download",
                data=file,
                file_name=f"{topic.lower().replace(' ', '_')}_roadmap.png",
                mime="image/png",
                help="Download your roadmap as PNG"
            )
        
        # Add sharing options
        st.markdown("### 📤 Share")
        st.button("📧 Email", use_container_width=True)
        st.button("📱 Social", use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        Made with ❤️ by SmartFlow AI Team
    </div>
    """, 
    unsafe_allow_html=True
)
