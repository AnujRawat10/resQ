import streamlit as st
import requests
import pandas as pd

# Backend URL
backend_url = "http://127.0.0.1:8080"

# Page Configuration
st.set_page_config(page_title="Admin Panel - Disaster Mapping", layout="wide")

# Title
st.title("Admin Panel - Crowdsourced Disaster Mapping")

# Function to fetch reports
def fetch_reports():
    try:
        response = requests.get(f"{backend_url}/user/reports/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch reports.")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []

# Function to update report status
def update_status(report_id, new_status):
    try:
        response = requests.put(
            f"{backend_url}/admin/report/{report_id}/status",
            json={"status": new_status}
        )
        if response.status_code == 200:
            st.success("Status updated successfully.")
        else:
            st.error("Failed to update status.")
    except Exception as e:
        st.error(f"Error: {e}")

# Fetch and Display Reports
st.subheader("All Reports")
reports = fetch_reports()

if reports:
    # Convert to DataFrame for better display and manipulation
    df = pd.DataFrame(reports)
    
    # Displaying reports in a table
    st.dataframe(df[['id', 'image_filename', 'latitude', 'longitude', 'location', 'description', 'status']])
    
    # Displaying coordinates on a map
    st.subheader("Reports Map")
    st.map(df[['latitude', 'longitude']])

    # Status Update Section
    st.subheader("Update Report Status")
    report_id = st.selectbox("Select Report ID:", df['id'])
    new_status = st.selectbox("New Status:", ["not_resolved", "in_progress", "resolved"])
    if st.button("Update Status"):
        update_status(report_id, new_status)
else:
    st.info("No reports available.")
