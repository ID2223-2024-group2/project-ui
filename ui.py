import streamlit as st
import ui_helpers
import datetime
import pandas as pd
import numpy as np
import hopsworks
import os
import time

import ui_inference

st.title("🐐 Gävleborg Train Delay Forecast")
st.write("*A snow-accelerated real-time delay estimator.*")


@st.cache_resource(show_spinner="Connecting to Hopsworks")
def get_project():
    hopsworks_api_key = os.environ.get("HOPSWORKS_API_KEY", open(".hw_key").read().strip())
    return hopsworks.login(api_key_value=hopsworks_api_key)


project = get_project()
tab_predict, tab_data, tab_evaluate = st.tabs(["Forecast", "Data", "Historical Accuracy"])


with tab_predict:
    col1, _ = st.columns(2)
    with col1:
        transport_string = transport_mode = st.selectbox("Mode of transportation", options=["Train", "Bus"], key="foo")
    delay, on_time, date = ui_inference.inference(project, transport_mode)
    st.text("")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Estimated Avg. Arrival Delay", ui_helpers.seconds_to_minute_string(delay))
    with col2:
        st.metric("Estimated On Time Percentage", f"{on_time:.1f}%")
    st.write("*Transport is on-time if it arrives within 3 minutes before or 5 minutes after its scheduled time.*")
    st.divider()
    st.write("Forecasts are generated every quarter-hour, but may take a few minutes to appear. "
             "Predictions may not reflect reality. All data is given as-is without guarantees.")

with tab_data:
    interval_start = ui_helpers.get_interval(date)
    interval_end = ui_helpers.get_interval(date + datetime.timedelta(hours=1), full=True)
    st.write(f"Using data from the interval {interval_start} to {interval_end}.")
    st.text("Real-time data triggers the batch ingestion GitHub Actions pipeline manually. "
            "While the pipeline is running, it cannot manually be re-triggered. "
            "Pipeline runs usually take 5 minutes.")
    github_headers = ui_inference.github_headers()
    ui_inference.github_workflow_wait(github_headers)
    if st.button("Download and use real-time data", type="primary"):
        ui_inference.github_workflow_trigger(github_headers)
        st.rerun()


with tab_evaluate:
    col1, col2 = st.columns(2)
    with col1:
        what_mode = st.selectbox("Mode of transportation", options=["Train", "Bus"], key="bar")
    with col2:
        what_data = st.pills("Chart elements to show", ["Actual", "Predicted"], selection_mode="multi")
    st.text("")
    if len(what_data) > 0:
        st.text("hi")
