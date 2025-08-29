import streamlit as st

# Set page config
st.set_page_config(
    page_title="Delta Shoreline Model",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("🏔️ Delta Shoreline Model")
st.sidebar.markdown("Choose a model to explore:")

model_choice = st.sidebar.radio(
    "Select Model:",
    ["Simple Box Model", "Advanced Model with Slopes"],
    index=0
)

if model_choice == "Simple Box Model":
    # Import and run simple model
    exec(open('simplebox.py').read())
else:
    # Import and run advanced model
    exec(open('advancedbox.py').read())

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
### About
Delta shoreline evolution models for analyzing coastal dynamics under varying sea-level scenarios.

**Models:**
- **Simple**: Basic box model with fundamental parameters
- **Advanced**: Complex model with topset, foreset, and basement slopes

**Features:**
- Interactive parameter adjustment
- Scenario comparison
- Real-time visualization
- Multiple analysis perspectives
""")
