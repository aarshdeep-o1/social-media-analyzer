import streamlit as st

def create_sidebar():
    # Toggle for theme
    if 'theme' not in st.session_state:
        st.session_state.theme = 'Dark'
        
    theme = st.sidebar.radio("🌓 Theme", ["Dark", "Light"], horizontal=True)
    st.session_state.theme = theme

    st.markdown("""
    <style>
    /* Make space for the logo above the navigation links */
    [data-testid="stSidebarNav"] {
        padding-top: 80px !important;
    }
    
    /* Fixed logo styling at the very top of the sidebar container */
    [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] .sidebar-logo {
        position: fixed;
        top: 25px;
        left: 25px;
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 999999;
    }
    
    /* Hide logo when sidebar is collapsed (if fixed becomes relative to viewport) */
    [data-testid="stSidebar"][aria-expanded="false"] .sidebar-logo {
        display: none !important;
    }
    
    .sidebar-logo .icon {
        font-size: 32px;
        line-height: 1;
    }
    
    .sidebar-logo .name {
        font-size: 20px;
        font-weight: 700;
        letter-spacing: 0.5px;
        line-height: 1;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add dark/light mode CSS overrides
    if theme == "Light":
        st.markdown("""
        <style>
        :root {
            --text-color: #111827 !important;
            --secondary-background-color: #ffffff !important;
            --background-color: #f9fafb !important;
        }
        html, body, [class*="css"] {
            color: var(--text-color) !important;
        }
        .stApp {
            background-color: var(--background-color) !important;
        }
        [data-testid="stSidebar"] { 
            background: linear-gradient(180deg, #f3f4f6, #e5e7eb) !important; 
        }
        [data-testid="stSidebar"] * { 
            color: #1f2937 !important; 
        }
        .hero { 
            background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 50%, #9ca3af 100%) !important; 
        }
        .hero h1, .hero p { color: #111827 !important; }
        .sidebar-logo .name { color: #1f2937 !important; }
        .page-header { background: linear-gradient(135deg, #e5e7eb, #d1d5db) !important; }
        .page-header h2, .page-header p { color: #111827 !important; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        :root {
            --text-color: #e0e0e0 !important;
            --secondary-background-color: #1e1e2d !important;
            --background-color: #0e0e17 !important;
        }
        html, body {
            color: var(--text-color) !important;
        }
        .stApp {
            background-color: var(--background-color) !important;
        }
        [data-testid="stSidebar"] { 
            background: linear-gradient(180deg, #0f0c29, #302b63, #24243e) !important; 
        }
        [data-testid="stSidebar"] * { 
            color: #e0e0e0 !important; 
        }
        .sidebar-logo .name { color: white !important; }
        </style>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div class='sidebar-logo'>
        <div class='icon'>📊</div>
        <div class='name'>InstaAnalytics</div>
    </div>
    """, unsafe_allow_html=True)
