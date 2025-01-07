import pandas as pd
import streamlit as st
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import os
import requests
import time

import ui_helpers
import weather.simulated as ws

MODEL_VERSION = 3
FV_VERSION = 7
TTL = 5 * 60
TREND_WINDOW = 2

GIT_OWNER = "ID2223-2024-group2"
GIT_REPO = "project"
GIT_WORKFLOW = "regular-update.yml"
GIT_REF = "main"
GIT_BASE_URL = f"https://api.github.com/repos/{GIT_OWNER}/{GIT_REPO}"


@st.cache_data(ttl=TTL, show_spinner="Running inference")
def inference(_project, transport_string: str, weather_condition: str) -> pd.DataFrame:
    infer, feature_scaler, label_scaler = download_model(_project)
    last_entries = download_last_entries(_project, transport_string, last_entries=TREND_WINDOW)
    if weather_condition != "Current":
        last_entries = ws.simulate_weather(last_entries, weather_condition)

    delay, on_time = run_inference(infer, feature_scaler, label_scaler, last_entries)

    prediction_df = last_entries.copy()
    prediction_df.sort_values(by=["arrival_time_bin"], inplace=True, ascending=True)
    prediction_df["predicted_delay"] = delay
    prediction_df["predicted_on_time"] = on_time
    return prediction_df


@st.cache_resource(show_spinner="Downloading AI model")
def download_model(_project):
    mr = _project.get_model_registry()
    hw_model = mr.get_model(name="keras", version=MODEL_VERSION)
    where_model = hw_model.download()
    loaded_model = tf.saved_model.load(where_model)
    feature_scaler = StandardScaler()
    feature_scaler.mean_ = loaded_model.x_scaler[0]
    feature_scaler.scale_ = loaded_model.x_scaler[1]
    label_scaler = StandardScaler()
    label_scaler.mean_ = loaded_model.y_scaler[0]
    label_scaler.scale_ = loaded_model.y_scaler[1]
    infer = loaded_model.signatures["serving_default"]
    return infer, feature_scaler, label_scaler


@st.cache_data(ttl=TTL, show_spinner="Downloading data")
def download_all_data(_project):
    fs = _project.get_feature_store("tsedmid2223_featurestore")
    fv = fs.get_feature_view("delays_fv", FV_VERSION)
    df = fv.get_batch_data()
    df.sort_values(by=["arrival_time_bin"], inplace=True, ascending=False)
    return df


@st.cache_data(ttl=TTL, show_spinner="Preparing data")
def download_last_entries(_project, transport_string, last_entries=1):
    df = download_all_data(_project)
    correct_transport = df[df["route_type"] == ui_helpers.transport_int(transport_string)]
    last = correct_transport.head(last_entries)
    return last


def run_inference(infer, feature_scaler, label_scaler, last_entries):
    stripped = ui_helpers.strip_dates(last_entries)
    useful = stripped[ui_helpers.TO_USE]
    one_hotted = ui_helpers.one_hot(useful)
    feature = tf.dtypes.cast(feature_scaler.transform(one_hotted), tf.float32)
    predictions = infer(feature)["output_0"]
    values = label_scaler.inverse_transform(predictions)
    delays = values[:, 0]
    on_times = values[:, 1]
    return delays, on_times


def github_headers():
    github_token = os.environ["GITHUB_TOKEN"]
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github+json"
    }
    return headers


def github_workflow_running_now(headers):
    url = f"{GIT_BASE_URL}/actions/runs"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    runs = response.json()["workflow_runs"]
    for run in runs:
        if run["head_branch"] == GIT_REF:
            return run["conclusion"] is None


def github_workflow_trigger(headers):
    url = f"{GIT_BASE_URL}/actions/workflows/{GIT_WORKFLOW}/dispatches"
    response = requests.post(url, headers=headers, json={"ref": GIT_REF})
    response.raise_for_status()


def github_workflow_wait(headers):
    with st.spinner("Waiting for pipeline re-run eligibility..."):
        while github_workflow_running_now(headers):
            time.sleep(5)
        download_all_data.clear()
        download_last_entries.clear()
