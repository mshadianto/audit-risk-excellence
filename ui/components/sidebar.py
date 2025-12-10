"""
Sidebar Component for AURIX.
Handles navigation, theme toggle, and stats display.
"""

import streamlit as st
from typing import List, Dict
from ui.styles.css_builder import get_current_theme
from ui.components.badges import render_badge


def get_logo_svg() -> str:
    """Generate AURIX logo SVG."""
    t = get_current_theme()
    fill = t['primary']
    
    return f'''<svg width="32" height="32" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
<path d="M50 8 L90 25 L90 55 C90 78 70 92 50 98 C30 92 10 78 10 55 L10 25 Z" fill="{fill}" opacity="0.9"/>
<circle cx="50" cy="48" r="8" fill="white" opacity="0.9"/>
<circle cx="35" cy="33" r="4" fill="white" opacity="0.7"/>
<circle cx="65" cy="33" r="4" fill="white" opacity="0.7"/>
<circle cx="30" cy="55" r="4" fill="white" opacity="0.7"/>
<circle cx="70" cy="55" r="4" fill="white" opacity="0.7"/>
<circle cx="50" cy="72" r="4" fill="white" opacity="0.7"/>
<line x1="50" y1="48" x2="35" y2="33" stroke="white" stroke-width="2" opacity="0.5"/>
<line x1="50" y1="48" x2="65" y2="33" stroke="white" stroke-width="2" opacity="0.5"/>
<line x1="50" y1="48" x2="30" y2="55" stroke="white" stroke-width="2" opacity="0.5"/>
<line x1="50" y1="48" x2="70" y2="55" stroke="white" stroke-width="2" opacity="0.5"/>
<line x1="50" y1="48" x2="50" y2="72" stroke="white" stroke-width="2" opacity="0.5"/>
</svg>'''


def render_logo():
    """Render AURIX logo with branding."""
    t = get_current_theme()
    
    st.markdown(f'''
    <div class="logo-container">
        {get_logo_svg()}
        <div>
            <div class="logo-text">AURIX</div>
            <div class="logo-tagline">v4.0 Enterprise</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_theme_toggle():
    """Render theme toggle buttons."""
    st.markdown('<div class="section-title">Theme</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("☀️ Light", use_container_width=True, key="light_btn"):
            st.session_state.theme = 'light'
            st.rerun()
    
    with col2:
        if st.button("🌙 Dark", use_container_width=True, key="dark_btn"):
            st.session_state.theme = 'dark'
            st.rerun()


def render_navigation(routes: List[str], categories: Dict[str, List[str]]) -> str:
    """Render navigation menu and return selected page."""
    st.markdown('<div class="section-title">Navigation</div>', unsafe_allow_html=True)
    
    # Flatten routes maintaining order
    selected_page = st.radio(
        label="Navigation Menu",
        options=routes,
        label_visibility="collapsed",
        key="nav_menu"
    )
    
    return selected_page


def render_session_stats():
    """Render session statistics."""
    t = get_current_theme()
    
    st.markdown('<div class="section-title">Statistics</div>', unsafe_allow_html=True)
    
    # Get stats from session state
    doc_count = len(st.session_state.get('documents', []))
    finding_count = len(st.session_state.get('findings', []))
    active_rules = len([
        r for r in st.session_state.get('continuous_audit_rules', [])
        if r.get('active', False)
    ])
    
    st.markdown(f'''
    <div class="pro-card" style="padding:1rem;">
        <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
            <span style="color:{t['text_muted']} !important;font-size:0.8rem;">Documents</span>
            <span style="color:{t['text']} !important;font-weight:600;">{doc_count}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
            <span style="color:{t['text_muted']} !important;font-size:0.8rem;">Findings</span>
            <span style="color:{t['text']} !important;font-weight:600;">{finding_count}</span>
        </div>
        <div style="display:flex;justify-content:space-between;">
            <span style="color:{t['text_muted']} !important;font-size:0.8rem;">CA Rules</span>
            <span style="color:{t['text']} !important;font-weight:600;">{active_rules}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_visitor_stats(stats: dict = None):
    """Render visitor statistics."""
    t = get_current_theme()
    
    st.markdown('<div class="section-title">👥 Visitor Stats</div>', unsafe_allow_html=True)
    
    if stats is None:
        # Use mock/session data
        stats = {
            'today_visits': st.session_state.get('page_views', 0),
            'total_visits': 100,
            'unique_visitors': 50,
        }
    
    st.markdown(f'''
    <div class="pro-card" style="padding:1rem;">
        <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
            <span style="color:{t['text_muted']} !important;font-size:0.8rem;">Today Visits</span>
            <span style="color:{t['accent']} !important;font-weight:600;">{stats.get('today_visits', 0)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
            <span style="color:{t['text_muted']} !important;font-size:0.8rem;">Total Visits</span>
            <span style="color:{t['text']} !important;font-weight:600;">{stats.get('total_visits', 0):,}</span>
        </div>
        <div style="display:flex;justify-content:space-between;">
            <span style="color:{t['text_muted']} !important;font-size:0.8rem;">Your Views</span>
            <span style="color:{t['success']} !important;font-weight:600;">{st.session_state.get('page_views', 0)}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_llm_config():
    """Render LLM configuration section."""
    from app.constants import LLM_PROVIDER_INFO
    
    st.markdown('<div class="section-title">AI Provider</div>', unsafe_allow_html=True)
    
    providers = list(LLM_PROVIDER_INFO.keys())
    
    provider = st.selectbox(
        "Provider",
        providers,
        key="llm_provider",
        label_visibility="collapsed",
        format_func=lambda x: f"{LLM_PROVIDER_INFO[x]['name']} {'🆓' if LLM_PROVIDER_INFO[x]['free'] else '💎'}"
    )
    
    info = LLM_PROVIDER_INFO.get(provider, {})
    
    # Show API key input if needed
    if provider not in ['mock', 'ollama']:
        st.text_input(
            "API Key",
            type="password",
            key="api_key_input",
            label_visibility="collapsed",
            placeholder="Enter API key..."
        )
    
    # Show helper text
    if info.get('url'):
        st.markdown(
            f"<small><a href='{info['url']}' target='_blank'>Get API Key →</a></small>",
            unsafe_allow_html=True
        )


def render_sidebar(routes: List[str], categories: Dict[str, List[str]]) -> str:
    """
    Render complete sidebar.
    
    Args:
        routes: List of page names
        categories: Dict mapping category names to page lists
    
    Returns:
        Selected page name
    """
    with st.sidebar:
        # Logo
        render_logo()
        
        # Theme Toggle
        render_theme_toggle()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Navigation
        selected_page = render_navigation(routes, categories)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Stats
        render_session_stats()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Visitor Stats
        render_visitor_stats()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # LLM Config
        render_llm_config()
    
    return selected_page
