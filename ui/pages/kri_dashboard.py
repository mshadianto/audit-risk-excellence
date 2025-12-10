"""
KRI Dashboard Page Module for AURIX.
Key Risk Indicators monitoring and visualization.
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

from ui.styles.css_builder import get_current_theme
from ui.components import (
    render_page_header,
    render_footer,
    render_badge,
    render_metric_card,
    render_kri_gauge,
    render_progress_bar
)
from data.seeds import KRI_INDICATORS


class KRIDashboardPage:
    """KRI Dashboard with interactive visualizations."""
    
    def __init__(self):
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state for KRI data."""
        if 'kri_values' not in st.session_state:
            st.session_state.kri_values = self._generate_sample_kri_data()
        
        if 'kri_history' not in st.session_state:
            st.session_state.kri_history = self._generate_historical_data()
    
    def _generate_sample_kri_data(self) -> Dict:
        """Generate sample KRI values for demo."""
        kri_data = {}
        
        for category, indicators in KRI_INDICATORS.items():
            kri_data[category] = {}
            for ind in indicators:
                name = ind['name']
                threshold = ind['threshold']
                
                # Generate realistic values based on threshold
                if threshold == 0:
                    value = random.randint(0, 3)
                elif ind['good_direction'] == 'lower':
                    value = threshold * random.uniform(0.5, 1.2)
                elif ind['good_direction'] == 'higher':
                    value = threshold * random.uniform(0.85, 1.15)
                else:
                    value = threshold * random.uniform(0.9, 1.1)
                
                kri_data[category][name] = {
                    'value': round(value, 2),
                    'threshold': threshold,
                    'unit': ind['unit'],
                    'good_direction': ind['good_direction'],
                    'trend': random.choice(['up', 'down', 'stable']),
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
        
        return kri_data
    
    def _generate_historical_data(self) -> Dict:
        """Generate historical KRI data for trends."""
        history = {}
        
        for category, indicators in KRI_INDICATORS.items():
            history[category] = {}
            for ind in indicators:
                name = ind['name']
                threshold = ind['threshold']
                
                # Generate 12 months of data
                values = []
                base_value = threshold * 0.8 if threshold > 0 else 1
                
                for i in range(12):
                    variation = random.uniform(-0.15, 0.15)
                    val = base_value * (1 + variation)
                    values.append(round(val, 2))
                    base_value = val
                
                history[category][name] = values
        
        return history
    
    def render(self):
        """Render the KRI Dashboard page."""
        render_page_header("KRI Dashboard", "Key Risk Indicators Monitoring & Analysis")
        
        t = get_current_theme()
        
        # Overall Risk Summary
        self._render_risk_summary()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Category selector
        categories = list(KRI_INDICATORS.keys())
        
        tab_names = [f"📊 {cat}" for cat in categories]
        tabs = st.tabs(tab_names)
        
        for tab, category in zip(tabs, categories):
            with tab:
                self._render_category_dashboard(category)
        
        render_footer()
    
    def _render_risk_summary(self):
        """Render overall risk summary."""
        t = get_current_theme()
        
        # Calculate breach counts
        total_kris = 0
        breached = 0
        warning = 0
        
        for category, indicators in st.session_state.kri_values.items():
            for name, data in indicators.items():
                total_kris += 1
                value = data['value']
                threshold = data['threshold']
                direction = data['good_direction']
                
                if threshold == 0:
                    if value > 0:
                        breached += 1
                elif direction == 'lower':
                    if value > threshold:
                        breached += 1
                    elif value > threshold * 0.8:
                        warning += 1
                elif direction == 'higher':
                    if value < threshold:
                        breached += 1
                    elif value < threshold * 1.1:
                        warning += 1
        
        healthy = total_kris - breached - warning
        
        # Use Streamlit columns for metrics
        cols = st.columns(4)
        
        metrics_data = [
            ("TOTAL KRIS", str(total_kris), "Monitored indicators", t['accent']),
            ("HEALTHY", str(healthy), f"{healthy/total_kris*100:.0f}% of total", t['success']),
            ("WARNING", str(warning), "Near threshold", t['warning']),
            ("BREACHED", str(breached), "Action required", t['danger'] if breached > 0 else t['success']),
        ]
        
        for col, (label, value, change, color) in zip(cols, metrics_data):
            with col:
                st.markdown(f'''
                <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.25rem;">
                    <div style="font-size:0.75rem;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;color:{t['text_muted']} !important;margin-bottom:0.5rem;">{label}</div>
                    <div style="font-size:1.75rem;font-weight:700;color:{t['text']} !important;">{value}</div>
                    <div style="font-size:0.75rem;margin-top:0.25rem;color:{color} !important;">{change}</div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Risk heat indicator
        if breached > 2:
            risk_level = "HIGH"
            risk_color = t['danger']
        elif breached > 0 or warning > 3:
            risk_level = "MEDIUM"
            risk_color = t['warning']
        else:
            risk_level = "LOW"
            risk_color = t['success']
        
        st.markdown(f'''
        <div style="text-align:center;padding:1rem;background:linear-gradient(135deg, {risk_color}15, {risk_color}05);border:1px solid {risk_color}30;border-radius:12px;margin-top:1rem;">
            <div style="font-size:0.85rem;color:{t['text_muted']} !important;">Overall Risk Level</div>
            <div style="font-size:2rem;font-weight:700;color:{risk_color} !important;">{risk_level}</div>
            <div style="font-size:0.8rem;color:{t['text_secondary']} !important;">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    def _render_category_dashboard(self, category: str):
        """Render dashboard for a specific KRI category."""
        t = get_current_theme()
        
        st.markdown(f"### {category}")
        
        indicators = st.session_state.kri_values.get(category, {})
        
        if not indicators:
            st.info("No indicators configured for this category.")
            return
        
        # Create gauge grid
        cols = st.columns(3)
        
        for i, (name, data) in enumerate(indicators.items()):
            with cols[i % 3]:
                self._render_kri_card(name, data, category)
        
        # Trend Analysis
        st.markdown("---")
        st.markdown("#### 📈 Trend Analysis (12 Months)")
        
        history = st.session_state.kri_history.get(category, {})
        
        selected_kri = st.selectbox(
            "Select KRI for trend view",
            options=list(indicators.keys()),
            key=f"kri_trend_{category}"
        )
        
        if selected_kri and selected_kri in history:
            self._render_trend_chart(selected_kri, history[selected_kri], indicators[selected_kri])
    
    def _render_kri_card(self, name: str, data: Dict, category: str):
        """Render a single KRI card with gauge."""
        t = get_current_theme()
        
        value = data['value']
        threshold = data['threshold']
        unit = data['unit']
        direction = data['good_direction']
        trend = data['trend']
        
        # Determine status color
        if threshold == 0:
            if value == 0:
                status = 'healthy'
                status_color = t['success']
            elif value <= 2:
                status = 'warning'
                status_color = t['warning']
            else:
                status = 'breached'
                status_color = t['danger']
        elif direction == 'lower':
            if value <= threshold * 0.8:
                status = 'healthy'
                status_color = t['success']
            elif value <= threshold:
                status = 'warning'
                status_color = t['warning']
            else:
                status = 'breached'
                status_color = t['danger']
        elif direction == 'higher':
            if value >= threshold:
                status = 'healthy'
                status_color = t['success']
            elif value >= threshold * 0.9:
                status = 'warning'
                status_color = t['warning']
            else:
                status = 'breached'
                status_color = t['danger']
        else:  # optimal
            diff_pct = abs(value - threshold) / threshold if threshold > 0 else 0
            if diff_pct <= 0.1:
                status = 'healthy'
                status_color = t['success']
            elif diff_pct <= 0.2:
                status = 'warning'
                status_color = t['warning']
            else:
                status = 'breached'
                status_color = t['danger']
        
        # Trend icon
        trend_icons = {'up': '📈', 'down': '📉', 'stable': '➡️'}
        trend_icon = trend_icons.get(trend, '➡️')
        
        st.markdown(f'''
        <div class="pro-card" style="padding:1rem;text-align:center;border-left:4px solid {status_color};">
            <div style="font-size:0.85rem;color:{t['text_secondary']} !important;margin-bottom:0.5rem;">
                {name}
            </div>
            <div style="font-size:2rem;font-weight:700;color:{status_color} !important;">
                {value}{unit}
            </div>
            <div style="font-size:0.75rem;color:{t['text_muted']} !important;margin:0.5rem 0;">
                Threshold: {threshold}{unit}
            </div>
            <div style="display:flex;justify-content:center;align-items:center;gap:0.5rem;">
                <span style="font-size:1rem;">{trend_icon}</span>
                <span class="badge" style="background:{status_color}20;color:{status_color};">
                    {status.upper()}
                </span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Progress bar showing position relative to threshold
        if threshold > 0:
            max_display = threshold * 1.5
            pct = min((value / max_display) * 100, 100)
            threshold_pct = (threshold / max_display) * 100
            
            st.markdown(f'''
            <div style="position:relative;height:20px;background:{t['bg_secondary']};border-radius:4px;margin-top:0.5rem;">
                <div style="position:absolute;left:{threshold_pct}%;top:0;bottom:0;width:2px;background:{t['warning']};"></div>
                <div style="width:{pct}%;height:100%;background:{status_color};border-radius:4px;"></div>
            </div>
            ''', unsafe_allow_html=True)
    
    def _render_trend_chart(self, name: str, values: List[float], current_data: Dict):
        """Render a simple trend chart."""
        t = get_current_theme()
        
        threshold = current_data['threshold']
        unit = current_data['unit']
        
        # Generate month labels
        months = []
        for i in range(11, -1, -1):
            month = (datetime.now() - timedelta(days=30*i)).strftime('%b')
            months.append(month)
        
        # Calculate chart dimensions
        max_val = max(max(values), threshold * 1.2 if threshold > 0 else max(values) * 1.2)
        min_val = min(min(values), threshold * 0.5 if threshold > 0 else 0)
        range_val = max_val - min_val if max_val > min_val else 1
        
        chart_height = 200
        
        # Header
        st.markdown(f'''
        <div class="pro-card" style="padding:1rem;">
            <div style="display:flex;justify-content:space-between;margin-bottom:1rem;">
                <span style="font-weight:600;color:{t['text']} !important;">{name} - 12 Month Trend</span>
                <span style="color:{t['text_muted']} !important;">Threshold: {threshold}{unit}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Use Streamlit columns for the chart
        cols = st.columns(12)
        for i, (col, month, val) in enumerate(zip(cols, months, values)):
            with col:
                height_pct = ((val - min_val) / range_val * 100) if range_val > 0 else 50
                color = t['success'] if val <= threshold or threshold == 0 else t['danger']
                st.markdown(f'''
                <div style="display:flex;flex-direction:column;align-items:center;height:{chart_height}px;">
                    <div style="flex:1;width:100%;display:flex;align-items:end;">
                        <div style="width:100%;height:{height_pct}%;background:{color};border-radius:4px 4px 0 0;min-height:4px;"></div>
                    </div>
                    <div style="font-size:0.6rem;color:{t['text_muted']} !important;margin-top:4px;">{month}</div>
                    <div style="font-size:0.65rem;color:{t['text']} !important;">{val:.1f}</div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Stats footer
        st.markdown(f'''
        <div class="pro-card" style="padding:1rem;margin-top:0.5rem;">
            <div style="display:flex;justify-content:space-around;font-size:0.85rem;">
                <div>
                    <span style="color:{t['text_muted']} !important;">Min:</span>
                    <span style="font-weight:600;color:{t['text']} !important;"> {min(values):.2f}{unit}</span>
                </div>
                <div>
                    <span style="color:{t['text_muted']} !important;">Max:</span>
                    <span style="font-weight:600;color:{t['text']} !important;"> {max(values):.2f}{unit}</span>
                </div>
                <div>
                    <span style="color:{t['text_muted']} !important;">Avg:</span>
                    <span style="font-weight:600;color:{t['text']} !important;"> {sum(values)/len(values):.2f}{unit}</span>
                </div>
                <div>
                    <span style="color:{t['text_muted']} !important;">Current:</span>
                    <span style="font-weight:600;color:{t['text']} !important;"> {current_data['value']}{unit}</span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Update KRI value
        col1, col2 = st.columns([3, 1])
        
        with col1:
            new_value = st.number_input(
                f"Update {name} value",
                value=float(current_data['value']),
                step=0.1,
                key=f"update_kri_{name}"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📥 Update", key=f"btn_update_{name}"):
                # Find and update the value
                for cat, indicators in st.session_state.kri_values.items():
                    if name in indicators:
                        indicators[name]['value'] = new_value
                        indicators[name]['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                        st.success(f"✓ {name} updated to {new_value}{unit}")
                        st.rerun()


def render():
    """Entry point for the KRI Dashboard page."""
    page = KRIDashboardPage()
    page.render()
