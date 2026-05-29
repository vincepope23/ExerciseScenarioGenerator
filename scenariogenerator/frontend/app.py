import os

import streamlit as st
from dotenv import load_dotenv

from scenariogenerator.backend.user_actions import get_gefahr_options, generate_szenario, get_user_input_prompt, get_locations
from scenariogenerator.constants import ROOT_DIR

# --- 1. SEITEN-KONFIGURATION ---
st.set_page_config(
    page_title="Exercise Scenario Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()
api_token = os.getenv("MISTRAL_API_KEY")

# --- 2. HEADER: BILD UND TITEL ---
header_left, header_right = st.columns([1, 2], vertical_alignment="center")

with header_left:
    st.image(ROOT_DIR / "scenariogenerator/frontend/header für front-end.png", use_container_width=True)
    
with header_right:
    st.title("Exercise Scenario Generator")

st.write("---") 

# --- 3. CUSTOM CSS ---
st.markdown("""
    <style>
    /* BANNER STYLING (Dunkelgrün + Weisser Text) */
    [data-testid="stHorizontalBlock"]:first-of-type {
        background-color: #24362B !important; 
        border-radius: 12px;
        padding: 15px 20px;
        margin-bottom: 20px;
    }
    
    [data-testid="stHorizontalBlock"]:first-of-type, 
    [data-testid="stHorizontalBlock"]:first-of-type * {
        color: white !important;
    }
    
    [data-testid="stHorizontalBlock"]:first-of-type h1 {
        margin-top: 0px;
        margin-bottom: 0px;
    }

    /* DROPDOWN TITEL GLOBAL WEISS (Die Beschriftung über der Box) */
    div[data-testid="stSelectbox"] label p {
        color: white !important;
        font-weight: 500;
    }
    
    /* --- NEU: DROPDOWN BOX INHALTE SCHWARZ --- */
    /* Macht den ausgewählten Text in den Gefahr- und Location-Dropdowns schwarz */
    div[data-baseweb="select"] * {
        color: black !important;
        -webkit-text-fill-color: black !important;
    }

    /* FIX: EINGABEFELD (TEXT AREA) ZWINGEND HELL & TEXT SCHWARZ */
    .stTextArea textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
        -webkit-text-fill-color: #000000 !important; 
    }

    /* --- NEU: RECHTE BOX (Szenariotext) ZWINGEND SCHWARZ --- */
    /* Geht sicher, dass auch Listen, Absätze und fettgedruckter Text schwarz werden */
    .scenario-box, 
    .scenario-box * {
        color: black !important;
        -webkit-text-fill-color: black !important;
    }

    /* BUTTON STYLING (Swiss Red) */
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
    
    /* RECHTE BOX (Basis-Design) */
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


# --- 4. SESSION STATE INITIALISIERUNG ---
if "generated_scenario" not in st.session_state:
    st.session_state.generated_scenario = "Wählen Sie links Ihre Parameter und klicken Sie auf **CREATE**, um ein Szenario zu generieren."

if "ausgangslage_text" not in st.session_state:
    st.session_state.ausgangslage_text = get_user_input_prompt()


# --- 5. RASTER-AUFTEILUNG (50/50) ---
left_col, right_col = st.columns([1, 1], gap="large")

# --- LINKE SPALTE: EINGABE ---
def update_location_options():
    st.session_state.location_options = get_locations(st.session_state.selected_gefahr)

with left_col:
    st.markdown("<h3 style='color: white;'>Konfiguration</h3>", unsafe_allow_html=True)

    # 1. Gefahr Dropdown
    gefahr_options = get_gefahr_options()
    selected_gefahr = st.selectbox(
        "Gefahr (Hazard)",
        gefahr_options,
        key="selected_gefahr",
        on_change=update_location_options
    )

    # Initialize location_options in session_state if not present
    if "location_options" not in st.session_state:
        st.session_state.location_options = get_locations(selected_gefahr)

    # 2. Location Dropdown
    selected_location = st.selectbox(
        "Ort (Location)",
        st.session_state.location_options,
        key="selected_location"
    )

    # 3. Prompt text editable (Ausgangslage)
    editable_prompt = st.text_area("Ausgangslage (bearbeitbar)", key="ausgangslage_text", height=140)

    st.write("")  # Layout spacer

    # 4. CREATE Button
    if st.button("CREATE"):
        with st.spinner("Generiere Szenario..."):
            st.session_state.generated_scenario = generate_szenario(
                selected_gefahr, selected_location, editable_prompt, "mistral"
            )

# --- RECHTE SPALTE: AUSGABE ---
with right_col:
    st.markdown("<h3 style='color: white;'>Szenario</h3>", unsafe_allow_html=True)
    
    # Render den Text mit absolut zwingendem INLINE-CSS für schwarze Schrift
    st.markdown(
        f'<div class="scenario-box" style="background-color: #F8F9FA !important; color: black !important;">'
        f'<div style="color: black !important;">{st.session_state.generated_scenario}</div>'
        f'</div>', 
        unsafe_allow_html=True
    )