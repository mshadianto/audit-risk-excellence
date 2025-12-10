"""
Application Router - Handles page navigation and rendering.
"""

import streamlit as st
from typing import Dict, Callable, Any

from ui.components.sidebar import render_sidebar
from ui.styles.css_builder import inject_css
from ui.pages import (
    dashboard,
    documents,
    ptcf_builder,
    risk_assessment,
    findings,
    continuous_audit,
    kri_dashboard,
    fraud_detection,
    regulatory_compliance,
    chat,
    analytics,
    settings,
    help,
    about,
    error,
    not_found
)


class Router:
    """
    Application router that handles page navigation.
    Implements a simple routing pattern for Streamlit.
    """
    
    def __init__(self):
        """Initialize router with page mappings."""
        self.routes: Dict[str, Callable] = {
            "📊 Dashboard": dashboard.render,
            "📁 Documents": documents.render,
            "🎭 PTCF Builder": ptcf_builder.render,
            "⚖️ Risk Assessment": risk_assessment.render,
            "📋 Findings Tracker": findings.render,
            "🔄 Continuous Audit": continuous_audit.render,
            "📈 KRI Dashboard": kri_dashboard.render,
            "🔍 Fraud Detection": fraud_detection.render,
            "📚 Regulations": regulatory_compliance.render,
            "🤖 AI Chat": chat.render,
            "📊 Analytics": analytics.render,
            "⚙️ Settings": settings.render,
            "❓ Help": help.render,
            "ℹ️ About": about.render,
        }
        
        self.page_categories = {
            "Main": [
                "📊 Dashboard",
                "📁 Documents",
                "🎭 PTCF Builder",
            ],
            "Audit": [
                "⚖️ Risk Assessment",
                "📋 Findings Tracker",
                "🔄 Continuous Audit",
            ],
            "Intelligence": [
                "📈 KRI Dashboard",
                "🔍 Fraud Detection",
                "🤖 AI Chat",
                "📊 Analytics",
            ],
            "Reference": [
                "📚 Regulations",
                "⚙️ Settings",
                "❓ Help",
                "ℹ️ About",
            ]
        }
    
    def render(self):
        """Main render method - renders sidebar and current page."""
        # Inject CSS styles
        inject_css()
        
        # Render sidebar and get selected page
        selected_page = render_sidebar(
            routes=list(self.routes.keys()),
            categories=self.page_categories
        )
        
        # Store current page in session
        st.session_state.current_page = selected_page
        
        # Render selected page
        self._render_page(selected_page)
    
    def _render_page(self, page_name: str):
        """Render specific page by name."""
        if page_name in self.routes:
            try:
                self.routes[page_name]()
            except Exception as e:
                self._render_error_page(page_name, e)
        else:
            self._render_404(page_name)
    
    def _render_error_page(self, page_name: str, err: Exception):
        """Render error page when page fails to load."""
        st.session_state.error_timestamp = st.session_state.get('error_timestamp', '')
        from datetime import datetime
        st.session_state.error_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        error.render(
            error_message=f"Failed to load {page_name}: {str(err)}",
            error_code="ERR_PAGE_LOAD"
        )
    
    def _render_404(self, requested_page: str = ""):
        """Render 404 not found page."""
        not_found.render(requested_page)
    
    def get_page_icon(self, page_name: str) -> str:
        """Extract icon from page name."""
        if " " in page_name:
            return page_name.split(" ")[0]
        return "📄"
    
    def get_page_title(self, page_name: str) -> str:
        """Extract title from page name (without icon)."""
        if " " in page_name:
            return " ".join(page_name.split(" ")[1:])
        return page_name
