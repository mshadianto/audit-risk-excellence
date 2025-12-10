"""
Interactive Risk Universe Module for AURIX.
Stunning visual exploration of audit universe and risk relationships.
"""

import streamlit as st
from datetime import datetime
import random
import math

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer
from data.seeds import AUDIT_UNIVERSE, RISK_FACTORS


def render():
    """Render the risk universe page."""
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
    """Render interactive universe map."""
    st.markdown("### 🌐 Audit Universe Map")
    
    st.markdown(f'''
    <p style="color:{t['text_secondary']};">
    Click on any domain to explore its audit areas and associated risks.
    </p>
    ''', unsafe_allow_html=True)
    
    # Create interactive universe visualization
    categories = list(AUDIT_UNIVERSE.keys())
    colors = [t['primary'], t['accent'], t['success'], t['warning'], t['danger'], "#8b5cf6"]
    
    # Center hub
    center_html = f'''
    <div style="position:relative;width:100%;height:600px;background:radial-gradient(circle at center, {t['primary']}10 0%, {t['card']} 70%);border-radius:20px;border:1px solid {t['border']};overflow:hidden;">
        <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:120px;height:120px;background:linear-gradient(135deg, {t['primary']}, {t['accent']});border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 0 60px {t['primary']}50;z-index:10;">
            <div style="text-align:center;color:white;">
                <div style="font-size:1.5rem;">🏛️</div>
                <div style="font-size:0.7rem;font-weight:600;">AUDIT</div>
                <div style="font-size:0.6rem;">UNIVERSE</div>
            </div>
        </div>
        
        <div style="position:absolute;left:50%;top:15%;transform:translateX(-50%);">
            <div style="width:100px;height:100px;background:linear-gradient(135deg, {colors[0]}, {colors[0]}dd);border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 20px {colors[0]}40;cursor:pointer;">
                <div style="text-align:center;color:white;">
                    <div style="font-size:1.25rem;">⚖️</div>
                    <div style="font-size:0.55rem;font-weight:600;">Governance</div>
                </div>
            </div>
        </div>
        
        <div style="position:absolute;left:80%;top:30%;transform:translateX(-50%);">
            <div style="width:90px;height:90px;background:linear-gradient(135deg, {colors[1]}, {colors[1]}dd);border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 20px {colors[1]}40;cursor:pointer;">
                <div style="text-align:center;color:white;">
                    <div style="font-size:1.25rem;">⚠️</div>
                    <div style="font-size:0.55rem;font-weight:600;">Risk Mgmt</div>
                </div>
            </div>
        </div>
        
        <div style="position:absolute;left:85%;top:60%;transform:translateX(-50%);">
            <div style="width:95px;height:95px;background:linear-gradient(135deg, {colors[2]}, {colors[2]}dd);border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 20px {colors[2]}40;cursor:pointer;">
                <div style="text-align:center;color:white;">
                    <div style="font-size:1.25rem;">💰</div>
                    <div style="font-size:0.55rem;font-weight:600;">Financial</div>
                </div>
            </div>
        </div>
        
        <div style="position:absolute;left:50%;top:85%;transform:translateX(-50%);">
            <div style="width:100px;height:100px;background:linear-gradient(135deg, {colors[3]}, {colors[3]}dd);border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 20px {colors[3]}40;cursor:pointer;">
                <div style="text-align:center;color:white;">
                    <div style="font-size:1.25rem;">⚙️</div>
                    <div style="font-size:0.55rem;font-weight:600;">Operations</div>
                </div>
            </div>
        </div>
        
        <div style="position:absolute;left:15%;top:60%;transform:translateX(-50%);">
            <div style="width:95px;height:95px;background:linear-gradient(135deg, {colors[4]}, {colors[4]}dd);border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 20px {colors[4]}40;cursor:pointer;">
                <div style="text-align:center;color:white;">
                    <div style="font-size:1.25rem;">💻</div>
                    <div style="font-size:0.55rem;font-weight:600;">Technology</div>
                </div>
            </div>
        </div>
        
        <div style="position:absolute;left:20%;top:30%;transform:translateX(-50%);">
            <div style="width:90px;height:90px;background:linear-gradient(135deg, {colors[5]}, {colors[5]}dd);border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 20px {colors[5]}40;cursor:pointer;">
                <div style="text-align:center;color:white;">
                    <div style="font-size:1.25rem;">🛡️</div>
                    <div style="font-size:0.55rem;font-weight:600;">AML/CFT</div>
                </div>
            </div>
        </div>
    </div>
    '''
    st.markdown(center_html, unsafe_allow_html=True)
    
    # Category details
    st.markdown("<br>", unsafe_allow_html=True)
    
    selected_category = st.selectbox("Select Domain to Explore", options=categories)
    
    if selected_category:
        areas = AUDIT_UNIVERSE[selected_category]
        
        st.markdown(f"#### 📋 {selected_category} - Audit Areas")
        
        cols = st.columns(3)
        for i, area in enumerate(areas):
            risk_level = random.choice(["High", "Medium", "Low"])
            risk_color = {"High": t['danger'], "Medium": t['warning'], "Low": t['success']}[risk_level]
            last_audit = f"{random.randint(1, 18)} months ago"
            
            with cols[i % 3]:
                st.markdown(f'''
                <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-bottom:0.75rem;cursor:pointer;transition:all 0.2s;">
                    <div style="font-weight:600;color:{t['text']};margin-bottom:0.5rem;">{area}</div>
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="background:{risk_color}20;color:{risk_color};padding:0.2rem 0.5rem;border-radius:8px;font-size:0.7rem;font-weight:600;">{risk_level} Risk</span>
                        <span style="font-size:0.7rem;color:{t['text_muted']};">Last: {last_audit}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)


def _render_risk_network(t: dict):
    """Render risk relationship network."""
    st.markdown("### 🔗 Risk Relationship Network")
    
    st.markdown(f'''
    <p style="color:{t['text_secondary']};">
    Visualize how different risks are interconnected across your organization.
    </p>
    ''', unsafe_allow_html=True)
    
    # Network visualization using CSS/HTML
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:2rem;position:relative;height:500px;overflow:hidden;">
        
        <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:80px;height:80px;background:{t['danger']};border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-weight:600;font-size:0.7rem;text-align:center;box-shadow:0 0 30px {t['danger']}60;z-index:5;">
            Credit<br>Risk
        </div>
        
        
        <div style="position:absolute;left:25%;top:25%;width:60px;height:60px;background:{t['warning']};border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-size:0.6rem;text-align:center;box-shadow:0 0 20px {t['warning']}40;">
            Market<br>Risk
        </div>
        
        <div style="position:absolute;left:75%;top:25%;width:60px;height:60px;background:{t['primary']};border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-size:0.6rem;text-align:center;box-shadow:0 0 20px {t['primary']}40;">
            Liquidity<br>Risk
        </div>
        
        <div style="position:absolute;left:20%;top:60%;width:55px;height:55px;background:{t['accent']};border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-size:0.55rem;text-align:center;box-shadow:0 0 20px {t['accent']}40;">
            Op<br>Risk
        </div>
        
        <div style="position:absolute;left:80%;top:60%;width:55px;height:55px;background:{t['success']};border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-size:0.55rem;text-align:center;box-shadow:0 0 20px {t['success']}40;">
            Compliance<br>Risk
        </div>
        
        <div style="position:absolute;left:50%;top:15%;transform:translateX(-50%);width:50px;height:50px;background:#8b5cf6;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-size:0.55rem;text-align:center;box-shadow:0 0 20px #8b5cf640;">
            Cyber<br>Risk
        </div>
        
        <div style="position:absolute;left:50%;top:85%;transform:translateX(-50%);width:50px;height:50px;background:#ec4899;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-size:0.55rem;text-align:center;box-shadow:0 0 20px #ec489940;">
            Reputation<br>Risk
        </div>
        
        
        <svg style="position:absolute;width:100%;height:100%;top:0;left:0;pointer-events:none;">
            
            <line x1="50%" y1="50%" x2="27%" y2="28%" stroke="{t['warning']}" stroke-width="3" opacity="0.6"/>
            <line x1="50%" y1="50%" x2="73%" y2="28%" stroke="{t['primary']}" stroke-width="4" opacity="0.7"/>
            <line x1="50%" y1="50%" x2="23%" y2="62%" stroke="{t['accent']}" stroke-width="2" opacity="0.5"/>
            <line x1="50%" y1="50%" x2="77%" y2="62%" stroke="{t['success']}" stroke-width="2" opacity="0.5"/>
            <line x1="50%" y1="50%" x2="50%" y2="20%" stroke="#8b5cf6" stroke-width="2" opacity="0.5"/>
            <line x1="50%" y1="50%" x2="50%" y2="80%" stroke="#ec4899" stroke-width="3" opacity="0.6"/>
            
            
            <line x1="27%" y1="28%" x2="73%" y2="28%" stroke="{t['border']}" stroke-width="1" stroke-dasharray="4,4" opacity="0.4"/>
            <line x1="23%" y1="62%" x2="77%" y2="62%" stroke="{t['border']}" stroke-width="1" stroke-dasharray="4,4" opacity="0.4"/>
        </svg>
        
        
        <div style="position:absolute;bottom:1rem;right:1rem;background:{t['bg_secondary']};padding:0.75rem;border-radius:8px;font-size:0.7rem;">
            <div style="color:{t['text_muted']};margin-bottom:0.5rem;">Connection Strength</div>
            <div style="display:flex;gap:0.5rem;align-items:center;">
                <div style="width:30px;height:4px;background:{t['danger']};border-radius:2px;"></div>
                <span style="color:{t['text']};">Strong</span>
            </div>
            <div style="display:flex;gap:0.5rem;align-items:center;margin-top:0.25rem;">
                <div style="width:30px;height:2px;background:{t['text_muted']};border-radius:1px;"></div>
                <span style="color:{t['text']};">Moderate</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Risk correlation matrix
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📊 Risk Correlation Matrix")
    
    risks = ["Credit", "Market", "Liquidity", "Operational", "Compliance", "Cyber"]
    
    # Create correlation matrix display
    matrix_html = f'<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:0.8rem;">'
    matrix_html += f'<tr><th style="padding:0.5rem;background:{t["bg_secondary"]};color:{t["text"]};"></th>'
    
    for risk in risks:
        matrix_html += f'<th style="padding:0.5rem;background:{t["bg_secondary"]};color:{t["text"]};text-align:center;">{risk}</th>'
    
    matrix_html += '</tr>'
    
    correlations = [
        [1.0, 0.6, 0.8, 0.4, 0.5, 0.3],
        [0.6, 1.0, 0.7, 0.3, 0.2, 0.4],
        [0.8, 0.7, 1.0, 0.4, 0.3, 0.3],
        [0.4, 0.3, 0.4, 1.0, 0.6, 0.7],
        [0.5, 0.2, 0.3, 0.6, 1.0, 0.5],
        [0.3, 0.4, 0.3, 0.7, 0.5, 1.0],
    ]
    
    for i, risk in enumerate(risks):
        matrix_html += f'<tr><td style="padding:0.5rem;background:{t["bg_secondary"]};color:{t["text"]};font-weight:600;">{risk}</td>'
        
        for j, corr in enumerate(correlations[i]):
            if i == j:
                bg = t['primary']
                text_color = 'white'
            elif corr >= 0.7:
                bg = f'{t["danger"]}80'
                text_color = 'white'
            elif corr >= 0.5:
                bg = f'{t["warning"]}80'
                text_color = t['text']
            else:
                bg = f'{t["success"]}40'
                text_color = t['text']
            
            matrix_html += f'<td style="padding:0.5rem;background:{bg};color:{text_color};text-align:center;font-weight:600;">{corr:.1f}</td>'
        
        matrix_html += '</tr>'
    
    matrix_html += '</table></div>'
    
    st.markdown(matrix_html, unsafe_allow_html=True)


def _render_risk_matrix(t: dict):
    """Render interactive risk assessment matrix."""
    st.markdown("### 📊 Risk Assessment Matrix")
    
    # Create 5x5 risk matrix
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.5rem;">
        <div style="display:flex;">
            
            <div style="writing-mode:vertical-rl;text-orientation:mixed;transform:rotate(180deg);padding-right:1rem;font-weight:600;color:{t['text']};">
                LIKELIHOOD →
            </div>
            
            
            <div style="flex:1;">
                
                <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:4px;">
                    
                    <div style="background:{t['warning']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">Medium<br>🔶</div>
                    <div style="background:{t['danger']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">High<br>🔴</div>
                    <div style="background:{t['danger']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">High<br>🔴</div>
                    <div style="background:#7f1d1d;padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">Critical<br>⛔</div>
                    <div style="background:#7f1d1d;padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">Critical<br>⛔</div>
                    
                    
                    <div style="background:{t['success']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">Low<br>🟢</div>
                    <div style="background:{t['warning']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">Medium<br>🔶</div>
                    <div style="background:{t['danger']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">High<br>🔴</div>
                    <div style="background:{t['danger']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">High<br>🔴</div>
                    <div style="background:#7f1d1d;padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">Critical<br>⛔</div>
                    
                    
                    <div style="background:{t['success']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">Low<br>🟢</div>
                    <div style="background:{t['warning']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">Medium<br>🔶</div>
                    <div style="background:{t['warning']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">Medium<br>🔶</div>
                    <div style="background:{t['danger']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">High<br>🔴</div>
                    <div style="background:{t['danger']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">High<br>🔴</div>
                    
                    
                    <div style="background:#166534;padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">V.Low<br>✅</div>
                    <div style="background:{t['success']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">Low<br>🟢</div>
                    <div style="background:{t['warning']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">Medium<br>🔶</div>
                    <div style="background:{t['warning']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">Medium<br>🔶</div>
                    <div style="background:{t['danger']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">High<br>🔴</div>
                    
                    
                    <div style="background:#166534;padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">V.Low<br>✅</div>
                    <div style="background:#166534;padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">V.Low<br>✅</div>
                    <div style="background:{t['success']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">Low<br>🟢</div>
                    <div style="background:{t['warning']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">Medium<br>🔶</div>
                    <div style="background:{t['warning']};padding:1.5rem;text-align:center;border-radius:4px;color:white;font-size:0.7rem;font-weight:600;">Medium<br>🔶</div>
                </div>
                
                
                <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:4px;margin-top:0.5rem;">
                    <div style="text-align:center;font-size:0.7rem;color:{t['text_muted']};">Insignif.</div>
                    <div style="text-align:center;font-size:0.7rem;color:{t['text_muted']};">Minor</div>
                    <div style="text-align:center;font-size:0.7rem;color:{t['text_muted']};">Moderate</div>
                    <div style="text-align:center;font-size:0.7rem;color:{t['text_muted']};">Major</div>
                    <div style="text-align:center;font-size:0.7rem;color:{t['text_muted']};">Severe</div>
                </div>
                
                <div style="text-align:center;margin-top:0.5rem;font-weight:600;color:{t['text']};">
                    IMPACT →
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Risk items to plot
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🎯 Current Risk Positions")
    
    risks = [
        {"name": "Credit Concentration", "likelihood": 4, "impact": 5, "rating": "Critical"},
        {"name": "Cybersecurity Breach", "likelihood": 3, "impact": 5, "rating": "High"},
        {"name": "Regulatory Non-compliance", "likelihood": 3, "impact": 4, "rating": "High"},
        {"name": "Operational Failure", "likelihood": 2, "impact": 3, "rating": "Medium"},
        {"name": "Third-party Risk", "likelihood": 3, "impact": 3, "rating": "Medium"},
        {"name": "Staff Turnover", "likelihood": 4, "impact": 2, "rating": "Medium"},
    ]
    
    for risk in risks:
        rating_colors = {"Critical": t['danger'], "High": t['warning'], "Medium": t['accent'], "Low": t['success']}
        color = rating_colors.get(risk['rating'], t['text_muted'])
        
        st.markdown(f'''
        <div style="background:{t['card']};border-left:4px solid {color};border-radius:0 12px 12px 0;padding:1rem;margin-bottom:0.5rem;display:flex;align-items:center;justify-content:space-between;">
            <div>
                <div style="font-weight:600;color:{t['text']};">{risk['name']}</div>
                <div style="font-size:0.8rem;color:{t['text_muted']};">Likelihood: {risk['likelihood']}/5 • Impact: {risk['impact']}/5</div>
            </div>
            <div style="background:{color};color:white;padding:0.25rem 0.75rem;border-radius:20px;font-size:0.75rem;font-weight:600;">
                {risk['rating']}
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_focus_areas(t: dict):
    """Render audit focus areas based on risk."""
    st.markdown("### 🎯 Recommended Focus Areas")
    
    st.markdown(f'''
    <p style="color:{t['text_secondary']};">
    AI-recommended audit priorities based on risk assessment, regulatory requirements, and resource availability.
    </p>
    ''', unsafe_allow_html=True)
    
    # Priority matrix
    focus_areas = [
        {
            "name": "Credit Risk Management",
            "priority": "Critical",
            "reason": "NPL ratio trending up + regulatory scrutiny",
            "last_audit": "8 months ago",
            "recommended_timing": "Q1 2025",
            "estimated_hours": 240,
            "risk_score": 95
        },
        {
            "name": "Cybersecurity Controls",
            "priority": "High",
            "reason": "Recent industry breaches + new POJK requirements",
            "last_audit": "12 months ago",
            "recommended_timing": "Q1 2025",
            "estimated_hours": 200,
            "risk_score": 88
        },
        {
            "name": "AML Transaction Monitoring",
            "priority": "High",
            "reason": "Regulatory examination pending + alert backlog",
            "last_audit": "6 months ago",
            "recommended_timing": "Q1 2025",
            "estimated_hours": 160,
            "risk_score": 85
        },
        {
            "name": "Third-Party Risk Management",
            "priority": "Medium",
            "reason": "Increased outsourcing + vendor incidents",
            "last_audit": "14 months ago",
            "recommended_timing": "Q2 2025",
            "estimated_hours": 120,
            "risk_score": 72
        },
    ]
    
    for area in focus_areas:
        priority_colors = {"Critical": t['danger'], "High": t['warning'], "Medium": t['accent']}
        color = priority_colors.get(area['priority'], t['text_muted'])
        
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.5rem;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:1rem;">
                <div>
                    <div style="font-size:1.1rem;font-weight:700;color:{t['text']};">{area['name']}</div>
                    <div style="font-size:0.85rem;color:{t['text_secondary']};margin-top:0.25rem;">{area['reason']}</div>
                </div>
                <div style="background:{color};color:white;padding:0.35rem 1rem;border-radius:20px;font-weight:600;font-size:0.8rem;">
                    {area['priority']} Priority
                </div>
            </div>
            
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;">
                <div style="text-align:center;background:{t['bg_secondary']};padding:0.75rem;border-radius:8px;">
                    <div style="font-size:0.7rem;color:{t['text_muted']};">Risk Score</div>
                    <div style="font-size:1.25rem;font-weight:700;color:{color};">{area['risk_score']}</div>
                </div>
                <div style="text-align:center;background:{t['bg_secondary']};padding:0.75rem;border-radius:8px;">
                    <div style="font-size:0.7rem;color:{t['text_muted']};">Last Audit</div>
                    <div style="font-size:0.9rem;font-weight:600;color:{t['text']};">{area['last_audit']}</div>
                </div>
                <div style="text-align:center;background:{t['bg_secondary']};padding:0.75rem;border-radius:8px;">
                    <div style="font-size:0.7rem;color:{t['text_muted']};">Recommended</div>
                    <div style="font-size:0.9rem;font-weight:600;color:{t['primary']};">{area['recommended_timing']}</div>
                </div>
                <div style="text-align:center;background:{t['bg_secondary']};padding:0.75rem;border-radius:8px;">
                    <div style="font-size:0.7rem;color:{t['text_muted']};">Est. Hours</div>
                    <div style="font-size:0.9rem;font-weight:600;color:{t['text']};">{area['estimated_hours']}h</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
