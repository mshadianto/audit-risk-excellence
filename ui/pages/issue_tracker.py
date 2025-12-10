"""
Issue Tracker Module for AURIX.
Kanban-style issue tracking for audit findings.
"""

import streamlit as st
from datetime import datetime, timedelta
import random

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer


def render():
    """Render the issue tracker page."""
    t = get_current_theme()
    
    render_page_header(
        "📌 Issue Tracker",
        "Track and manage audit issues with Kanban-style workflow"
    )
    
    # Initialize issues
    if 'issues' not in st.session_state:
        st.session_state.issues = _get_sample_issues()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Kanban Board",
        "📊 List View",
        "➕ New Issue",
        "📈 Analytics"
    ])
    
    with tab1:
        _render_kanban_board(t)
    
    with tab2:
        _render_list_view(t)
    
    with tab3:
        _render_new_issue_form(t)
    
    with tab4:
        _render_analytics(t)
    
    render_footer()


def _get_sample_issues():
    """Get sample issues data."""
    return [
        {"id": "ISS-001", "title": "Segregation of Duties Gap", "status": "Open", "priority": "High", "assignee": "Ahmad R.", "due": "2025-02-15", "progress": 0},
        {"id": "ISS-002", "title": "Missing Approval Documentation", "status": "Open", "priority": "Medium", "assignee": "Budi S.", "due": "2025-02-20", "progress": 0},
        {"id": "ISS-003", "title": "System Access Review Overdue", "status": "Open", "priority": "Critical", "assignee": "Citra D.", "due": "2025-02-10", "progress": 0},
        {"id": "ISS-004", "title": "KYC Document Incomplete", "status": "In Progress", "priority": "High", "assignee": "Dewi P.", "due": "2025-02-25", "progress": 40},
        {"id": "ISS-005", "title": "Reconciliation Discrepancy", "status": "In Progress", "priority": "Medium", "assignee": "Ahmad R.", "due": "2025-03-01", "progress": 60},
        {"id": "ISS-006", "title": "Vendor Contract Expired", "status": "In Progress", "priority": "Low", "assignee": "Budi S.", "due": "2025-03-05", "progress": 80},
        {"id": "ISS-007", "title": "Backup Procedure Update", "status": "Review", "priority": "Medium", "assignee": "Citra D.", "due": "2025-02-28", "progress": 90},
        {"id": "ISS-008", "title": "Policy Document Revision", "status": "Review", "priority": "Low", "assignee": "Dewi P.", "due": "2025-03-10", "progress": 95},
        {"id": "ISS-009", "title": "Training Record Gap", "status": "Closed", "priority": "Medium", "assignee": "Ahmad R.", "due": "2025-01-30", "progress": 100},
        {"id": "ISS-010", "title": "Password Policy Violation", "status": "Closed", "priority": "High", "assignee": "Budi S.", "due": "2025-01-25", "progress": 100},
    ]


