import streamlit as st
# from scenariogenerator.backend.user_actions import get_gefahr_options, get_prompt, generate_szenario

# Set up page layout
st.set_page_config(
    page_title="Exercise Scenario Generator",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        background-color: #D52B1E !important; 
        color: white !important;
        font-weight: bold !important;
        font-size: 20px !important;
        width: 100%;
        border-radius: 8px;
        border: none;
        padding: 12px 0px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #A31F15 !important;
    }
    .scenario-box {
        background-color: #F8F9FA;
        padding: 24px;
        border-radius: 12px;
        min-height: 480px;
        border-left: 6px solid #D52B1E;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER: IMAGE AND TITLE ON THE SAME HEIGHT ---
# Adjust the numbers in [1, 5] to change the width ratio between the image and title
# Find this line in your code:
# header_left, header_right = st.columns([1, 5], vertical_alignment="center")

# Change it to this (makes the image significantly larger):
header_left, header_right = st.columns([1, 2], vertical_alignment="center")
with header_left:
    st.image("header für front-end.png", use_container_width=True)
    
with header_right:
    st.title("Exercise Scenario Generator")

st.write("---")

# Initialize session state
if "generated_scenario" not in st.session_state:
    st.session_state.generated_scenario = "Wählen Sie links Ihre Parameter und klicken Sie auf **CREATE**, um ein Szenario zu generieren."

if "ausgangslage_text" not in st.session_state:
    st.session_state.ausgangslage_text = (
        "In den Schweizer Regionen ereignet sich ein unvorhergesehener Zwischenfall...\n"
        "Eine koordinierte Rettungsaktion wird notwendig, bei der die lokalen Behörden "
        "schnell reagieren müssen."
    )

# Split screen 50/50
left_col, right_col = st.columns([1, 1], gap="large")

# --- LEFT COLUMN: WORKSPACE CONTROLS ---
with left_col:
    st.subheader("Szenario")
    
    # Mocking the backend options for demonstration
    gefahr_options = ["Brand", "Überschwemmung", "Cyberangriff"] 
    selected_gefahr = st.selectbox("Gefahr (Hazard)", gefahr_options)
    
    locato_options = ["Muri", "Zollikofen", "Bern", "Gstaad", "Basel", "Grindelwald"]
    selected_locato = st.selectbox("Ort (Location)", locato_options)
    
    if st.button("🔄 Ausgangslage anpassen"):
        st.session_state.ausgangslage_text = f"Neuer Text für {selected_gefahr}..."

    editable_ausgangslage = st.text_area(
        "Ausgangslage bearbeiten:", 
        value=st.session_state.ausgangslage_text, 
        height=200
    )
    
    if st.button("CREATE"):
        st.session_state.generated_scenario = "Szenario erfolgreich generiert!"

# --- RIGHT COLUMN: OUTPUT ---
with right_col:
    st.subheader("Output")
    st.markdown(f"""
        <div class="scenario-box">
            {st.session_state.generated_scenario}
        </div>
    """, unsafe_allow_html=True)
