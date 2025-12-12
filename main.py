import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
from typing import List, Dict, Optional
import json

st.set_page_config(
    page_title="Traffic Management System",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)


class TrafficSystem:
    """Модель системы управления трафиком"""
    
    @staticmethod
    def generate_traffic_data():
        """Генерация тестовых данных о трафике"""
        hours = list(range(24))
        traffic_density = [random.randint(20, 100) for _ in range(24)]
        return pd.DataFrame({
            'hour': hours,
            'traffic_density': traffic_density
        })
    
    @staticmethod
    def generate_incidents():
        """Генерация тестовых инцидентов"""
        incidents = []
        types = ['Accident', 'Congestion', 'Road Work', 'Weather Alert']
        statuses = ['New', 'Confirmed', 'Resolved', 'False Alarm']
        priorities = ['High', 'Medium', 'Low']
        
        for i in range(1, 6):
            incidents.append({
                'id': f'INC-2024-{i:03d}',
                'type': random.choice(types),
                'location': f'Intersection {random.randint(1, 20)}',
                'priority': random.choice(priorities),
                'status': random.choice(statuses),
                'timestamp': (datetime.now() - timedelta(hours=random.randint(1, 24))).strftime('%H:%M'),
                'assigned_to': f'Operator {random.randint(1, 5)}'
            })
        return incidents
    
    @staticmethod
    def generate_kpis():
        """Генерация KPI"""
        return {
            'avg_speed': random.randint(40, 80),
            'active_incidents': random.randint(0, 10),
            'equipment_status': f"{random.randint(85, 99)}%",
            'traffic_flow': random.randint(500, 1500),
            'response_time': f"{random.randint(5, 20)} min"
        }
    
    @staticmethod
    def generate_traffic_lights():
        """Генерация данных о светофорах"""
        lights = []
        phases = ['Green', 'Yellow', 'Red']
        
        for i in range(1, 9):
            lights.append({
                'id': f'TL-{i:03d}',
                'location': f'Intersection {i}',
                'current_phase': random.choice(phases),
                'status': random.choice(['Operational', 'Maintenance', 'Warning']),
                'phase_duration': random.randint(30, 90),
                'last_update': (datetime.now() - timedelta(minutes=random.randint(1, 60))).strftime('%H:%M')
            })
        return lights

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 20px;
        color: white;
        text-align: center;
    }
    
    .incident-card {
        border-left: 5px solid;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        background-color: #f8f9fa;
    }
    
    .high-priority {
        border-left-color: #dc3545;
    }
    
    .medium-priority {
        border-left-color: #ffc107;
    }
    
    .low-priority {
        border-left-color: #28a745;
    }
    
    .traffic-light {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        margin: 5px;
        display: inline-block;
    }
    
    .green {
        background-color: #28a745;
        box-shadow: 0 0 10px #28a745;
    }
    
    .yellow {
        background-color: #ffc107;
        box-shadow: 0 0 10px #ffc107;
    }
    
    .red {
        background-color: #dc3545;
        box-shadow: 0 0 10px #dc3545;
    }
    
    .status-badge {
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-active {
        background-color: #d4edda;
        color: #155724;
    }
    
    .status-resolved {
        background-color: #cce5ff;
        color: #004085;
    }
    
    .status-false {
        background-color: #f8d7da;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🚦 Traffic Control Center")
    
    selected_page = st.radio(
        "Navigation",
        ["Dashboard", "Incident Management", "Traffic Light Control", "Analytics & Reports"]
    )
    
    st.markdown("---")
    

    st.subheader("System Status")
    st.info("🟢 All systems operational")
    

    st.subheader("Current Shift")
    st.markdown("**Operator:** John Doe")
    st.markdown("**Shift:** 08:00 - 20:00")
    

    st.markdown("---")
    st.subheader("Quick Actions")
    if st.button("🚨 Emergency Mode"):
        st.warning("Emergency mode activated!")
    if st.button("🔄 Refresh All Data"):
        st.rerun()

if selected_page == "Dashboard":
    st.markdown('<h1 class="main-header">🚦 Traffic Management Dashboard</h1>', unsafe_allow_html=True)
    

    traffic_system = TrafficSystem()
    kpis = traffic_system.generate_kpis()
    

    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("Avg Speed", f"{kpis['avg_speed']} km/h", "+2.3%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("Active Incidents", kpis['active_incidents'], "-1")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("Equipment Status", kpis['equipment_status'], "98%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("Traffic Flow", f"{kpis['traffic_flow']}/h", "+5.1%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("Avg Response Time", kpis['response_time'], "-3min")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    

    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("🗺️ City Traffic Map")
        
    
        fig = go.Figure(go.Scattermapbox(
            lat=[40.7128, 40.7580, 40.7549, 40.7489, 40.7689],
            lon=[-74.0060, -73.9855, -73.9840, -73.9680, -73.9819],
            mode='markers',
            marker=dict(
                size=15,
                color=['red', 'yellow', 'green', 'orange', 'purple'],
                opacity=0.8
            ),
            text=['Heavy Traffic', 'Moderate Traffic', 'Clear', 'Accident', 'Construction'],
            hoverinfo='text'
        ))
        
        fig.update_layout(
            mapbox=dict(
                style="carto-positron",
                zoom=10,
                center=dict(lat=40.7128, lon=-74.0060)
            ),
            height=500,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    
        legend_cols = st.columns(5)
        colors = ['red', 'orange', 'yellow', 'green', 'purple']
        labels = ['Heavy', 'Accident', 'Moderate', 'Clear', 'Construction']
        
        for idx, col in enumerate(legend_cols):
            with col:
                st.markdown(f'<div style="display: flex; align-items: center; gap: 10px;">'
                           f'<div style="width: 20px; height: 20px; background-color: {colors[idx]}; border-radius: 3px;"></div>'
                           f'<span>{labels[idx]}</span>'
                           f'</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("📋 Active Incidents")
        
        incidents = traffic_system.generate_incidents()
        active_incidents = [i for i in incidents if i['status'] in ['New', 'Confirmed']]
        
        for incident in active_incidents:
            priority_class = incident['priority'].lower().replace(' ', '-')
            
            with st.container():
                st.markdown(f'<div class="incident-card {priority_class}-priority">', unsafe_allow_html=True)
                
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"**{incident['id']}**")
                    st.caption(f"{incident['type']} • {incident['location']}")
                with cols[1]:
                    status_color = {
                        'New': 'status-active',
                        'Confirmed': 'status-resolved',
                        'False Alarm': 'status-false'
                    }.get(incident['status'], '')
                    st.markdown(f'<div class="status-badge {status_color}">{incident["status"]}</div>', 
                              unsafe_allow_html=True)
                
                st.markdown(f"*{incident['timestamp']} • Assigned to: {incident['assigned_to']}*")
                
            
                action_cols = st.columns(3)
                with action_cols[0]:
                    if st.button("👁️", key=f"view_{incident['id']}", help="View Details"):
                        st.session_state.selected_incident = incident['id']
                with action_cols[1]:
                    if st.button("✅", key=f"confirm_{incident['id']}", help="Confirm"):
                        st.success(f"Incident {incident['id']} confirmed!")
                with action_cols[2]:
                    if st.button("🚨", key=f"emergency_{incident['id']}", help="Call Emergency"):
                        st.warning(f"Emergency services dispatched to {incident['location']}")
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    

    st.subheader("📊 Traffic Density (24 Hours)")
    traffic_data = traffic_system.generate_traffic_data()
    
    fig = px.line(traffic_data, x='hour', y='traffic_density', 
                  title='',
                  labels={'hour': 'Hour of Day', 'traffic_density': 'Traffic Density (%)'})
    
    fig.update_layout(
        xaxis=dict(tickmode='linear', dtick=2),
        yaxis=dict(range=[0, 100]),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif selected_page == "Incident Management":
    st.markdown('<h1 class="main-header">🚨 Incident Management</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Incident List")
        
        incidents = TrafficSystem.generate_incidents()
        
    
        filter_cols = st.columns(3)
        with filter_cols[0]:
            status_filter = st.selectbox("Filter by Status", ["All", "New", "Confirmed", "Resolved", "False Alarm"])
        with filter_cols[1]:
            priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
        with filter_cols[2]:
            type_filter = st.selectbox("Filter by Type", ["All", "Accident", "Congestion", "Road Work", "Weather Alert"])
        
    
        filtered_incidents = incidents
        if status_filter != "All":
            filtered_incidents = [i for i in filtered_incidents if i['status'] == status_filter]
        if priority_filter != "All":
            filtered_incidents = [i for i in filtered_incidents if i['priority'] == priority_filter]
        if type_filter != "All":
            filtered_incidents = [i for i in filtered_incidents if i['type'] == type_filter]
        
    
        for incident in filtered_incidents:
            with st.expander(f"{incident['id']} - {incident['type']} ({incident['priority']} Priority)"):
                cols = st.columns(2)
                with cols[0]:
                    st.write(f"**Location:** {incident['location']}")
                    st.write(f"**Status:** {incident['status']}")
                with cols[1]:
                    st.write(f"**Time:** {incident['timestamp']}")
                    st.write(f"**Assigned:** {incident['assigned_to']}")
                
            
                action_cols = st.columns(4)
                with action_cols[0]:
                    if st.button("Confirm", key=f"confirm_det_{incident['id']}"):
                        st.success(f"Incident {incident['id']} confirmed as valid.")
                with action_cols[1]:
                    if st.button("False Alarm", key=f"false_{incident['id']}"):
                        st.info(f"Incident {incident['id']} marked as false alarm.")
                with action_cols[2]:
                    if st.button("Call Police", key=f"police_{incident['id']}"):
                        st.warning(f"Police dispatched to {incident['location']}")
                with action_cols[3]:
                    if st.button("Call Ambulance", key=f"ambulance_{incident['id']}"):
                        st.warning(f"Ambulance dispatched to {incident['location']}")
                
            
                status_update = st.selectbox("Update Status", 
                                           ["Select", "In Progress", "Resolved", "Escalated"], 
                                           key=f"status_{incident['id']}")
                if status_update != "Select":
                    st.info(f"Status updated to: {status_update}")
    
    with col2:
        st.subheader("🎥 Live Camera Feed")
        
    
        st.image("https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=800", 
                caption="Live feed from Camera #C001 - Main Intersection")
        
        st.markdown("**Camera Controls**")
        cam_cols = st.columns(2)
        with cam_cols[0]:
            if st.button("▶️ Play", use_container_width=True):
                st.info("Video playing...")
        with cam_cols[1]:
            if st.button("⏸️ Pause", use_container_width=True):
                st.info("Video paused")
        
        st.markdown("---")
        
        st.subheader("📝 New Incident Report")
        
        with st.form("new_incident_form"):
            incident_type = st.selectbox("Type", ["Accident", "Congestion", "Road Work", "Weather Alert", "Other"])
            location = st.text_input("Location", "Intersection 15, Main St.")
            priority = st.select_slider("Priority", ["Low", "Medium", "High"])
            description = st.text_area("Description", "Describe the incident...")
            
            submitted = st.form_submit_button("🚨 Report Incident")
            if submitted:
                st.success(f"New {priority} priority incident reported at {location}")
        
        st.markdown("---")
        
        st.subheader("📈 Incident Statistics")
        
        stats_data = {
            'Status': ['Active', 'Resolved', 'False Alarms', 'Total'],
            'Count': [len([i for i in incidents if i['status'] in ['New', 'Confirmed']]),
                     len([i for i in incidents if i['status'] == 'Resolved']),
                     len([i for i in incidents if i['status'] == 'False Alarm']),
                     len(incidents)]
        }
        
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)

elif selected_page == "Traffic Light Control":
    st.markdown('<h1 class="main-header">🚦 Traffic Light Control Panel</h1>', unsafe_allow_html=True)
    

    traffic_lights = TrafficSystem.generate_traffic_lights()
    light_ids = [light['id'] for light in traffic_lights]
    
    selected_light_id = st.selectbox("Select Traffic Light", light_ids)
    selected_light = next((light for light in traffic_lights if light['id'] == selected_light_id), None)
    
    if selected_light:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"🚦 {selected_light['id']} - {selected_light['location']}")
            
        
            st.markdown("### Intersection Diagram")
            
        
            st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
            
        
            phase_colors = {
                'Green': 'green',
                'Yellow': 'yellow',
                'Red': 'red'
            }
            
            current_color = phase_colors.get(selected_light['current_phase'], 'gray')
            
            st.markdown(f'''
            <div style="display: flex; flex-direction: column; align-items: center; gap: 10px;">
                <div class="traffic-light {current_color}"></div>
                <div style="font-size: 1.2rem; font-weight: bold;">{selected_light['current_phase']}</div>
                <div style="color: #666;">Duration: {selected_light['phase_duration']} seconds</div>
            </div>
            ''', unsafe_allow_html=True)
            
        
            st.markdown("### Phase Timeline")
            
            phases_data = {
                'Phase': ['Green', 'Yellow', 'Red'],
                'Duration': [selected_light['phase_duration'] - 10, 5, 10]
            }
            
            fig = px.bar(phases_data, x='Phase', y='Duration', 
                        color='Phase',
                        color_discrete_map={'Green': 'green', 'Yellow': 'yellow', 'Red': 'red'})
            
            fig.update_layout(
                height=300,
                showlegend=False,
                yaxis_title="Duration (seconds)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Manual Controls")
            
        
            st.markdown("#### Manual Phase Control")
            
            manual_phase = st.selectbox("Select Phase", ["Green", "Yellow", "Red"], 
                                      key="manual_phase")
            manual_duration = st.slider("Duration (seconds)", 5, 180, 30)
            
            if st.button("⚡ Apply Phase", use_container_width=True):
                st.success(f"Phase set to {manual_phase} for {manual_duration} seconds")
            
            st.markdown("---")
            
        
            st.markdown("#### Special Modes")
            
            mode_cols = st.columns(2)
            with mode_cols[0]:
                if st.button("🟡 Flashing Yellow", use_container_width=True):
                    st.warning("Flashing yellow mode activated")
            with mode_cols[1]:
                if st.button("🔴 All Red", use_container_width=True):
                    st.error("All red mode activated - intersection closed")
            
            st.markdown("---")
            
        
            st.markdown("#### Light Status")
            
            status_info = {
                'ID': selected_light['id'],
                'Location': selected_light['location'],
                'Current Phase': selected_light['current_phase'],
                'Status': selected_light['status'],
                'Last Update': selected_light['last_update'],
                'Uptime': f"{random.randint(95, 100)}%"
            }
            
            for key, value in status_info.items():
                st.markdown(f"**{key}:** {value}")
            
            if st.button("🔄 Refresh Status", use_container_width=True):
                st.rerun()
    
    st.markdown("---")
    

    st.subheader("All Traffic Lights")
    
    lights_df = pd.DataFrame(traffic_lights)
    

    def status_style(val):
        color = {
            'Operational': 'green',
            'Maintenance': 'orange',
            'Warning': 'red'
        }.get(val, 'gray')
        return f'color: {color}; font-weight: bold'
    
    st.dataframe(
        lights_df.style.applymap(status_style, subset=['status']),
        use_container_width=True,
        hide_index=True
    )

elif selected_page == "Analytics & Reports":
    st.markdown('<h1 class="main-header">📊 Analytics & Reports</h1>', unsafe_allow_html=True)
    

    st.subheader("📅 Filters")
    
    filter_cols = st.columns(4)
    
    with filter_cols[0]:
        time_period = st.selectbox("Time Period", ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Custom"])
    
    with filter_cols[1]:
        if time_period == "Custom":
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
    
    with filter_cols[2]:
        zone = st.multiselect("City Zone", ["Downtown", "Suburbs", "Industrial", "Residential", "All"])
    
    with filter_cols[3]:
        metric = st.selectbox("Metric", ["Traffic Density", "Incident Count", "Average Speed", "Response Time"])
    

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Traffic Patterns")
        
    
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        traffic_pattern = [random.randint(60, 95) for _ in range(7)]
        
        fig = px.line(x=days, y=traffic_pattern, 
                     labels={'x': 'Day of Week', 'y': 'Traffic Density (%)'},
                     title="Weekly Traffic Pattern")
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Incident Analysis")
        
    
        incident_types = ['Accident', 'Congestion', 'Road Work', 'Weather Alert']
        incident_counts = [random.randint(5, 20) for _ in range(4)]
        
        fig = px.pie(values=incident_counts, names=incident_types,
                    title="Incidents by Type")
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    

    st.subheader("📋 Detailed Analytics")
    

    hours = list(range(24))
    detailed_data = {
        'Hour': hours,
        'Traffic_Density': [random.randint(30, 100) for _ in hours],
        'Avg_Speed': [random.randint(40, 80) for _ in hours],
        'Incident_Count': [random.randint(0, 5) for _ in hours],
        'Response_Time': [random.randint(5, 25) for _ in hours]
    }
    
    detailed_df = pd.DataFrame(detailed_data)
    

    selected_metric = st.selectbox("Select Metric to Display", 
                                  ["Traffic_Density", "Avg_Speed", "Incident_Count", "Response_Time"])
    
    fig = px.bar(detailed_df, x='Hour', y=selected_metric,
                title=f"Hourly {selected_metric.replace('_', ' ')}")
    
    fig.update_layout(
        height=400,
        xaxis=dict(tickmode='linear', dtick=2)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    

    with st.expander("📄 View Raw Data"):
        st.dataframe(detailed_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    

    st.subheader("📥 Export Reports")
    
    export_cols = st.columns(4)
    
    with export_cols[0]:
        report_type = st.selectbox("Report Type", 
                                  ["Daily Summary", "Weekly Analysis", "Monthly Report", "Incident Log"])
    
    with export_cols[1]:
        export_format = st.selectbox("Format", ["PDF", "Excel", "CSV", "JSON"])
    
    with export_cols[2]:
        include_charts = st.checkbox("Include Charts", value=True)
    
    with export_cols[3]:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📤 Generate & Export", use_container_width=True):
            st.success(f"Report generated in {export_format} format!")
            
        
            report_data = detailed_df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download Report",
                data=report_data,
                file_name=f"traffic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_format.lower()}",
                mime="text/csv" if export_format == "CSV" else 
                     "application/vnd.ms-excel" if export_format == "Excel" else
                     "application/json" if export_format == "JSON" else
                     "application/pdf"
            )
    

    st.markdown("---")
    st.subheader("📊 Performance Metrics")
    
    perf_metrics = {
        'Metric': ['System Uptime', 'Avg Response Time', 'Incident Resolution Rate', 
                  'Traffic Flow Improvement', 'Equipment Reliability'],
        'Value': ['99.8%', '12.5 min', '94.3%', '+7.2%', '98.5%'],
        'Target': ['99.5%', '15 min', '90%', '+5%', '95%'],
        'Status': ['✅ Exceeds', '✅ Meets', '✅ Exceeds', '✅ Exceeds', '✅ Exceeds']
    }
    
    perf_df = pd.DataFrame(perf_metrics)
    st.dataframe(perf_df, use_container_width=True, hide_index=True)

st.markdown("---")
footer_cols = st.columns(3)
with footer_cols[0]:
    st.markdown("**Traffic Management System v2.0**")
with footer_cols[1]:
    st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
with footer_cols[2]:
    st.markdown("© 2024 Smart City Traffic Control")