def _render_kanban_board(t: dict):
    """Render Kanban board view."""
    st.markdown("### 📋 Issue Kanban Board")
    
    issues = st.session_state.issues
    statuses = ["Open", "In Progress", "Review", "Closed"]
    status_icons = {"Open": "📥", "In Progress": "🔄", "Review": "👁️", "Closed": "✅"}
    status_colors = {"Open": t['danger'], "In Progress": t['warning'], "Review": t['accent'], "Closed": t['success']}
    
    # Count summary
    cols = st.columns(4)
    for i, status in enumerate(statuses):
        count = len([iss for iss in issues if iss['status'] == status])
        color = status_colors[status]
        with cols[i]:
            st.markdown(f"""
            <div style="background:{t['card']};border:2px solid {color};border-radius:12px;padding:1rem;text-align:center;">
                <div style="font-size:1.5rem;">{status_icons[status]}</div>
                <div style="font-size:2rem;font-weight:700;color:{color};">{count}</div>
                <div style="font-size:0.85rem;color:{t['text']};">{status}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Kanban columns
    cols = st.columns(4)
    
    for i, status in enumerate(statuses):
        with cols[i]:
            color = status_colors[status]
            st.markdown(f"""
            <div style="background:{color}20;border-top:3px solid {color};border-radius:0 0 8px 8px;padding:0.5rem;margin-bottom:0.75rem;">
                <span style="font-weight:600;color:{color};">{status_icons[status]} {status}</span>
            </div>
            """, unsafe_allow_html=True)
            
            status_issues = [iss for iss in issues if iss['status'] == status]
            
            for iss in status_issues:
                _render_issue_card(t, iss)
            
            if not status_issues:
                st.markdown(f"""
                <div style="background:{t['bg_secondary']};border:1px dashed {t['border']};border-radius:8px;padding:1rem;text-align:center;color:{t['text_muted']};font-size:0.85rem;">
                    No issues
                </div>
                """, unsafe_allow_html=True)


def _render_issue_card(t: dict, issue: dict):
    """Render a single issue card."""
    priority_colors = {
        "Critical": t['danger'],
        "High": "#f97316",
        "Medium": t['warning'],
        "Low": t['success']
    }
    color = priority_colors.get(issue['priority'], t['text_muted'])
    
    st.markdown(f"""
    <div style="background:{t['card']};border:1px solid {t['border']};border-left:3px solid {color};border-radius:0 8px 8px 0;padding:0.75rem;margin-bottom:0.5rem;">
        <div style="font-size:0.65rem;color:{t['text_muted']};margin-bottom:0.25rem;">{issue['id']}</div>
        <div style="font-size:0.85rem;font-weight:600;color:{t['text']};margin-bottom:0.5rem;">{issue['title']}</div>
        <div style="display:flex;justify-content:space-between;align-items:center;font-size:0.7rem;">
            <span style="background:{color}20;color:{color};padding:0.1rem 0.4rem;border-radius:4px;">{issue['priority']}</span>
            <span style="color:{t['text_muted']};">👤 {issue['assignee'].split()[0]}</span>
        </div>
        <div style="margin-top:0.5rem;">
            <div style="height:4px;background:{t['bg_secondary']};border-radius:2px;overflow:hidden;">
                <div style="height:100%;width:{issue['progress']}%;background:{color};"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_list_view(t: dict):
    """Render list view of issues."""
    st.markdown("### 📊 Issue List")
    
    issues = st.session_state.issues
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.multiselect("Status", ["Open", "In Progress", "Review", "Closed"], default=["Open", "In Progress", "Review"])
    with col2:
        priority_filter = st.multiselect("Priority", ["Critical", "High", "Medium", "Low"], default=["Critical", "High", "Medium", "Low"])
    with col3:
        search = st.text_input("🔍 Search", placeholder="Search issues...")
    
    # Filter issues
    filtered = [iss for iss in issues 
                if iss['status'] in status_filter 
                and iss['priority'] in priority_filter
                and (search.lower() in iss['title'].lower() if search else True)]
    
    st.markdown(f"**Showing {len(filtered)} issues**")
    
    # List
    for iss in filtered:
        priority_colors = {"Critical": t['danger'], "High": "#f97316", "Medium": t['warning'], "Low": t['success']}
        status_colors = {"Open": t['danger'], "In Progress": t['warning'], "Review": t['accent'], "Closed": t['success']}
        
        p_color = priority_colors.get(iss['priority'], t['text_muted'])
        s_color = status_colors.get(iss['status'], t['text_muted'])
        
        st.markdown(f"""
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:8px;padding:1rem;margin-bottom:0.5rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="flex:1;">
                    <span style="font-size:0.75rem;color:{t['text_muted']};margin-right:0.5rem;">{iss['id']}</span>
                    <span style="font-weight:600;color:{t['text']};">{iss['title']}</span>
                </div>
                <div style="display:flex;gap:0.5rem;align-items:center;">
                    <span style="background:{s_color}20;color:{s_color};padding:0.2rem 0.5rem;border-radius:4px;font-size:0.7rem;">{iss['status']}</span>
                    <span style="background:{p_color}20;color:{p_color};padding:0.2rem 0.5rem;border-radius:4px;font-size:0.7rem;">{iss['priority']}</span>
                    <span style="font-size:0.75rem;color:{t['text_muted']};">👤 {iss['assignee']}</span>
                    <span style="font-size:0.75rem;color:{t['text_muted']};">📅 {iss['due']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_new_issue_form(t: dict):
    """Render new issue form."""
    st.markdown("### ➕ Create New Issue")
    
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("Issue Title *", placeholder="Brief description of the issue")
        category = st.selectbox("Category", ["Control Deficiency", "Compliance Gap", "Process Issue", "Documentation Gap", "System Issue"])
        priority = st.selectbox("Priority", ["Critical", "High", "Medium", "Low"])
        assignee = st.selectbox("Assignee", ["Ahmad R.", "Budi S.", "Citra D.", "Dewi P."])
    
    with col2:
        due_date = st.date_input("Due Date", value=datetime.now() + timedelta(days=30))
        related_finding = st.text_input("Related Finding ID", placeholder="e.g., FND-2025-001")
        source = st.selectbox("Source", ["Internal Audit", "External Audit", "Regulator", "Self-Identified", "Whistleblower"])
        auditee = st.text_input("Auditee/Department", placeholder="e.g., Operations Division")
    
    description = st.text_area("Description", placeholder="Detailed description of the issue...", height=100)
    action = st.text_area("Recommended Action", placeholder="Suggested corrective action...", height=80)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Save as Draft", use_container_width=True):
            st.info("Draft saved!")
    with col2:
        if st.button("✅ Create Issue", use_container_width=True, type="primary"):
            if title:
                new_id = f"ISS-{len(st.session_state.issues)+1:03d}"
                st.success(f"Issue {new_id} created successfully!")
            else:
                st.error("Please enter issue title")
    with col3:
        if st.button("🗑️ Clear Form", use_container_width=True):
            st.rerun()


def _render_analytics(t: dict):
    """Render issue analytics."""
    st.markdown("### 📈 Issue Analytics")
    
    issues = st.session_state.issues
    
    # Summary metrics
    total = len(issues)
    open_count = len([i for i in issues if i['status'] == 'Open'])
    in_progress = len([i for i in issues if i['status'] == 'In Progress'])
    critical_open = len([i for i in issues if i['status'] in ['Open', 'In Progress'] and i['priority'] == 'Critical'])
    
    cols = st.columns(5)
    metrics = [
        ("📋 Total Issues", total, t['primary']),
        ("📥 Open", open_count, t['danger']),
        ("🔄 In Progress", in_progress, t['warning']),
        ("⏰ Overdue", 2, t['danger']),
        ("🔴 Critical Open", critical_open, t['danger']),
    ]
    
    for col, (label, value, color) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;text-align:center;">
                <div style="font-size:1.75rem;font-weight:700;color:{color};">{value}</div>
                <div style="font-size:0.75rem;color:{t['text_muted']};">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # By Status
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### By Status")
        for status in ["Open", "In Progress", "Review", "Closed"]:
            count = len([i for i in issues if i['status'] == status])
            pct = count / total * 100
            color = {"Open": t['danger'], "In Progress": t['warning'], "Review": t['accent'], "Closed": t['success']}[status]
            st.markdown(f"""
            <div style="margin-bottom:0.5rem;">
                <div style="display:flex;justify-content:space-between;margin-bottom:0.25rem;">
                    <span style="font-size:0.85rem;color:{t['text']};">{status}</span>
                    <span style="font-size:0.85rem;color:{t['text_muted']};">{count} ({pct:.0f}%)</span>
                </div>
                <div style="height:8px;background:{t['bg_secondary']};border-radius:4px;overflow:hidden;">
                    <div style="height:100%;width:{pct}%;background:{color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### By Priority")
        for priority in ["Critical", "High", "Medium", "Low"]:
            count = len([i for i in issues if i['priority'] == priority])
            pct = count / total * 100
            color = {"Critical": t['danger'], "High": "#f97316", "Medium": t['warning'], "Low": t['success']}[priority]
            st.markdown(f"""
            <div style="margin-bottom:0.5rem;">
                <div style="display:flex;justify-content:space-between;margin-bottom:0.25rem;">
                    <span style="font-size:0.85rem;color:{t['text']};">{priority}</span>
                    <span style="font-size:0.85rem;color:{t['text_muted']};">{count} ({pct:.0f}%)</span>
                </div>
                <div style="height:8px;background:{t['bg_secondary']};border-radius:4px;overflow:hidden;">
                    <div style="height:100%;width:{pct}%;background:{color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Aging analysis
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### ⏱️ Aging Analysis (Open Issues)")
    
    aging = [
        ("0-7 days", 2, t['success']),
        ("8-14 days", 1, t['accent']),
        ("15-30 days", 1, t['warning']),
        ("31-60 days", 0, "#f97316"),
        (">60 days", 0, t['danger']),
    ]
    
    cols = st.columns(5)
    for col, (label, count, color) in zip(cols, aging):
        with col:
            st.markdown(f"""
            <div style="background:{color}20;border:1px solid {color};border-radius:8px;padding:0.75rem;text-align:center;">
                <div style="font-size:1.25rem;font-weight:700;color:{color};">{count}</div>
                <div style="font-size:0.7rem;color:{t['text_muted']};">{label}</div>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    render()
