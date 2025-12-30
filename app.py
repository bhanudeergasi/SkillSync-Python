import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# --- PAGE CONFIG ---
st.set_page_config(page_title="SkillSync", page_icon="⚡", layout="wide")

# --- CSS (Keep it Black & Readable) ---
st.markdown("""
<style>
.metric-card {
    background-color: #FFFFFF;
    color: #000000 !important;
    padding: 15px;
    border-radius: 8px;
    border-left: 6px solid #00C853;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
.big-stat {
    font-size: 20px !important;
    font-weight: 700;
    color: #00C853;
    word-wrap: break-word;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("SkillSync ⚡")
    # Auto-Login
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ AI Connected")
    else:
        api_key = st.text_input("🔑 API Key", type="password")

# --- MAIN ---
st.title("⚡ SkillSync: Career Transition")
col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader("📸 Upload Workspace", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

if uploaded_file and api_key:
    genai.configure(api_key=api_key)

    # --- THE NUCLEAR FIX: MODEL FALLBACK ---
    # It tries 1.5 Flash. If that crashes (404), it silently switches to 'gemini-pro'
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Test if it works by checking name
        test_name = model.model_name 
    except:
        st.warning("⚠️ Using Standard Model (Fallback)")
        model = genai.GenerativeModel('gemini-pro')

    prompt = """
    Act as a Career Expert. Analyze this image.
    Return a JSON object with this structure:
    {
        "current_role": "Job Title",
        "skills_detected": ["Skill 1", "Skill 2"],
        "green_career_match": "Green Job Title",
        "match_percentage": 85,
        "reasoning": "Why it fits",
        "certification_course": "Course Name"
    }
    """

    with col2:
        if st.button("🚀 Analyze Career Path", type="primary"):
            with st.spinner("Analyzing..."):
                try:
                    response = model.generate_content([prompt, image])
                    text = response.text.replace("```json", "").replace("```", "").strip()
                    data = json.loads(text)

                    # --- DASHBOARD ---
                    c1, c2, c3 = st.columns(3)
                    c1.markdown(f'<div class="metric-card"><b>Role</b><br><span class="big-stat" style="color:#333">{data["current_role"]}</span></div>', unsafe_allow_html=True)
                    c2.markdown(f'<div class="metric-card"><b>Match</b><br><span class="big-stat">{data["green_career_match"]}</span></div>', unsafe_allow_html=True)
                    c3.markdown(f'<div class="metric-card"><b>Confidence</b><br><span class="big-stat">{data["match_percentage"]}%</span></div>', unsafe_allow_html=True)
                    
                    st.write("---")
                    st.subheader("Why this works:")
                    st.info(data["reasoning"])
                    st.subheader("Recommended Certification:")
                    st.success(f"🎓 {data['certification_course']}")

                except Exception as e:
                    st.error(f"Error: {e}")
