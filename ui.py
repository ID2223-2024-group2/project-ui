import pandas as pd
import streamlit as st
import ui_helpers
import datetime
import hopsworks
import os

import ui_hindcast
import ui_inference
import ui_weather
from shared.constants import get_relative_static_url

st.set_page_config(
    page_title="Gävleborg Transit Delay Forecast",
    page_icon="🐐"
)

st.title("🐐 Gävleborg Transit Delay Forecast")
st.write("*A snow-accelerated real-time delay estimator.*")

SHOW_TABLES = False

@st.cache_resource(show_spinner="Connecting to Hopsworks")
def get_project():
    hopsworks_api_key = os.environ["HOPSWORKS_API_KEY"]
    return hopsworks.login(api_key_value=hopsworks_api_key, project="TSEDMID2223")


project = get_project()
tab_predict, tab_data, tab_evaluate = st.tabs(["Forecast", "Data", "Historical Accuracy"])

# Fetch the current weather description before the selectbox
weather_df, weather_icons = ui_weather.get_current_weather_df()
current_weather_description = weather_icons[0].description

current_weather_predictions = pd.DataFrame()

with tab_predict:
    col1, col2 = st.columns(2)
    transport_options = {"🚂 Train": "Train", "🚌 Bus": "Bus"}
    weather_options = {
        f"{weather_icons[0].to_emoji()} Actual Current Weather": "Current",
        "☀️ Clear*": "Clear",
        "💨 Windy*": "Windy",
        "🌨️ Snow*": "Snow"
    }

    with col1:
        transport_string = st.selectbox("Mode of transportation", options=list(transport_options.keys()), key="transport_string")
        transport_mode = transport_options[transport_string]

    with col2:
        weather_condition = st.selectbox("Weather condition", options=list(weather_options.keys()), key="weather_condition")
        weather_condition = weather_options[weather_condition]

    prediction_df = ui_inference.inference(project, transport_mode, weather_condition)
    if weather_condition == "Current":
        current_weather_predictions = prediction_df.copy()

    if SHOW_TABLES:
        with st.expander("Show Delay Forecast Table"):
            st.dataframe(prediction_df)

    delay, on_time, date = ui_helpers.get_current_prediction_values(prediction_df)
    delay_trend, on_time_trend = ui_helpers.get_prediction_trends(prediction_df)

    st.text("")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Estimated Avg. Arrival Delay", ui_helpers.seconds_to_minute_string(delay),
                  delta=ui_helpers.seconds_to_minute_string(delay_trend), delta_color="inverse")
    with col2:
        st.metric("Estimated On Time Percentage\*\*", f"{on_time:.1f}%", delta=f"{on_time_trend:.1f}%")
    st.write("*All metrics are per-stop; Trends are calculated based on previous hour(s)*")

    st.write("#### Weather Forecast")
    st.write("Predictions from [Open-Meteo](https://open-meteo.com); Icons via [OpenWeather](https://openweathermap.org)")

    st.markdown(
        f"""
        <div style="background-color: #f0f0f010; padding: 10px; border-radius: 5px; margin-bottom: 10px">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="flex: 1; text-align: center;">
                    <strong>Current ({ui_helpers.get_hour_range(weather_df.iloc[0]["date"])})</strong>
                </div>
                <div style="flex: 1; text-align: center;">
                    <strong>Upcoming ({ui_helpers.get_hour_range(weather_df.iloc[1]["date"])})</strong>
                </div>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="flex: 2; text-align: center;">
                    <img src="{weather_icons[0].open_weather_icon_url}" width="128">
                </div>
                <div style="flex: 4; font-size: 1.1em; text-align: center;">
                    {weather_icons[0].description}
                </div>
                <div style="flex: 0.1; height: 60px; border-left: 1px solid #ccc; margin: 0 10px;"></div>
                <div style="flex: 2; text-align: center;">
                    <img src="{weather_icons[1].open_weather_icon_url}" width="128">
                </div>
                <div style="flex: 4; font-size: 1.1em; text-align: center;">
                    {weather_icons[1].description}
                </div>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 10px;">
        """,
        unsafe_allow_html=True
    )

    if SHOW_TABLES:
        with st.expander("Show Weather Forecast Table"):
           st.dataframe(weather_df)

    st.divider()
    st.write("*\* If selected, weather conditions for the current time interval are replaced with simulated values*")
    st.write("*\*\* Transport is on-time if it arrives within 3 minutes before or 5 minutes after its scheduled time.*")
    st.write("Delay forecasts are generated every quarter-hour, but may take a few minutes to appear. "
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
        what_mode = st.selectbox("Mode of transportation", options=["Train", "Bus"], key="what_mode")
    with col2:
        st.write("")
        st.write("")
        interpolate_values = st.checkbox("Interpolate missing values*", value=True)
    # with col2:
    #     possibilities_labels = ["Arrival Delay", "On Time %"]
    #     possibilities_cols = ["predicted_mean_on_time_percent", "predicted_mean_arrival_delay_seconds"]
    #     what_data = st.multiselect("Series",
    #                                options=possibilities_cols,
    #                                default=possibilities_cols,
    #                                format_func=lambda label: possibilities_labels[possibilities_cols.index(label)])
    how_far = st.slider("Number of datapoints", min_value=80, max_value=800, value=100)
    hindcast_delay, reindexed_df = ui_hindcast.hindcast(project, what_mode, how_far)

    if not interpolate_values:
        hindcast_delay = reindexed_df

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

    st.write("\* Data can be missing during times with no transit service (e.g. nights, trains outside of rush-hours). ")