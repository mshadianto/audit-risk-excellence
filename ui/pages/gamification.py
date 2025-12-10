"""
Gamification Center Module for AURIX.
Achievements, badges, XP system, and team leaderboard.
Makes audit work engaging and fun!
"""

import streamlit as st
from datetime import datetime, timedelta
import random
import math

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer


def render():
    """Render the gamification center page."""
    t = get_current_theme()
    
    render_page_header(
        "🎮 Gamification Center",
        "Track achievements, earn badges, and compete with your team!"
    )
    
    # Initialize gamification state
    _init_gamification_state()
    
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


def _init_gamification_state():
    """Initialize gamification session state."""
    if 'user_xp' not in st.session_state:
        st.session_state.user_xp = 2450
    if 'user_level' not in st.session_state:
        st.session_state.user_level = 12
    if 'user_badges' not in st.session_state:
        st.session_state.user_badges = ['first_audit', 'risk_hunter', 'speed_demon', 'perfectionist', 'team_player']
    if 'daily_streak' not in st.session_state:
        st.session_state.daily_streak = 7
    if 'weekly_goals' not in st.session_state:
        st.session_state.weekly_goals = {'findings': 8, 'workpapers': 5, 'reviews': 12}


def _render_my_progress(t: dict):
    """Render user progress dashboard."""
    
    # Level and XP Header
    xp = st.session_state.user_xp
    level = st.session_state.user_level
    xp_for_next = level * 250
    xp_progress = (xp % 250) / 250 * 100
    
    st.markdown(f'''
    <div style="background:linear-gradient(135deg, {t['primary']}, {t['accent']});border-radius:20px;padding:2rem;margin-bottom:2rem;color:white;position:relative;overflow:hidden;">
        <div style="position:absolute;top:-50px;right:-50px;width:200px;height:200px;background:rgba(255,255,255,0.1);border-radius:50%;"></div>
        <div style="position:absolute;bottom:-30px;left:-30px;width:150px;height:150px;background:rgba(255,255,255,0.05);border-radius:50%;"></div>
        
        <div style="display:flex;align-items:center;gap:2rem;position:relative;z-index:1;">
            <div style="text-align:center;">
                <div style="width:100px;height:100px;background:rgba(255,255,255,0.2);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:2.5rem;border:4px solid rgba(255,255,255,0.5);">
                    👨‍💼
                </div>
            </div>
            <div style="flex:1;">
                <div style="font-size:0.9rem;opacity:0.9;text-transform:uppercase;letter-spacing:0.1em;">Senior Auditor</div>
                <div style="font-size:2rem;font-weight:700;margin:0.25rem 0;">Level {level}</div>
                <div style="font-size:0.9rem;opacity:0.8;margin-bottom:0.75rem;">{xp:,} / {xp_for_next:,} XP to next level</div>
                <div style="height:12px;background:rgba(255,255,255,0.2);border-radius:6px;overflow:hidden;">
                    <div style="width:{xp_progress}%;height:100%;background:rgba(255,255,255,0.9);border-radius:6px;transition:width 0.5s;"></div>
                </div>
            </div>
            <div style="text-align:center;padding:1rem;background:rgba(255,255,255,0.15);border-radius:12px;">
                <div style="font-size:2.5rem;">🔥</div>
                <div style="font-size:1.5rem;font-weight:700;">{st.session_state.daily_streak}</div>
                <div style="font-size:0.75rem;opacity:0.9;">Day Streak</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Stats Grid
    stats = [
        ("🎯", "Audits Completed", "47", "+3 this week", t['success']),
        ("📋", "Findings Documented", "156", "+12 this week", t['primary']),
        ("⏱️", "Hours Logged", "1,248", "+42 this week", t['accent']),
        ("⭐", "Quality Score", "94%", "+2% vs last month", t['warning']),
    ]
    
    cols = st.columns(4)
    for col, (icon, label, value, change, color) in zip(cols, stats):
        with col:
            st.markdown(f'''
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.25rem;text-align:center;transition:transform 0.2s;cursor:pointer;" 
                 
                >
                <div style="font-size:2rem;margin-bottom:0.5rem;">{icon}</div>
                <div style="font-size:1.75rem;font-weight:700;color:{color};">{value}</div>
                <div style="font-size:0.8rem;color:{t['text_muted']};margin-bottom:0.25rem;">{label}</div>
                <div style="font-size:0.7rem;color:{t['success']};">📈 {change}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Weekly Goals
    st.markdown("### 🎯 Weekly Goals")
    
    goals = [
        ("Document Findings", 8, 12, "📋"),
        ("Complete Workpapers", 5, 8, "📝"),
        ("Review Documents", 12, 15, "👁️"),
        ("AI Consultations", 20, 20, "🤖"),
    ]
    
    for label, current, target, icon in goals:
        progress = min(current / target * 100, 100)
        is_complete = current >= target
        
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-bottom:0.75rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                <span style="color:{t['text']};font-weight:500;">{icon} {label}</span>
                <span style="color:{t['success'] if is_complete else t['text_muted']};font-weight:600;">
                    {current}/{target} {'✅' if is_complete else ''}
                </span>
            </div>
            <div style="height:8px;background:{t['border']};border-radius:4px;overflow:hidden;">
                <div style="width:{progress}%;height:100%;background:{'linear-gradient(90deg, ' + t['success'] + ', #10b981)' if is_complete else t['primary']};border-radius:4px;transition:width 0.5s;"></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Recent Achievements
    st.markdown("### 🏅 Recent Achievements")
    
    achievements = [
        ("🎯", "Perfect Week", "Completed all weekly goals", "2 hours ago", "+100 XP"),
        ("🔥", "7 Day Streak", "Logged in 7 consecutive days", "Today", "+50 XP"),
        ("📋", "Finding Machine", "Documented 10 findings in one day", "Yesterday", "+75 XP"),
        ("🤖", "AI Explorer", "Used all AI features", "3 days ago", "+50 XP"),
    ]
    
    for icon, title, desc, time, xp in achievements:
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-bottom:0.5rem;display:flex;align-items:center;gap:1rem;">
            <div style="width:50px;height:50px;background:linear-gradient(135deg, {t['primary']}20, {t['accent']}20);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;">
                {icon}
            </div>
            <div style="flex:1;">
                <div style="font-weight:600;color:{t['text']};">{title}</div>
                <div style="font-size:0.8rem;color:{t['text_muted']};">{desc}</div>
            </div>
            <div style="text-align:right;">
                <div style="color:{t['success']};font-weight:600;font-size:0.85rem;">{xp}</div>
                <div style="font-size:0.7rem;color:{t['text_muted']};">{time}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_badges(t: dict):
    """Render badges collection."""
    st.markdown("### 🎖️ Badge Collection")
    
    # Badge categories
    all_badges = {
        "Audit Excellence": [
            {"id": "first_audit", "name": "First Blood", "desc": "Complete your first audit", "icon": "🎯", "rarity": "common", "earned": True},
            {"id": "audit_master", "name": "Audit Master", "desc": "Complete 50 audits", "icon": "👑", "rarity": "legendary", "earned": False, "progress": 47},
            {"id": "perfectionist", "name": "Perfectionist", "desc": "Zero rework on 10 consecutive audits", "icon": "💎", "rarity": "epic", "earned": True},
            {"id": "speed_demon", "name": "Speed Demon", "desc": "Complete audit 20% under budget", "icon": "⚡", "rarity": "rare", "earned": True},
        ],
        "Risk Hunter": [
            {"id": "risk_hunter", "name": "Risk Hunter", "desc": "Identify 100 risks", "icon": "🎯", "rarity": "rare", "earned": True},
            {"id": "critical_finder", "name": "Critical Finder", "desc": "Find 10 critical risks", "icon": "🔴", "rarity": "epic", "earned": False, "progress": 7},
            {"id": "risk_prophet", "name": "Risk Prophet", "desc": "Predict risk that materialized", "icon": "🔮", "rarity": "legendary", "earned": False},
        ],
        "Team Player": [
            {"id": "team_player", "name": "Team Player", "desc": "Collaborate on 20 audits", "icon": "🤝", "rarity": "common", "earned": True},
            {"id": "mentor", "name": "Mentor", "desc": "Review 50 junior workpapers", "icon": "👨‍🏫", "rarity": "rare", "earned": False, "progress": 32},
            {"id": "knowledge_sharer", "name": "Knowledge Sharer", "desc": "Create 10 templates used by team", "icon": "📚", "rarity": "epic", "earned": False},
        ],
        "AI Pioneer": [
            {"id": "ai_curious", "name": "AI Curious", "desc": "First AI-assisted audit", "icon": "🤖", "rarity": "common", "earned": True},
            {"id": "prompt_master", "name": "Prompt Master", "desc": "Create 50 effective prompts", "icon": "✨", "rarity": "rare", "earned": False, "progress": 28},
            {"id": "ai_innovator", "name": "AI Innovator", "desc": "Discover new AI use case", "icon": "💡", "rarity": "legendary", "earned": False},
        ],
    }
    
    rarity_colors = {
        "common": ("#9ca3af", "Common"),
        "rare": ("#3b82f6", "Rare"),
        "epic": ("#8b5cf6", "Epic"),
        "legendary": ("#f59e0b", "Legendary"),
    }
    
    # Stats
    total_badges = sum(len(badges) for badges in all_badges.values())
    earned_badges = sum(1 for badges in all_badges.values() for b in badges if b.get('earned'))
    
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.5rem;margin-bottom:2rem;text-align:center;">
        <div style="font-size:3rem;margin-bottom:0.5rem;">🏆</div>
        <div style="font-size:2rem;font-weight:700;color:{t['text']};">{earned_badges} / {total_badges}</div>
        <div style="color:{t['text_muted']};">Badges Collected</div>
        <div style="margin-top:1rem;display:flex;justify-content:center;gap:1rem;">
            <span style="font-size:0.8rem;color:#9ca3af;">● 3 Common</span>
            <span style="font-size:0.8rem;color:#3b82f6;">● 2 Rare</span>
            <span style="font-size:0.8rem;color:#8b5cf6;">● 1 Epic</span>
            <span style="font-size:0.8rem;color:#f59e0b;">● 0 Legendary</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Badge grid by category
    for category, badges in all_badges.items():
        st.markdown(f"#### {category}")
        
        cols = st.columns(4)
        for i, badge in enumerate(badges):
            color, rarity_name = rarity_colors[badge['rarity']]
            earned = badge.get('earned', False)
            progress = badge.get('progress', 0)
            
            with cols[i % 4]:
                if earned:
                    st.markdown(f'''
                    <div style="background:linear-gradient(135deg, {color}15, {color}25);border:2px solid {color};border-radius:16px;padding:1.25rem;text-align:center;margin-bottom:1rem;">
                        <div style="font-size:2.5rem;margin-bottom:0.5rem;">{badge['icon']}</div>
                        <div style="font-weight:600;color:{t['text']};font-size:0.9rem;">{badge['name']}</div>
                        <div style="font-size:0.7rem;color:{t['text_muted']};margin:0.25rem 0;">{badge['desc']}</div>
                        <div style="font-size:0.65rem;color:{color};font-weight:600;text-transform:uppercase;">✓ {rarity_name}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                    <div style="background:{t['card']};border:2px dashed {t['border']};border-radius:16px;padding:1.25rem;text-align:center;margin-bottom:1rem;opacity:0.6;">
                        <div style="font-size:2.5rem;margin-bottom:0.5rem;filter:grayscale(100%);">🔒</div>
                        <div style="font-weight:600;color:{t['text_muted']};font-size:0.9rem;">{badge['name']}</div>
                        <div style="font-size:0.7rem;color:{t['text_muted']};margin:0.25rem 0;">{badge['desc']}</div>
                        {f'<div style="font-size:0.65rem;color:{color};">Progress: {progress}%</div>' if progress else ''}
                    </div>
                    ''', unsafe_allow_html=True)


def _render_leaderboard(t: dict):
    """Render team leaderboard."""
    st.markdown("### 📊 Team Leaderboard")
    
    # Time filter
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        period = st.selectbox("Period", ["This Week", "This Month", "This Quarter", "All Time"], label_visibility="collapsed")
    with col2:
        metric = st.selectbox("Metric", ["XP Points", "Findings", "Audits", "Quality Score"], label_visibility="collapsed")
    
    # Leaderboard data
    leaderboard = [
        {"rank": 1, "name": "Andi Pratama", "role": "Senior Auditor", "xp": 3250, "level": 15, "avatar": "👨‍💼", "trend": "up", "badges": 12},
        {"rank": 2, "name": "Anda (You)", "role": "Senior Auditor", "xp": 2450, "level": 12, "avatar": "🧑‍💻", "trend": "up", "badges": 8, "is_you": True},
        {"rank": 3, "name": "Siti Rahayu", "role": "Audit Manager", "xp": 2380, "level": 11, "avatar": "👩‍💼", "trend": "down", "badges": 10},
        {"rank": 4, "name": "Budi Santoso", "role": "Staff Auditor", "xp": 2100, "level": 10, "avatar": "👨‍🔬", "trend": "up", "badges": 7},
        {"rank": 5, "name": "Dewi Lestari", "role": "IT Auditor", "xp": 1950, "level": 9, "avatar": "👩‍💻", "trend": "same", "badges": 6},
        {"rank": 6, "name": "Rizky Aditya", "role": "Staff Auditor", "xp": 1820, "level": 8, "avatar": "🧔", "trend": "up", "badges": 5},
        {"rank": 7, "name": "Maya Putri", "role": "Junior Auditor", "xp": 1650, "level": 7, "avatar": "👩‍🎓", "trend": "up", "badges": 4},
        {"rank": 8, "name": "Hendra Wijaya", "role": "Junior Auditor", "xp": 1420, "level": 6, "avatar": "👨‍🎓", "trend": "down", "badges": 3},
    ]
    
    # Top 3 podium
    st.markdown("<br>", unsafe_allow_html=True)
    
    cols = st.columns([1, 1.2, 1])
    
    # Second place
    with cols[0]:
        p = leaderboard[1]
        st.markdown(f'''
        <div style="text-align:center;margin-top:2rem;">
            <div style="font-size:3rem;">{p['avatar']}</div>
            <div style="background:linear-gradient(135deg, #94a3b8, #64748b);color:white;padding:0.25rem 0.75rem;border-radius:20px;display:inline-block;font-size:0.8rem;margin:0.5rem 0;">
                🥈 2nd
            </div>
            <div style="font-weight:600;color:{t['text']};">{p['name']}</div>
            <div style="font-size:0.8rem;color:{t['text_muted']};">{p['xp']:,} XP</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # First place
    with cols[1]:
        p = leaderboard[0]
        st.markdown(f'''
        <div style="text-align:center;">
            <div style="font-size:4rem;">{p['avatar']}</div>
            <div style="background:linear-gradient(135deg, #fbbf24, #f59e0b);color:white;padding:0.5rem 1rem;border-radius:20px;display:inline-block;font-weight:600;margin:0.5rem 0;">
                👑 1st Place
            </div>
            <div style="font-weight:700;color:{t['text']};font-size:1.1rem;">{p['name']}</div>
            <div style="font-size:0.9rem;color:{t['primary']};font-weight:600;">{p['xp']:,} XP</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Third place
    with cols[2]:
        p = leaderboard[2]
        st.markdown(f'''
        <div style="text-align:center;margin-top:3rem;">
            <div style="font-size:2.5rem;">{p['avatar']}</div>
            <div style="background:linear-gradient(135deg, #cd7f32, #b8860b);color:white;padding:0.25rem 0.75rem;border-radius:20px;display:inline-block;font-size:0.8rem;margin:0.5rem 0;">
                🥉 3rd
            </div>
            <div style="font-weight:600;color:{t['text']};">{p['name']}</div>
            <div style="font-size:0.8rem;color:{t['text_muted']};">{p['xp']:,} XP</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Full leaderboard table
    st.markdown("#### Full Rankings")
    
    for p in leaderboard:
        is_you = p.get('is_you', False)
        trend_icon = "📈" if p['trend'] == 'up' else ("📉" if p['trend'] == 'down' else "➡️")
        
        bg = f"linear-gradient(90deg, {t['primary']}15, {t['card']})" if is_you else t['card']
        border = t['primary'] if is_you else t['border']
        
        st.markdown(f'''
        <div style="background:{bg};border:{'2px' if is_you else '1px'} solid {border};border-radius:12px;padding:1rem;margin-bottom:0.5rem;display:flex;align-items:center;gap:1rem;">
            <div style="width:40px;text-align:center;">
                <span style="font-size:1.25rem;font-weight:700;color:{t['text']};">#{p['rank']}</span>
            </div>
            <div style="font-size:2rem;">{p['avatar']}</div>
            <div style="flex:1;">
                <div style="font-weight:600;color:{t['text']};">{p['name']} {' 👈' if is_you else ''}</div>
                <div style="font-size:0.8rem;color:{t['text_muted']};">{p['role']} • Level {p['level']}</div>
            </div>
            <div style="text-align:center;padding:0 1rem;">
                <div style="font-size:0.7rem;color:{t['text_muted']};">Badges</div>
                <div style="font-weight:600;color:{t['accent']};">🎖️ {p['badges']}</div>
            </div>
            <div style="text-align:right;min-width:100px;">
                <div style="font-weight:700;color:{t['primary']};">{p['xp']:,} XP</div>
                <div style="font-size:0.75rem;color:{t['text_muted']};">{trend_icon} {p['trend']}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_challenges(t: dict):
    """Render active challenges."""
    st.markdown("### 🎯 Active Challenges")
    
    # Daily challenges
    st.markdown("#### Daily Challenges")
    
    daily = [
        {"name": "Early Bird", "desc": "Log in before 8 AM", "reward": "25 XP", "progress": 100, "icon": "🌅", "expires": "Completed!"},
        {"name": "Document Master", "desc": "Upload 3 documents", "reward": "30 XP", "progress": 66, "icon": "📁", "expires": "8h left"},
        {"name": "AI Apprentice", "desc": "Use AI Chat 5 times", "reward": "40 XP", "progress": 40, "icon": "🤖", "expires": "8h left"},
    ]
    
    for c in daily:
        is_complete = c['progress'] >= 100
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['success'] if is_complete else t['border']};border-radius:12px;padding:1.25rem;margin-bottom:0.75rem;">
            <div style="display:flex;align-items:center;gap:1rem;">
                <div style="font-size:2rem;">{c['icon']}</div>
                <div style="flex:1;">
                    <div style="font-weight:600;color:{t['text']};">{c['name']} {'✅' if is_complete else ''}</div>
                    <div style="font-size:0.8rem;color:{t['text_muted']};">{c['desc']}</div>
                    <div style="height:6px;background:{t['border']};border-radius:3px;margin-top:0.5rem;overflow:hidden;">
                        <div style="width:{c['progress']}%;height:100%;background:{t['success'] if is_complete else t['primary']};"></div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="color:{t['success']};font-weight:600;">{c['reward']}</div>
                    <div style="font-size:0.7rem;color:{t['text_muted']};">{c['expires']}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Weekly challenges
    st.markdown("#### Weekly Challenges")
    
    weekly = [
        {"name": "Marathon Runner", "desc": "Complete 3 full audits", "reward": "200 XP + Badge", "progress": 66, "icon": "🏃", "expires": "3 days left"},
        {"name": "Quality Champion", "desc": "Zero rework on all deliverables", "reward": "150 XP", "progress": 100, "icon": "💎", "expires": "Completed!"},
        {"name": "Team Spirit", "desc": "Review 5 colleague workpapers", "reward": "100 XP", "progress": 80, "icon": "🤝", "expires": "3 days left"},
    ]
    
    for c in weekly:
        is_complete = c['progress'] >= 100
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['success'] if is_complete else t['border']};border-radius:12px;padding:1.25rem;margin-bottom:0.75rem;">
            <div style="display:flex;align-items:center;gap:1rem;">
                <div style="font-size:2rem;">{c['icon']}</div>
                <div style="flex:1;">
                    <div style="font-weight:600;color:{t['text']};">{c['name']} {'✅' if is_complete else ''}</div>
                    <div style="font-size:0.8rem;color:{t['text_muted']};">{c['desc']}</div>
                    <div style="height:6px;background:{t['border']};border-radius:3px;margin-top:0.5rem;overflow:hidden;">
                        <div style="width:{c['progress']}%;height:100%;background:{t['success'] if is_complete else t['accent']};"></div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="color:{t['warning']};font-weight:600;">{c['reward']}</div>
                    <div style="font-size:0.7rem;color:{t['text_muted']};">{c['expires']}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Special event
    st.markdown("#### 🎉 Special Event: Year-End Audit Sprint")
    
    st.markdown(f'''
    <div style="background:linear-gradient(135deg, {t['warning']}20, {t['danger']}20);border:2px solid {t['warning']};border-radius:16px;padding:1.5rem;margin-bottom:1rem;">
        <div style="display:flex;align-items:center;gap:1.5rem;">
            <div style="font-size:3rem;">🏆</div>
            <div style="flex:1;">
                <div style="font-weight:700;color:{t['text']};font-size:1.1rem;">Complete 5 audits before Dec 31</div>
                <div style="color:{t['text_secondary']};margin:0.25rem 0;">Double XP for all activities during the event!</div>
                <div style="height:10px;background:{t['border']};border-radius:5px;margin-top:0.75rem;overflow:hidden;">
                    <div style="width:60%;height:100%;background:linear-gradient(90deg, {t['warning']}, {t['danger']});"></div>
                </div>
                <div style="font-size:0.8rem;color:{t['text_muted']};margin-top:0.5rem;">3/5 completed • 21 days remaining</div>
            </div>
            <div style="text-align:center;background:{t['card']};padding:1rem;border-radius:12px;">
                <div style="font-size:0.75rem;color:{t['text_muted']};">Grand Prize</div>
                <div style="font-size:1.5rem;font-weight:700;color:{t['warning']};">1000 XP</div>
                <div style="font-size:0.7rem;color:{t['accent']};">+ Exclusive Badge</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def _render_rewards(t: dict):
    """Render rewards store."""
    st.markdown("### 🎁 Rewards Store")
    
    current_xp = st.session_state.user_xp
    
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-bottom:1.5rem;text-align:center;">
        <span style="color:{t['text_muted']};">Your Balance:</span>
        <span style="font-size:1.5rem;font-weight:700;color:{t['primary']};margin-left:0.5rem;">{current_xp:,} XP</span>
    </div>
    ''', unsafe_allow_html=True)
    
    rewards = [
        {"name": "Coffee Voucher ☕", "desc": "Starbucks Rp 50k voucher", "cost": 500, "icon": "☕", "stock": 10},
        {"name": "Extra Leave Day 🏖️", "desc": "1 additional day off", "cost": 2000, "icon": "🏖️", "stock": 3},
        {"name": "Training Budget 📚", "desc": "Rp 500k training fund", "cost": 1500, "icon": "📚", "stock": 5},
        {"name": "Lunch with CAE 🍽️", "desc": "Exclusive lunch meeting", "cost": 3000, "icon": "🍽️", "stock": 1},
        {"name": "Profile Badge Frame 🖼️", "desc": "Golden profile border", "cost": 800, "icon": "🖼️", "stock": "∞"},
        {"name": "Custom Title ✨", "desc": "Choose your own title", "cost": 1000, "icon": "✨", "stock": "∞"},
        {"name": "Parking Spot 🚗", "desc": "Premium parking for 1 month", "cost": 2500, "icon": "🚗", "stock": 2},
        {"name": "Tech Gadget 🎧", "desc": "Wireless earbuds", "cost": 5000, "icon": "🎧", "stock": 1},
    ]
    
    cols = st.columns(4)
    for i, reward in enumerate(rewards):
        can_afford = current_xp >= reward['cost']
        
        with cols[i % 4]:
            st.markdown(f'''
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.25rem;text-align:center;margin-bottom:1rem;opacity:{'1' if can_afford else '0.6'};">
                <div style="font-size:2.5rem;margin-bottom:0.5rem;">{reward['icon']}</div>
                <div style="font-weight:600;color:{t['text']};font-size:0.9rem;">{reward['name']}</div>
                <div style="font-size:0.75rem;color:{t['text_muted']};margin:0.25rem 0;min-height:2rem;">{reward['desc']}</div>
                <div style="font-size:1.1rem;font-weight:700;color:{t['primary']};margin:0.5rem 0;">{reward['cost']:,} XP</div>
                <div style="font-size:0.7rem;color:{t['text_muted']};">Stock: {reward['stock']}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button("Redeem" if can_afford else "Need More XP", key=f"redeem_{i}", use_container_width=True, disabled=not can_afford):
                if can_afford:
                    st.success(f"🎉 {reward['name']} redeemed!")
