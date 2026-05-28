import streamlit as st
from scenariogenerator.backend.user_actions import get_gefahr_options, get_prompt, generate_szenario

# Set up page layout to wide to comfortably fit the side-by-side design
st.set_page_config(
    page_title="Exercise Scenario Generator",
    layout="wide"
)

# Custom CSS to mimic a modern app frame with a distinct right sidebar panel
st.markdown("""
    <style>
    /* Make the button a sharp Swiss Red interactive element */
    .stButton>button {
        background-color: #D52B1E !important; /* Swiss Red */
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
    /* Right panel background box */
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

st.title("Exercise Scenario Generator")
st.write("---")

# Initialize session state so the scenario persists across browser updates
if "generated_scenario" not in st.session_state:
    st.session_state.generated_scenario = "Wählen Sie links Ihre Parameter und klicken Sie auf **CREATE**, um ein Szenario zu generieren."

# Initialize session state for the editable prompt
if "ausgangslage_text" not in st.session_state:
    st.session_state.ausgangslage_text = (
        "In den Schweizer Regionen ereignet sich ein unvorhergesehener Zwischenfall...\n"
        "Eine koordinierte Rettungsaktion wird notwendig, bei der die lokalen Behörden "
        "schnell reagieren müssen."
    )

# Split screen 50/50 between the left main workspace and the right output sidebar
left_col, right_col = st.columns([1, 1], gap="large")

# --- LEFT COLUMN: WORKSPACE CONTROLS ---
with left_col:
    st.subheader("Szenario")
    
    # 1. Gefahr Dropdown
     #gefahr_options = ["Lawinen", "Überflutung", "Gletscherabbruch", "Erdbeben", "Steinschlag"]
    gefahr_options = get_gefahr_options()
    selected_gefahr = st.selectbox("Gefahr (Hazard)", gefahr_options)
    
    # 2. Location Dropdown
    locato_options = ["Muri", "Zollikofen", "Bern", "Gstaad", "Basel", "Grindelwald"]
    selected_locato = st.selectbox("Ort (Location)", locato_options)
    
    # NEW FEATURE: Refresh Button for the Prompt
    if st.button("Aktuellisieren"):
        # st.session_state.ausgangslage_text = (
        #     f"Aufgrund des Ereignisses '{selected_gefahr}' in der Region {selected_locato} "
        #    f"ist die Lage unübersichtlich. Erste zivile Notrufe gehen ein, und die "
        #    f"wichtigsten Zufahrtsstrassen sind aktuell nicht passierbar. Die Blaulichtorganisationen "
        #     f"benötigen umgehend Anweisungen zur Priorisierung."
        # )
        st.session_state.ausgangslage_text = get_prompt(selected_gefahr)

    # 3. Prompt text editable (Ausgangslage) - Now tied to session_state key
    editable_prompt = st.text_area("Ausgangslage (bearbeitbar)", key="ausgangslage_text", height=140)
    
    st.write("") # Layout spacer
    
    # 4. CREATE Button (Syntax fix applied here)
    if st.button("CREATE"):
        st.session_state.generated_scenario = f"""
### 🚨 Szenario: Krisenfall in {selected_locato}

**Ausgangslage:** {editable_prompt}

**Ereignis:** In der Region **{selected_locato}** hat sich eine kritische Situation durch das Ereignis **{selected_gefahr}** entwickelt.

**Auswirkungen:** Wichtige Verkehrsachsen sind blockiert. Die lokalen Einsatzkräfte (Blaulichtorganisationen) koordinieren sich eng mit dem zuständigen Führungsstab. Die Lage erfordert die sofortige Priorisierung von Schutzmassnahmen und eine rasche Ressourceneinteilung vor Ort.
"""

# --- RIGHT COLUMN: THE SIDEBAR PANEL ---
with right_col:
    st.subheader("Szenario")
    
    # Render the text smoothly inside the designated right layout panel 
    st.markdown(
        f'<div class="scenario-box">{st.session_state.generated_scenario}</div>', 
        unsafe_allow_html=True

    )