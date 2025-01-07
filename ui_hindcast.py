import streamlit as st
import datetime

import ui_helpers

TTL = 60 * 60
FV_VERSION = 1


@st.cache_data(ttl=TTL, show_spinner="Preparing hindcast data")
def hindcast(_project, transport_string, datapoints):
    now = datetime.datetime.now()
    yesterday_midnight = datetime.datetime(now.year, now.month, now.day) - datetime.timedelta(days=1)
    df = download_all_data(_project)
    df = df.tail(datapoints)
    df = df[df["route_type"] == ui_helpers.transport_int(transport_string)]
    df["arrival_time_bin"] = df["arrival_time_bin"].dt.tz_convert(None)
    df = df[df["arrival_time_bin"] <= yesterday_midnight]
    return df


@st.cache_data(ttl=TTL, show_spinner="Downloading hindcast data")
def download_all_data(_project):
    fs = _project.get_feature_store("tsedmid2223_featurestore")
    fv = fs.get_feature_view("monitor_fv", FV_VERSION)
    df = fv.get_batch_data()
    df.sort_values(by=["arrival_time_bin"], inplace=True, ascending=True)
    return df
