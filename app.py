import streamlit as st
import json
from services.vision_service import VisionAnalyzer
from utils.image_helper import validate_image

# Page Setup
st.set_page_config(page_title="Smart Board Assistant", page_icon="🧠", layout="wide")

# Theme Toggle State
if 'theme' not in st.session_state:
    st.session_state.theme = 'auto'  # auto, light, dark

# Function to get CSS based on theme
def get_themed_css(theme_mode):
    # Determine colors based on theme
    if theme_mode == 'light':
        colors = {
            'bg_primary': 'linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%)',
            'bg_card': '#ffffff',
            'bg_sidebar': 'linear-gradient(180deg, #1e40af 0%, #3b82f6 100%)',
            'bg_upload': 'linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)',
            'bg_radio': '#f8fafc',
            'bg_expander': 'linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)',
            'bg_empty': 'linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)',
            'bg_task': 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)',
            'text_primary': '#1e3a8a',
            'text_secondary': '#334155',
            'text_muted': '#64748b',
            'text_sidebar': '#ffffff',
            'border_upload': '#3b82f6',
            'border_card': '#e2e8f0',
            'border_task': '#f59e0b',
            'border_empty': '#93c5fd',
            'shadow_card': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
            'shadow_image': '0 4px 12px rgba(0, 0, 0, 0.1)',
        }
    else:  # dark
        colors = {
            'bg_primary': 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
            'bg_card': '#1e293b',
            'bg_sidebar': 'linear-gradient(180deg, #0f172a 0%, #1e293b 100%)',
            'bg_upload': 'linear-gradient(135deg, #1e293b 0%, #334155 100%)',
            'bg_radio': '#334155',
            'bg_expander': 'linear-gradient(135deg, #1e293b 0%, #334155 100%)',
            'bg_empty': 'linear-gradient(135deg, #1e293b 0%, #334155 100%)',
            'bg_task': 'linear-gradient(135deg, #422006 0%, #713f12 100%)',
            'text_primary': '#93c5fd',
            'text_secondary': '#e2e8f0',
            'text_muted': '#94a3b8',
            'text_sidebar': '#e2e8f0',
            'border_upload': '#3b82f6',
            'border_card': '#334155',
            'border_task': '#f59e0b',
            'border_empty': '#475569',
            'shadow_card': '0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)',
            'shadow_image': '0 4px 12px rgba(0, 0, 0, 0.3)',
        }
    
    return f"""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styling */
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Main Container */
    .main {{
        background: {colors['bg_primary']};
    }}
    
    /* Header Styling */
    h1 {{
        color: {colors['text_primary']};
        font-weight: 700;
        letter-spacing: -0.5px;
    }}
    
    h2, h3 {{
        color: {colors['text_secondary']};
        font-weight: 600;
    }}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background: {colors['bg_sidebar']};
    }}
    
    [data-testid="stSidebar"] * {{
        color: {colors['text_sidebar']} !important;
    }}
    
    [data-testid="stSidebar"] .stMarkdown {{
        color: rgba(255, 255, 255, 0.95) !important;
    }}
    
    /* Card Containers */
    .stContainer {{
        background: {colors['bg_card']};
        border-radius: 16px;
        padding: 24px;
        box-shadow: {colors['shadow_card']};
        margin-bottom: 20px;
    }}
    
    /* File Uploader */
    [data-testid="stFileUploader"] {{
        background: {colors['bg_upload']};
        border: 2px dashed {colors['border_upload']};
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }}
    
    [data-testid="stFileUploader"] label {{
        font-weight: 600;
        color: {colors['text_primary']};
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    }}
    
    /* Radio Buttons */
    .stRadio > label {{
        font-weight: 600;
        color: {colors['text_secondary']};
        font-size: 16px;
    }}
    
    .stRadio > div {{
        background: {colors['bg_radio']};
        padding: 12px;
        border-radius: 10px;
        border: 1px solid {colors['border_card']};
    }}
    
    /* Alerts & Info Boxes */
    .stAlert {{
        border-radius: 12px;
        border-left: 4px solid;
        padding: 16px;
        margin: 12px 0;
    }}
    
    [data-baseweb="notification"] {{
        border-radius: 12px;
        padding: 16px;
    }}
    
    /* Success Message */
    .element-container:has(.stSuccess) {{
        animation: slideIn 0.5s ease-out;
    }}
    
    @keyframes slideIn {{
        from {{
            opacity: 0;
            transform: translateY(-10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background: {colors['bg_expander']};
        border-radius: 10px;
        font-weight: 600;
        color: {colors['text_primary']};
    }}
    
    /* Download Button */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 10px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }}
    
    .stDownloadButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
    }}
    
    /* Task Items */
    .stWarning {{
        background: {colors['bg_task']};
        border-left: 4px solid {colors['border_task']};
        border-radius: 10px;
        padding: 12px 16px;
        margin: 8px 0;
    }}
    
    /* Image Preview */
    [data-testid="stImage"] {{
        border-radius: 12px;
        overflow: hidden;
        box-shadow: {colors['shadow_image']};
    }}
    
    /* Spinner */
    .stSpinner > div {{
        border-color: #3b82f6 !important;
    }}
    
    /* Feature Badge */
    .feature-badge {{
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 6px 12px;
        border-radius: 20px;
        margin: 4px 0;
        font-size: 14px;
    }}
    
    /* Paragraph text colors for dark mode */
    .main p {{
        color: {colors['text_muted']};
    }}
    
    .main strong {{
        color: {colors['text_secondary']};
    }}
    
    .main em {{
        color: {colors['text_muted']};
    }}
    
    /* Empty state styling */
    .empty-state {{
        text-align: center;
        padding: 60px 20px;
        background: {colors['bg_empty']};
        border-radius: 16px;
        border: 2px dashed {colors['border_empty']};
    }}
    
    .empty-state-title {{
        font-size: 18px;
        color: {colors['text_primary']};
        font-weight: 600;
        margin: 16px 0 8px 0;
    }}
    
    .empty-state-subtitle {{
        font-size: 14px;
        color: {colors['text_muted']};
        margin: 0;
    }}
    </style>
    """

