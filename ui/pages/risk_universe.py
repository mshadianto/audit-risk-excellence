"""
Risk Universe Explorer Module for AURIX.
Interactive exploration of audit universe and risk landscape.
"""

import streamlit as st
from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer
from data.seeds import AUDIT_UNIVERSE, RISK_FACTORS


def render():
    """Render the risk universe explorer page."""
    t = get_current_theme()
    
    render_page_header(
        "🌐 Risk Universe Explorer",
        "Interactive exploration of your audit universe and risk landscape"
    )
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🌐 Universe Map",
        "🔗 Risk Network",
        "📊 Risk Matrix",
        "🎯 Focus Areas"
    ])
    
    with tab1:
        _render_universe_map(t)
    
    with tab2:
        _render_risk_network(t)
    
    with tab3:
        _render_risk_matrix(t)
    
    with tab4:
        _render_focus_areas(t)
    
    render_footer()


def _render_universe_map(t: dict):
    """Render audit universe map."""
    st.markdown("### 🌐 Audit Universe Map")
    st.markdown(f"<p style='color:{t['text_secondary']};'>Click on any domain to explore its audit areas and associated risks.</p>", unsafe_allow_html=True)
    
    # Domain cards in 2 rows of 3
    domains = [
        ("⚖️", "Governance", t['primary'], ["Board Oversight", "Committee Effectiveness", "Policy Framework", "Ethics & Culture"]),
        ("⚠️", "Risk Management", t['accent'], ["ERM Framework", "Risk Appetite", "Risk Reporting", "Stress Testing"]),
        ("💰", "Financial", t['success'], ["Financial Reporting", "Treasury", "Tax", "Budgeting"]),
        ("⚙️", "Operations", t['warning'], ["Branch Operations", "Customer Service", "Vendor Management", "Business Continuity"]),
        ("💻", "Technology", t['danger'], ["IT General Controls", "Cybersecurity", "Data Management", "System Development"]),
        ("🛡️", "AML/CFT", "#8b5cf6", ["CDD/KYC", "Transaction Monitoring", "Sanctions Screening", "STR Filing"]),
    ]
    
    # First row
    cols1 = st.columns(3)
    for i, (icon, name, color, areas) in enumerate(domains[:3]):
        with cols1[i]:
            _render_domain_card(t, icon, name, color, areas)
    
    # Second row
    cols2 = st.columns(3)
    for i, (icon, name, color, areas) in enumerate(domains[3:]):
        with cols2[i]:
            _render_domain_card(t, icon, name, color, areas)
    
    # Domain selector for details
    st.markdown("<br>", unsafe_allow_html=True)
    categories = list(AUDIT_UNIVERSE.keys())
    selected = st.selectbox("🔍 Select Domain to Explore", categories)
    
    if selected:
        areas = AUDIT_UNIVERSE.get(selected, [])
        st.markdown(f"#### 📋 {selected} - Audit Areas ({len(areas)} areas)")
        
        cols = st.columns(2)
        for i, area in enumerate(areas):
            with cols[i % 2]:
                risk_level = ["High", "Medium", "Low"][i % 3]
                risk_color = t['danger'] if risk_level == "High" else t['warning'] if risk_level == "Medium" else t['success']
                st.markdown(f"""
                <div style="background:{t['card']};border:1px solid {t['border']};border-radius:8px;padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:{t['text']};">📁 {area}</span>
                        <span style="background:{risk_color}20;color:{risk_color};padding:0.15rem 0.5rem;border-radius:4px;font-size:0.7rem;">{risk_level}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)


def _render_domain_card(t: dict, icon: str, name: str, color: str, areas: list):
    """Render a single domain card."""
    areas_text = " • ".join(areas[:3])
    if len(areas) > 3:
        areas_text += f" +{len(areas)-3} more"
    
    st.markdown(f"""
    <div style="background:{t['card']};border:2px solid {color};border-radius:16px;padding:1.25rem;text-align:center;min-height:180px;">
        <div style="width:60px;height:60px;background:{color}20;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 0.75rem;font-size:1.5rem;">
            {icon}
        </div>
        <div style="font-weight:700;color:{color};font-size:1.1rem;margin-bottom:0.5rem;">{name}</div>
        <div style="font-size:0.75rem;color:{t['text_muted']};">{areas_text}</div>
    </div>
    """, unsafe_allow_html=True)


def _render_risk_network(t: dict):
    """Render risk network visualization."""
    st.markdown("### 🔗 Risk Interconnections")
    st.markdown(f"<p style='color:{t['text_secondary']};'>How different risk types are connected and influence each other.</p>", unsafe_allow_html=True)
    
    risks = [
        ("Credit Risk", t['danger'], ["Market Risk", "Liquidity Risk", "Operational Risk"]),
        ("Market Risk", t['warning'], ["Credit Risk", "Liquidity Risk"]),
        ("Liquidity Risk", t['primary'], ["Credit Risk", "Market Risk", "Reputational Risk"]),
        ("Operational Risk", t['accent'], ["Cyber Risk", "Compliance Risk", "Reputational Risk"]),
        ("Cyber Risk", t['danger'], ["Operational Risk", "Reputational Risk"]),
        ("Compliance Risk", t['success'], ["Operational Risk", "Reputational Risk"]),
        ("Reputational Risk", "#8b5cf6", ["All Risks"]),
    ]
    
    for risk_name, color, connections in risks:
        conn_text = ", ".join(connections)
        st.markdown(f"""
        <div style="background:{t['card']};border-left:4px solid {color};border-radius:0 8px 8px 0;padding:1rem;margin-bottom:0.75rem;">
            <div style="font-weight:600;color:{color};margin-bottom:0.25rem;">{risk_name}</div>
            <div style="font-size:0.8rem;color:{t['text_muted']};">Connected to: {conn_text}</div>
        </div>
        """, unsafe_allow_html=True)


def _render_risk_matrix(t: dict):
    """Render 5x5 risk matrix."""
    st.markdown("### 📊 Risk Assessment Matrix")
    
    # Matrix header
    st.markdown(f"""
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.5rem;">
        <div style="text-align:center;margin-bottom:1rem;">
            <span style="font-weight:600;color:{t['text']};">IMPACT →</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Build matrix with columns
    impacts = ["Insignificant", "Minor", "Moderate", "Major", "Severe"]
    likelihoods = ["Almost Certain", "Likely", "Possible", "Unlikely", "Rare"]
    
    # Color mapping based on risk score
    def get_cell_color(l_idx, i_idx):
        score = (5 - l_idx) * (i_idx + 1)
        if score >= 15:
            return t['danger']
        elif score >= 10:
            return "#f97316"  # orange
        elif score >= 5:
            return t['warning']
        else:
            return t['success']
    
    st.markdown("**← LIKELIHOOD**")
    
    # Header row
    header_cols = st.columns([1.5] + [1]*5)
    header_cols[0].markdown("")
    for i, imp in enumerate(impacts):
        header_cols[i+1].markdown(f"<div style='text-align:center;font-size:0.7rem;color:{t['text_muted']};'>{imp}</div>", unsafe_allow_html=True)
    
    # Matrix rows
    for l_idx, likelihood in enumerate(likelihoods):
        row_cols = st.columns([1.5] + [1]*5)
        row_cols[0].markdown(f"<div style='font-size:0.75rem;color:{t['text']};padding-top:0.5rem;'>{likelihood}</div>", unsafe_allow_html=True)
        
        for i_idx in range(5):
            color = get_cell_color(l_idx, i_idx)
            score = (5 - l_idx) * (i_idx + 1)
            row_cols[i_idx+1].markdown(f"""
            <div style="background:{color};color:white;text-align:center;padding:0.5rem;border-radius:4px;font-weight:600;font-size:0.8rem;">
                {score}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Current risk positions
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📍 Current Risk Positions")
    
    current_risks = [
        ("Credit Risk - SME Portfolio", 4, 4, "Critical"),
        ("Cyber Security Threats", 4, 5, "Critical"),
        ("AML Compliance Gap", 3, 4, "High"),
        ("System Downtime", 3, 3, "Medium"),
        ("Staff Turnover", 2, 3, "Medium"),
        ("Vendor Dependency", 2, 2, "Low"),
    ]
    
    for name, likelihood, impact, rating in current_risks:
        rating_color = t['danger'] if rating == "Critical" else t['warning'] if rating == "High" else t['accent'] if rating == "Medium" else t['success']
        st.markdown(f"""
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:8px;padding:0.75rem;margin-bottom:0.5rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="color:{t['text']};">{name}</span>
                <div>
                    <span style="font-size:0.75rem;color:{t['text_muted']};margin-right:1rem;">L:{likelihood} × I:{impact}</span>
                    <span style="background:{rating_color}20;color:{rating_color};padding:0.2rem 0.6rem;border-radius:4px;font-size:0.7rem;font-weight:600;">{rating}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_focus_areas(t: dict):
    """Render AI-recommended focus areas."""
    st.markdown("### 🎯 AI-Recommended Focus Areas")
    st.markdown(f"<p style='color:{t['text_secondary']};'>Based on risk assessment, regulatory changes, and audit history.</p>", unsafe_allow_html=True)
    
    focus_areas = [
        ("Cybersecurity Controls Review", 95, "Q4 2024", "Q1 2025", "40 hours", "Critical vulnerabilities identified in penetration test"),
        ("AML Transaction Monitoring", 88, "Q3 2024", "Q1 2025", "60 hours", "New PPATK regulations effective January 2025"),
        ("Credit Risk - SME Segment", 85, "Q2 2024", "Q2 2025", "80 hours", "NPL ratio trending upward"),
        ("IT Change Management", 72, "Q1 2024", "Q2 2025", "35 hours", "Multiple system incidents in 2024"),
    ]
    
    for i, (area, score, last_audit, recommended, hours, reason) in enumerate(focus_areas):
        score_color = t['danger'] if score >= 90 else t['warning'] if score >= 80 else t['primary']
        
        st.markdown(f"""
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.25rem;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.75rem;">
                <div>
                    <span style="font-weight:600;color:{t['text']};font-size:1.1rem;">#{i+1} {area}</span>
                </div>
                <div style="background:{score_color};color:white;padding:0.35rem 0.75rem;border-radius:8px;font-weight:700;">
                    {score}
                </div>
            </div>
            <div style="font-size:0.85rem;color:{t['text_secondary']};margin-bottom:0.75rem;">
                💡 {reason}
            </div>
            <div style="display:flex;gap:1.5rem;font-size:0.8rem;color:{t['text_muted']};">
                <span>📅 Last: {last_audit}</span>
                <span>🎯 Recommended: {recommended}</span>
                <span>⏱️ Est: {hours}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    render()
