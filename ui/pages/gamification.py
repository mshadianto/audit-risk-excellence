"""
Gamification Center Module for AURIX.
Achievements, badges, XP system, and team leaderboard.
"""

import streamlit as st
from datetime import datetime, timedelta

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer


def render():
    """Render the gamification center page."""
    t = get_current_theme()
    
    render_page_header(
        "🎮 Gamification Center",
        "Track achievements, earn badges, and compete with your team!"
    )
    
    # Initialize state
    if 'user_xp' not in st.session_state:
        st.session_state.user_xp = 2450
    if 'user_level' not in st.session_state:
        st.session_state.user_level = 12
    if 'daily_streak' not in st.session_state:
        st.session_state.daily_streak = 7
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏆 My Progress",
        "🎖️ Badges",
        "📊 Leaderboard",
        "🎯 Challenges",
        "🎁 Rewards"
    ])
    
    with tab1:
        _render_my_progress(t)
    
    with tab2:
        _render_badges(t)
    
    with tab3:
        _render_leaderboard(t)
    
    with tab4:
        _render_challenges(t)
    
    with tab5:
        _render_rewards(t)
    
    render_footer()


def _render_my_progress(t: dict):
    """Render user progress."""
    xp = st.session_state.user_xp
    level = st.session_state.user_level
    streak = st.session_state.daily_streak
    xp_for_next = level * 250
    xp_progress = (xp % xp_for_next) / xp_for_next * 100
    
    # Level card
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, {t['primary']}, {t['accent']});border-radius:16px;padding:1.5rem;color:white;margin-bottom:1.5rem;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div style="font-size:0.8rem;text-transform:uppercase;letter-spacing:0.1em;opacity:0.9;">Senior Auditor</div>
                <div style="font-size:2.5rem;font-weight:700;">Level {level}</div>
                <div style="font-size:0.9rem;opacity:0.85;">{xp:,} / {xp_for_next:,} XP to next level</div>
            </div>
            <div style="text-align:center;background:rgba(255,255,255,0.2);padding:1rem;border-radius:12px;">
                <div style="font-size:2rem;">🔥</div>
                <div style="font-size:1.5rem;font-weight:700;">{streak}</div>
                <div style="font-size:0.75rem;">Day Streak</div>
            </div>
        </div>
        <div style="margin-top:1rem;height:12px;background:rgba(255,255,255,0.3);border-radius:6px;overflow:hidden;">
            <div style="height:100%;width:{xp_progress:.0f}%;background:white;border-radius:6px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    st.markdown("#### 📊 Your Stats")
    cols = st.columns(4)
    stats = [
        ("🎯", "47", "Audits Completed", t['primary']),
        ("📋", "156", "Findings", t['accent']),
        ("⏱️", "1,248", "Hours Logged", t['success']),
        ("⭐", "94%", "Quality Score", t['warning']),
    ]
    for col, (icon, value, label, color) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;text-align:center;">
                <div style="font-size:1.5rem;margin-bottom:0.25rem;">{icon}</div>
                <div style="font-size:1.5rem;font-weight:700;color:{color};">{value}</div>
                <div style="font-size:0.75rem;color:{t['text_muted']};">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Weekly goals
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🎯 Weekly Goals")
    
    goals = [
        ("📋 Document Findings", 8, 12),
        ("📝 Complete Workpapers", 5, 8),
        ("👁️ Review Documents", 12, 15),
        ("🤖 AI Consultations", 20, 20),
    ]
    
    for label, current, target in goals:
        pct = min(current / target * 100, 100)
        is_complete = current >= target
        color = t['success'] if is_complete else t['primary']
        
        st.markdown(f"""
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:8px;padding:0.75rem;margin-bottom:0.5rem;">
            <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                <span style="color:{t['text']};">{label}</span>
                <span style="color:{color};font-weight:600;">{current}/{target} {'✅' if is_complete else ''}</span>
            </div>
            <div style="height:8px;background:{t['bg_secondary']};border-radius:4px;overflow:hidden;">
                <div style="height:100%;width:{pct}%;background:{color};border-radius:4px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_badges(t: dict):
    """Render badges collection."""
    st.markdown("#### 🎖️ Your Badges")
    
    badges = [
        ("🎯", "First Audit", "Complete your first audit", True, "Common", t['success']),
        ("🔍", "Risk Hunter", "Identify 10 high-risk findings", True, "Rare", t['primary']),
        ("⚡", "Speed Demon", "Complete audit ahead of schedule", True, "Rare", t['primary']),
        ("💯", "Perfectionist", "Achieve 100% quality score", True, "Epic", "#8b5cf6"),
        ("🤝", "Team Player", "Collaborate on 5 audits", True, "Common", t['success']),
        ("🤖", "AI Pioneer", "Use AI features 50 times", False, "Rare", t['primary']),
        ("📚", "Knowledge Seeker", "Read all regulations", False, "Epic", "#8b5cf6"),
        ("🏆", "Audit Champion", "Rank #1 for a month", False, "Legendary", t['warning']),
    ]
    
    # Earned badges
    st.markdown("**Earned Badges**")
    cols = st.columns(4)
    earned = [b for b in badges if b[3]]
    for i, (icon, name, desc, _, rarity, color) in enumerate(earned):
        with cols[i % 4]:
            st.markdown(f"""
            <div style="background:{t['card']};border:2px solid {color};border-radius:12px;padding:1rem;text-align:center;margin-bottom:0.75rem;">
                <div style="font-size:2rem;margin-bottom:0.5rem;">{icon}</div>
                <div style="font-weight:600;color:{t['text']};font-size:0.85rem;">{name}</div>
                <div style="font-size:0.65rem;color:{color};">{rarity}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Locked badges
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**🔒 Locked Badges**")
    cols = st.columns(4)
    locked = [b for b in badges if not b[3]]
    for i, (icon, name, desc, _, rarity, color) in enumerate(locked):
        with cols[i % 4]:
            st.markdown(f"""
            <div style="background:{t['bg_secondary']};border:1px dashed {t['border']};border-radius:12px;padding:1rem;text-align:center;opacity:0.6;margin-bottom:0.75rem;">
                <div style="font-size:2rem;margin-bottom:0.5rem;filter:grayscale(1);">{icon}</div>
                <div style="font-weight:600;color:{t['text_muted']};font-size:0.85rem;">{name}</div>
                <div style="font-size:0.65rem;color:{t['text_muted']};">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


def _render_leaderboard(t: dict):
    """Render team leaderboard."""
    st.markdown("#### 📊 Team Leaderboard")
    st.markdown(f"<p style='color:{t['text_muted']};font-size:0.85rem;'>This Month's Rankings</p>", unsafe_allow_html=True)
    
    leaderboard = [
        (1, "Ahmad R.", 3250, 14, "🥇", "+2"),
        (2, "Citra D.", 3100, 13, "🥈", "-1"),
        (3, "Budi S.", 2890, 13, "🥉", "+1"),
        (4, "You", 2450, 12, "👤", "0"),
        (5, "Dewi P.", 2200, 11, "", "-2"),
        (6, "Eko W.", 1950, 10, "", "+1"),
        (7, "Fitri A.", 1800, 10, "", "-1"),
        (8, "Gita H.", 1650, 9, "", "0"),
    ]
    
    for rank, name, xp, level, medal, change in leaderboard:
        is_you = name == "You"
        bg = t['primary'] + "20" if is_you else t['card']
        border = t['primary'] if is_you else t['border']
        
        change_color = t['success'] if change.startswith('+') else t['danger'] if change.startswith('-') else t['text_muted']
        change_icon = "↑" if change.startswith('+') else "↓" if change.startswith('-') else "→"
        
        st.markdown(f"""
        <div style="background:{bg};border:1px solid {border};border-radius:8px;padding:0.75rem;margin-bottom:0.5rem;">
            <div style="display:flex;align-items:center;gap:1rem;">
                <div style="width:30px;font-weight:700;color:{t['text']};font-size:1.1rem;">{medal or f'#{rank}'}</div>
                <div style="flex:1;">
                    <div style="font-weight:{'700' if is_you else '500'};color:{t['text']};">{name}</div>
                    <div style="font-size:0.75rem;color:{t['text_muted']};">Level {level}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-weight:600;color:{t['primary']};">{xp:,} XP</div>
                    <div style="font-size:0.75rem;color:{change_color};">{change_icon} {change.replace('+','').replace('-','')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_challenges(t: dict):
    """Render daily/weekly challenges."""
    st.markdown("#### 🎯 Active Challenges")
    
    # Daily
    st.markdown("**Daily Challenges** (Resets in 8h 23m)")
    daily = [
        ("Complete 2 workpapers", "50 XP", 1, 2, t['primary']),
        ("Log 4 hours", "30 XP", 3, 4, t['accent']),
        ("Use AI assistant", "20 XP", 1, 1, t['success']),
    ]
    
    for task, reward, current, target, color in daily:
        pct = current / target * 100
        done = current >= target
        st.markdown(f"""
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:8px;padding:0.75rem;margin-bottom:0.5rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="color:{t['text']};{'text-decoration:line-through;opacity:0.6;' if done else ''}">{task}</span>
                    <span style="color:{t['success'] if done else color};font-size:0.8rem;margin-left:0.5rem;">{reward} {'✅' if done else ''}</span>
                </div>
                <span style="font-size:0.85rem;color:{t['text_muted']};">{current}/{target}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Weekly
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Weekly Challenges** (Resets in 4 days)")
    weekly = [
        ("Complete 1 full audit", "200 XP", 0, 1, t['primary']),
        ("Document 5 findings", "150 XP", 3, 5, t['warning']),
        ("Achieve 90%+ quality", "100 XP", 1, 1, t['success']),
    ]
    
    for task, reward, current, target, color in weekly:
        pct = current / target * 100
        done = current >= target
        st.markdown(f"""
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:8px;padding:0.75rem;margin-bottom:0.5rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                <div>
                    <span style="color:{t['text']};{'text-decoration:line-through;opacity:0.6;' if done else ''}">{task}</span>
                    <span style="color:{t['success'] if done else color};font-size:0.8rem;margin-left:0.5rem;">{reward} {'✅' if done else ''}</span>
                </div>
                <span style="font-size:0.85rem;color:{t['text_muted']};">{current}/{target}</span>
            </div>
            <div style="height:6px;background:{t['bg_secondary']};border-radius:3px;overflow:hidden;">
                <div style="height:100%;width:{pct}%;background:{color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_rewards(t: dict):
    """Render rewards store."""
    st.markdown("#### 🎁 Rewards Store")
    st.markdown(f"<p style='color:{t['text_muted']};'>You have <strong style='color:{t['primary']};'>2,450 XP</strong> to spend</p>", unsafe_allow_html=True)
    
    rewards = [
        ("☕", "Coffee Voucher", "100 XP", "Grab a coffee on us!", True),
        ("🏖️", "Extra Leave Day", "5,000 XP", "+1 day annual leave", True),
        ("📚", "Training Budget", "2,000 XP", "Rp 500k training allowance", True),
        ("🍽️", "Lunch with CAE", "3,000 XP", "Exclusive lunch meeting", True),
        ("🎨", "Custom Profile Badge", "500 XP", "Personalize your profile", True),
        ("👑", "Custom Title", "1,000 XP", "Choose your display title", True),
        ("🚗", "Premium Parking", "2,500 XP", "1 month reserved parking", False),
        ("💻", "Tech Gadget", "10,000 XP", "Choose from selection", False),
    ]
    
    cols = st.columns(2)
    for i, (icon, name, cost, desc, available) in enumerate(rewards):
        with cols[i % 2]:
            can_afford = st.session_state.user_xp >= int(cost.replace(' XP', '').replace(',', ''))
            
            st.markdown(f"""
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-bottom:0.75rem;{'opacity:0.5;' if not available else ''}">
                <div style="display:flex;gap:1rem;align-items:center;">
                    <div style="font-size:2rem;">{icon}</div>
                    <div style="flex:1;">
                        <div style="font-weight:600;color:{t['text']};">{name}</div>
                        <div style="font-size:0.75rem;color:{t['text_muted']};">{desc}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-weight:600;color:{t['primary'] if can_afford else t['text_muted']};">{cost}</div>
                        <div style="font-size:0.7rem;color:{t['text_muted']};">{'Available' if available else 'Coming Soon'}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    render()