# Determine active theme
if st.session_state.theme == 'auto':
    # For auto mode, we'll use media query to detect system preference
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Light mode (default) */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
    }
    
    h1 { color: #1e3a8a; font-weight: 700; letter-spacing: -0.5px; }
    h2, h3 { color: #334155; font-weight: 600; }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e40af 0%, #3b82f6 100%);
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    
    .stContainer {
        background: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 20px;
    }
    
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 2px dashed #3b82f6;
        border-radius: 12px;
        padding: 20px;
    }
    [data-testid="stFileUploader"] label { font-weight: 600; color: #1e40af; }
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    }
    
    .stRadio > label { font-weight: 600; color: #334155; }
    .stRadio > div {
        background: #f8fafc;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
    
    .stAlert { border-radius: 12px; padding: 16px; margin: 12px 0; }
    
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-radius: 10px;
        font-weight: 600;
        color: #1e40af;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 10px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 8px 0;
    }
    
    [data-testid="stImage"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .feature-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 6px 12px;
        border-radius: 20px;
        margin: 4px 0;
        font-size: 14px;
    }
    
    .main p { color: #64748b; }
    .main strong { color: #334155; }
    
    /* Dark mode (media query) */
    @media (prefers-color-scheme: dark) {
        .main { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); }
        h1 { color: #93c5fd; }
        h2, h3 { color: #e2e8f0; }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        }
        [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
        
        .stContainer {
            background: #1e293b;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
        }
        
        [data-testid="stFileUploader"] {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-color: #3b82f6;
        }
        [data-testid="stFileUploader"] label { color: #93c5fd; }
        
        .stRadio > label { color: #e2e8f0; }
        .stRadio > div {
            background: #334155;
            border-color: #334155;
        }
        
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: #93c5fd;
        }
        
        .stWarning {
            background: linear-gradient(135deg, #422006 0%, #713f12 100%);
            border-left-color: #f59e0b;
        }
        
        [data-testid="stImage"] {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        
        .main p { color: #94a3b8; }
        .main strong { color: #e2e8f0; }
    }
    </style>
    """, unsafe_allow_html=True)
else:
    # Apply chosen theme
    st.markdown(get_themed_css(st.session_state.theme), unsafe_allow_html=True)

# Theme Toggle in Sidebar
st.sidebar.markdown("### Tema Tampilan")
col_auto, col_light, col_dark = st.sidebar.columns(3)

with col_auto:
    if st.button("🔄", key="auto", use_container_width=True, help="Otomatis (Ikuti Device)", 
                 type="primary" if st.session_state.theme == 'auto' else "secondary"):
        st.session_state.theme = 'auto'
        st.rerun()

with col_light:
    if st.button("☀️", key="light", use_container_width=True, help="Mode Terang",
                 type="primary" if st.session_state.theme == 'light' else "secondary"):
        st.session_state.theme = 'light'
        st.rerun()

with col_dark:
    if st.button("🌙", key="dark", use_container_width=True, help="Mode Gelap",
                 type="primary" if st.session_state.theme == 'dark' else "secondary"):
        st.session_state.theme = 'dark'
        st.rerun()

# Show active theme
theme_emoji = {"auto": "🔄 Auto", "light": "☀️ Terang", "dark": "🌙 Gelap"}
st.sidebar.info(f"Aktif: **{theme_emoji[st.session_state.theme]}**")

st.sidebar.markdown("---")
st.sidebar.markdown("# Smart Board AI")
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='background: rgba(255,255,255,0.1); padding: 16px; border-radius: 12px; margin: 16px 0;'>
    <p style='font-size: 14px; line-height: 1.6; margin: 0;'>
        Ubah foto papan tulis atau catatan tangan menjadi data digital yang rapi dalam hitungan detik.
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### Fitur Unggulan")
st.sidebar.markdown("""
<div class='feature-badge'>Digitize Handwriting</div><br>
<div class='feature-badge'>Smart Summary</div><br>
<div class='feature-badge'>Auto To-Do List</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; padding: 12px; font-size: 12px; opacity: 0.8;'>
    Made with fiki for Students & Professionals
</div>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='font-size: 48px; margin-bottom: 8px;'>Lecture & Meeting Assistant</h1>
    <p style='font-size: 18px; max-width: 700px; margin: 0 auto; line-height: 1.6;'>
        Aplikasi produktivitas berbasis <strong>Computer Vision</strong> untuk Mahasiswa & Profesional.<br>
        <em>Upload foto papan tulis dosen atau coretan meeting, biarkan AI merapikannya.</em>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Load Service
@st.cache_resource
def get_analyzer():
    return VisionAnalyzer()

try:
    analyzer = get_analyzer()
except ValueError as e:
    st.error(f"{str(e)}")
    st.stop()

# Layout with Enhanced Containers
col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    with st.container():
        st.markdown("Upload Foto Catatan")
        st.markdown("<p style='font-size: 14px; margin-bottom: 16px;'>Format: JPG, PNG, JPEG (Maks 10MB)</p>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
        
        if uploaded_file:
            image = validate_image(uploaded_file)
            if image:
                st.markdown("<br>", unsafe_allow_html=True)
                st.image(image, caption="✓ Preview Foto", use_container_width=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("###Pilih Mode Pemrosesan")
                mode = st.radio(
                    "Output yang diinginkan:", 
                    ["Digitize Notes (Jadi Rangkuman Rapi)", 
                     "Action Items & Tasks (Cari Tugas/PR)"],
                    label_visibility="collapsed"
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                process_btn = st.button("Proses Sekarang", type="primary", use_container_width=True)

with col2:
    with st.container():
        st.markdown("### Hasil Cerdas")
        
        if uploaded_file and process_btn:
            with st.spinner("Sedang membaca tulisan tangan..."):
                if "Digitize" in mode:
                    # Mode Rangkuman
                    result = analyzer.digitize_notes(image)
                    st.success("Berhasil mendigitalkan catatan!")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander("Lihat Hasil Markdown", expanded=True):
                        st.markdown(result)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.download_button(
                        "Simpan sebagai .txt", 
                        result, 
                        file_name="catatan_rapi.txt",
                        use_container_width=True
                    )
                    
                else:
                    # Mode Action Items (JSON)
                    raw_json = analyzer.extract_action_items(image)
                    try:
                        clean_json = raw_json.replace("```json", "").replace("```", "")
                        data = json.loads(clean_json)
                        
                        # Tampilan Cantik untuk User
                        st.info(f"**Topik:** {data.get('topic', '-')}")
                        st.markdown(f"**Ringkasan:** {data.get('summary', '-')}")
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("### Daftar Tugas (To-Do)")
                        
                        if data.get('action_items'):
                            for idx, item in enumerate(data['action_items'], 1):
                                task = item.get('task')
                                who = item.get('assignee') or "Semua"
                                due = item.get('deadline') or "-"
                                st.warning(f"**#{idx}** ☐ **{task}**\n\n👤 Oleh: {who} | Deadline: {due}")
                        else:
                            st.info("ℹTidak ditemukan tugas khusus dalam catatan ini.")
                            
                    except:
                        st.error("Gagal parsing JSON, menampilkan raw text:")
                        st.code(raw_json, language="json")

        elif not uploaded_file:
            st.markdown("""
            <div class='empty-state'>
                <p style='font-size: 48px; margin: 0;'></p>
                <p class='empty-state-title'>Belum Ada Foto</p>
                <p class='empty-state-subtitle'>
                    Upload foto papan tulis atau catatan di panel kiri untuk memulai
                </p>
            </div>
            """, unsafe_allow_html=True)