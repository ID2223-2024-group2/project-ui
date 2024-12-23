import streamlit as st
import ui_helpers
import datetime
import hopsworks
import os

import ui_hindcast
import ui_inference

st.title("🐐 Gävleborg Train Delay Forecast")
st.write("*A snow-accelerated real-time delay estimator.*")


@st.cache_resource(show_spinner="Connecting to Hopsworks")
def get_project():
    hopsworks_api_key = os.environ["HOPSWORKS_API_KEY"]
    return hopsworks.login(api_key_value=hopsworks_api_key, project="TSEDMID2223")


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
    if st.checkbox("Enabled real-time data? This may freeze the UI during pipeline runs."):
        github_headers = ui_inference.github_headers()
        ui_inference.github_workflow_wait(github_headers)
        if st.button("Download and use real-time data", type="primary"):
            ui_inference.github_workflow_trigger(github_headers)
            st.rerun()


with tab_evaluate:
    col1, col2 = st.columns(2)
    with col1:
        what_mode = st.selectbox("Mode of transportation", options=["Train", "Bus"], key="bar")
    # with col2:
    #     possibilities_labels = ["Arrival Delay", "On Time %"]
    #     possibilities_cols = ["predicted_mean_on_time_percent", "predicted_mean_arrival_delay_seconds"]
    #     what_data = st.multiselect("Series",
    #                                options=possibilities_cols,
    #                                default=possibilities_cols,
    #                                format_func=lambda label: possibilities_labels[possibilities_cols.index(label)])
    how_far = st.slider("Number of datapoints", min_value=1, max_value=300, value=50)
    hindcast_delay = ui_hindcast.hindcast(project, what_mode, how_far)
    st.markdown("### Average Arrival Delay")
    renamed_delay = {
        "predicted_mean_arrival_delay_seconds": "Predicted",
        "mean_arrival_delay_seconds": "Actual"
    }
    st.line_chart(hindcast_delay.rename(columns=renamed_delay),
                  x="arrival_time_bin",
                  y=["Predicted", "Actual"],
                  x_label="Time",
                  y_label=["Delay (s)"])
    st.markdown("### On Time Percentage")
    renamed_on_time = {
        "predicted_mean_on_time_percent": "Predicted",
        "mean_on_time_percent": "Actual"
    }
    st.line_chart(hindcast_delay.rename(columns=renamed_on_time),
                  x="arrival_time_bin",
                  y=["Predicted", "Actual"],
                  x_label="Time",
                  y_label="Percentage (%)")
