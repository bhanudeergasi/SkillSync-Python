import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="SkillSync Dashboard",
    page_icon="⚡",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* Metric Cards: Cleaner, smaller shadow, visible black text */
    .metric-card {
        background-color: #FFFFFF;
        color: #000000 !important;
        padding: 15px;
        border-radius: 8px;
        border-left: 6px solid #00C853;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        height: 100%;
    }
    
    /* Big Stats: Smaller font, text wrapping enabled */
    .big-stat {
        font-size: 20px !important;
        font-weight: 700;
        color: #00C853;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Labels: Subtle and small */
    .stat-label {
        font-size: 12px;
        color: #666;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 4px;
        letter-spacing: 0.5px;
    }

    /* Description text inside cards */
    .card-text {
        font-size: 14px;
        color: #333;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SMART SIDEBAR (Auto-Login) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
    st.title("SkillSync")
    st.markdown("Mapped for the **Green Economy**")
    st.divider()
    
    # Check if key is in Secrets (Automatic Login)
    if "GOOGLE_API_KEY" in st.secrets:
        st.success("✅ AI Credential Loaded")
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        # Fallback: Ask user if no secret is found
        api_key = st.text_input("🔑 Enter Gemini API Key", type="password")
        st.info("Get free key at [Google AI Studio](https://aistudio.google.com/)")

# --- MAIN HEADER ---
st.title("⚡ SkillSync: Workforce Transition")
st.markdown("### Upload a workspace photo to generate a career pivot plan.")

# --- LAYOUT ---
col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader("📸 Upload Workspace Image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Analyzing Environment...", use_column_width=True)

# --- LOGIC ---
if uploaded_file and api_key:
    genai.configure(api_key=api_key)
    # Using 1.5 Flash for speed and stability
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = """
    Analyze this image of a workspace/worker. 
    Act as a Career Transition Expert.
    Return ONLY a raw JSON object (no markdown formatting) with this exact structure:
    {
        "current_role": "Predicted current job title (e.g. Diesel Mechanic)",
        "skills_detected": ["Skill 1", "Skill 2", "Skill 3", "Skill 4"],
        "green_career_match": "High-growth Green Economy Job Title",
        "match_percentage": 85,
        "reasoning": "Short 1-sentence explanation of why this fits.",
        "certification_course": "Name of a specific certification to take"
    }
    """

    with col2:
        if st.button("🚀 Analyze & Generate Path", type="primary"):
            with st.spinner("⚡ Gemini is analyzing tools, environment, and skills..."):
                try:
                    response = model.generate_content([prompt, image])
                    clean_text = response.text.replace("```json", "").replace("```", "").strip()
                    data = json.loads(clean_text)

                    # --- UI: TOP METRICS ---
                    m1, m2, m3 = st.columns(3)
                    
                    with m1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="stat-label">Current Role</div>
                            <div class="big-stat" style="color: #333;">{data['current_role']}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    with m2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="stat-label">Green Career Match</div>
                            <div class="big-stat">{data['green_career_match']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with m3:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="stat-label">Match Confidence</div>
                            <div class="big-stat">{data['match_percentage']}%</div>
                        </div>
                        """, unsafe_allow_html=True)

                    # --- UI: DETAILS ---
                    st.subheader("🛠️ Skill Bridge")
                    
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        # Reasoning Card
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="stat-label">Why this match?</div>
                            <div class="card-text">
                                {data['reasoning']}
                            </div>
                            <hr style="margin:10px 0; opacity:0.2;">
                            <div class="stat-label">Detected Skills</div>
                            <div class="card-text">
                                {' • '.join(data['skills_detected'])}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with c2:
                        # Certification Card
                        st.markdown(f"""
                        <div class="metric-card" style="border-left-color: #2962FF;">
                            <div class="stat-label">Recommended Certification</div>
                            <div class="big-stat" style="color: #2962FF; font-size: 18px !important;">
                                🎓 {data['certification_course']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.link_button(f"Find Courses: {data['certification_course']}", "https://www.google.com/search?q=" + data['certification_course'])

                    st.success("Analysis Complete.")

                except Exception as e:
                    st.error(f"Error parsing AI response: {e}")
                    with st.expander("Debug Raw Output"):
                        st.write(response.text)

elif not api_key:
    with col2:
        st.warning("👈 Please enter your API Key in the sidebar to start.")
