"""Streamlit dashboard for Agent Factory monitoring."""

import streamlit as st
import requests
import json
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List

# Configuration
API_BASE_URL = "http://localhost:8000"
HEALTH_ENDPOINT = f"{API_BASE_URL}/health"
REFRESH_INTERVAL = 30  # seconds

# Page configuration
st.set_page_config(
    page_title="Agent Factory Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        background-color: #f8f9fa;
    }
    .status-healthy { border-left: 4px solid #28a745; }
    .status-warning { border-left: 4px solid #ffc107; }
    .status-critical { border-left: 4px solid #dc3545; }
    .status-unknown { border-left: 4px solid #6c757d; }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
    }
    .metric-label {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


def get_health_data() -> Dict[str, Any]:
    """Fetch health data from the API."""
    try:
        response = requests.get(f"{HEALTH_ENDPOINT}/status", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch health data: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        return {}


def get_agent_summary() -> Dict[str, Any]:
    """Fetch agent summary from the API."""
    try:
        response = requests.get(f"{HEALTH_ENDPOINT}/agents", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch agent summary: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        return {}


def get_system_metrics() -> Dict[str, Any]:
    """Fetch system metrics from the API."""
    try:
        response = requests.get(f"{HEALTH_ENDPOINT}/metrics", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch metrics: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
            return {}


def render_header():
    """Render the main header."""
    st.markdown('<h1 class="main-header">🤖 Agent Factory Dashboard</h1>', unsafe_allow_html=True)
    
    # Last updated timestamp
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def render_system_overview(health_data: Dict[str, Any]):
    """Render system overview section."""
    st.header("📊 System Overview")
    
    if not health_data:
        st.warning("No health data available")
        return
    
    system_info = health_data.get("system", {}).get("overall", {})
    overall_status = system_info.get("status", "unknown")
    agent_health_pct = system_info.get("agent_health_percentage", 0)
    healthy_agents = system_info.get("healthy_agents", 0)
    total_agents = system_info.get("total_agents", 0)
    
    # Status indicator
    status_color = {
        "healthy": "🟢",
        "warning": "🟡", 
        "critical": "🔴",
        "unknown": "⚪"
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="status-card status-{overall_status}">
            <div class="metric-value">{status_color.get(overall_status, "⚪")}</div>
            <div class="metric-label">System Status</div>
            <div style="text-align: center; font-weight: bold; color: #1f77b4;">{overall_status.upper()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="status-card">
            <div class="metric-value">{agent_health_pct:.1f}%</div>
            <div class="metric-label">Agent Health</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="status-card">
            <div class="metric-value">{healthy_agents}/{total_agents}</div>
            <div class="metric-label">Healthy Agents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        last_check = system_info.get("last_check", "Unknown")
        if last_check != "Unknown":
            try:
                dt = datetime.fromisoformat(last_check.replace('Z', '+00:00'))
                last_check = dt.strftime('%H:%M:%S')
            except:
                pass
        
        st.markdown(f"""
        <div class="status-card">
            <div class="metric-value">{last_check}</div>
            <div class="metric-label">Last Check</div>
        </div>
        """, unsafe_allow_html=True)


def render_agent_status(health_data: Dict[str, Any]):
    """Render agent status section."""
    st.header("🤖 Agent Status")
    
    if not health_data:
        st.warning("No agent data available")
        return
    
    agents = health_data.get("agents", {})
    
    if not agents:
        st.info("No agents found")
        return
    
    # Create agent status grid
    cols = st.columns(3)
    col_idx = 0
    
    for agent_id, status in agents.items():
        with cols[col_idx]:
            agent_status = status.get("status", "unknown")
            agent_type = status.get("agent_type", "Unknown")
            last_seen = status.get("last_seen", "Unknown")
            
            # Format timestamp
            if last_seen != "Unknown":
                try:
                    dt = datetime.fromisoformat(last_seen.replace('Z', '+00:00'))
                    last_seen = dt.strftime('%H:%M:%S')
                except:
                    pass
            
            # Status colors
            status_colors = {
                "healthy": "#28a745",
                "unhealthy": "#ffc107", 
                "error": "#dc3545",
                "unknown": "#6c757d"
            }
            
            status_color = status_colors.get(agent_status, "#6c757d")
            
            st.markdown(f"""
            <div class="status-card status-{agent_status}">
                <h3 style="margin: 0; color: {status_color};">{agent_id.title()}</h3>
                <p><strong>Type:</strong> {agent_type}</p>
                <p><strong>Status:</strong> <span style="color: {status_color}; font-weight: bold;">{agent_status.upper()}</span></p>
                <p><strong>Last Seen:</strong> {last_seen}</p>
            </div>
            """, unsafe_allow_html=True)
        
        col_idx = (col_idx + 1) % 3


def render_infrastructure_status(health_data: Dict[str, Any]):
    """Render infrastructure status section."""
    st.header("🏗️ Infrastructure Status")
    
    if not health_data:
        st.warning("No infrastructure data available")
        return
    
    infrastructure = health_data.get("system", {}).get("infrastructure", {})
    
    if not infrastructure:
        st.info("No infrastructure data available")
        return
    
    cols = st.columns(len(infrastructure))
    
    for i, (component, status) in enumerate(infrastructure.items()):
        with cols[i]:
            if isinstance(status, dict) and "status" in status:
                component_status = status["status"]
                timestamp = status.get("timestamp", "Unknown")
                
                # Format timestamp
                if timestamp != "Unknown":
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        timestamp = dt.strftime('%H:%M:%S')
                    except:
                        pass
                
                # Status colors
                status_colors = {
                    "healthy": "#28a745",
                    "unhealthy": "#dc3545",
                    "error": "#dc3545"
                }
                
                status_color = status_colors.get(component_status, "#6c757d")
                
                st.markdown(f"""
                <div class="status-card status-{component_status}">
                    <h3 style="margin: 0; color: {status_color};">{component.title()}</h3>
                    <p><strong>Status:</strong> <span style="color: {status_color}; font-weight: bold;">{component_status.upper()}</span></p>
                    <p><strong>Last Check:</strong> {timestamp}</p>
                </div>
                """, unsafe_allow_html=True)


def render_metrics_charts(metrics_data: Dict[str, Any]):
    """Render metrics charts section."""
    st.header("📈 System Metrics")
    
    if not metrics_data:
        st.warning("No metrics data available")
        return
    
    # Agent health pie chart
    agent_metrics = metrics_data.get("agents", {})
    if agent_metrics:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Agent Health Distribution")
            
            labels = ["Healthy", "Unhealthy", "Error"]
            values = [
                agent_metrics.get("healthy", 0),
                agent_metrics.get("unhealthy", 0),
                agent_metrics.get("error", 0)
            ]
            
            colors = ["#28a745", "#ffc107", "#dc3545"]
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.3,
                marker_colors=colors
            )])
            
            fig.update_layout(
                title="Agent Status Distribution",
                showlegend=True,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Agent Health Percentage")
            
            health_pct = agent_metrics.get("health_percentage", 0)
            
            # Create gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=health_pct,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Health %"},
                delta={'reference': 100},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)


def render_sidebar():
    """Render the sidebar with controls."""
    st.sidebar.title("🎛️ Dashboard Controls")
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Auto-refresh", value=True)
    
    if auto_refresh:
        refresh_interval = st.sidebar.slider(
            "Refresh interval (seconds)", 
            min_value=5, 
            max_value=60, 
            value=REFRESH_INTERVAL
        )
        
        # Use st.empty() to create a placeholder for auto-refresh
        placeholder = st.sidebar.empty()
        if st.button("Refresh Now"):
            st.rerun()
        
        # Auto-refresh logic
        if auto_refresh:
            time.sleep(refresh_interval)
            st.rerun()
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Now"):
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # API status
    st.sidebar.subheader("🔌 API Status")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            st.sidebar.success("✅ API Connected")
        else:
            st.sidebar.error(f"❌ API Error: {response.status_code}")
    except:
        st.sidebar.error("❌ API Unreachable")
    
    st.sidebar.markdown("---")
    
    # System info
    st.sidebar.subheader("ℹ️ System Info")
    st.sidebar.markdown(f"**API Base:** {API_BASE_URL}")
    st.sidebar.markdown(f"**Dashboard:** Streamlit")
    st.sidebar.markdown(f"**Version:** 2.0.0")


def main():
    """Main dashboard function."""
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Fetch data
    health_data = get_health_data()
    agent_summary = get_agent_summary()
    metrics_data = get_system_metrics()
    
    # Render sections
    render_system_overview(health_data)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_agent_status(health_data)
    
    with col2:
        render_infrastructure_status(health_data)
    
    render_metrics_charts(metrics_data)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "🤖 Agent Factory Dashboard v2.0.0 | "
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()