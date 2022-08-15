import streamlit as st
import pandas as pd
import plotly_express as px

from datetime import date
from plotly import graph_objs as go
from PIL import Image as img


# --- Helpful Variables ---

# Image Oaths
title_dashboard_logo = 'dash_small.png'
sidebar_streamlit_logo = 'streamlit-logo-nbg.png'
main_waiting_logo = 'Waiting.png'

information_text = "This web application designed to present & visualize performance metrics of specific CSV data set ('merged_sorted.csv') present in the Git repo. To view the data in full-screen please click the button on top-right of each widget.  Your feedback is much awaited. Thankyou for giving the opprotunity to do something new."
data_display_text = "The columns, rows & values were not formatted or truncated to keep dataset authenticity. However, the data-set was altered to retain only useful information & decrease load times. Also, not HTML CSS elements were used to keep the usage of streamlit as a priority."

lottie_anim_hello = 'https://assets9.lottiefiles.com/packages/lf20_49rdyysj.json'


# --- Utility Functions ---

# File Uploading Section
def upload_data():
    file = st.file_uploader(
        "Please upload csv file to continue...", type="csv")
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.text(f"")

# Filters & displays data according to selected function


def load_selected_function(selected_function):
    df_selected_function = df_uploaded.query("Function == @selected_function")

    return df_selected_function

# Calculates meta data for overall performance (Data unformatted to keep authenticity)


def calculate_metadata(df_any):
    total_time = int(df_any['Time'].sum())
    min_time = float(df_any['Time'].min())
    max_time = float(df_any['Time'].max())
    avg_time = float(df_any['Time'].mean())

    st.text(f"  Total Time:    {total_time} s")
    st.text(f"Average Time:    {avg_time} s")
    st.text(f"Maximum Time:    {max_time} s")
    st.text(f"Minimum Time:    {min_time} s")

# Plots min,max,mean,sum of each function in the entire uploaded data-set


def plot_uploaded_data(df_uploaded, op_choice):
    if op_choice == 1:
        df_grouped_function_time = df_uploaded.groupby(by=['Function']).max()[
            ['Time']].sort_values(by=['Function'])
    elif op_choice == 2:
        df_grouped_function_time = df_uploaded.groupby(by=['Function']).min()[
            ['Time']].sort_values(by=['Function'])
    elif op_choice == 3:
        df_grouped_function_time = df_uploaded.groupby(by=['Function']).max()[
            ['Time']].sort_values(by=['Function'])
    elif op_choice == 4:
        df_grouped_function_time = df_uploaded.groupby(by=['Function']).max()[
            ['Time']].sort_values(by=['Function'])

    fig_grouped_function_time = px.bar(df_grouped_function_time, x='Time', y=df_grouped_function_time.index, orientation='h', color_discrete_sequence=[
                                       "#0083B8"] * len(df_grouped_function_time), template='plotly_white')
    fig_grouped_function_time.layout.update(xaxis_rangeslider_visible=True)

    st.plotly_chart(fig_grouped_function_time)

# Plots the data for the selected function from the select-box


def plot_selected_data(df_selected_function):
    fig_selected_function = go.Figure()
    fig_selected_function.add_trace(go.Scatter(
        x=df_selected_function['time_stamp'], y=df_selected_function['Time'], name='time(s)'))
    fig_selected_function.layout.update(xaxis_rangeslider_visible=True, xaxis=(dict(
        showgrid=False)), yaxis=(dict(showgrid=False)), plot_bgcolor="rgba(0,0,0,0)",)

    st.plotly_chart(fig_selected_function, use_container_width=True)


# --- WEB PAGE SETTINGS & MAIN CODE ---

# Page Layout Settings
st.set_page_config(page_title='Data Visualizer',
                   page_icon=':bar_chart:', layout='wide')

left_column_page, right_column_page = st.columns(2)
with left_column_page:
    st.title(":bar_chart: Data Visualizer")
    st.markdown(information_text)
    st.markdown(data_display_text)


with right_column_page:
    dashboard_logo = img.open(title_dashboard_logo)
    st.image(dashboard_logo)


# File Upload Section
with st.sidebar:
    streamlit_logo = img.open(sidebar_streamlit_logo)

    st.image(streamlit_logo)
    st.title("streamlit - Data Visualizer")
    st.markdown("##")

    st.header(":open_file_folder: Upload File")
    df_uploaded = upload_data()


# Data display & overall metrics display
st.markdown("---")
if df_uploaded is not None:
    st.header(":bar_chart: Dataset Analysis")

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader(":open_file_folder:File Opened 'merged_sorted.csv'")
        st.dataframe(df_uploaded)

    with right_column:
        st.subheader(":clipboard:Overall Performance Metrics")
        st.markdown("##")

        calculate_metadata(df_uploaded)
else:

    waiting_logo = img.open(main_waiting_logo)

    st.subheader("Waiting For File...!")
    st.image(waiting_logo)
    # st_lottie(load_lottie(lottie_anim_hello), key='hello') Note: doesnt work with url or json


# Data plot of Maximum & Minimum time taken by each function
if df_uploaded is not None:
    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader(":chart_with_upwards_trend:Maximum Time Of Each Function")
        plot_uploaded_data(df_uploaded, 1)

    with right_column:
        st.subheader(":chart_with_upwards_trend:Minimum Time Of Each Function")
        plot_uploaded_data(df_uploaded, 2)


# Data plot of Maximum & Minimum time taken by each function
if df_uploaded is not None:
    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader(":chart_with_upwards_trend:Total Time Of Each Function")
        plot_uploaded_data(df_uploaded, 3)

    with right_column:
        st.subheader(":chart_with_upwards_trend:Mean Time Of Each Function")
        plot_uploaded_data(df_uploaded, 4)

    st.markdown("---")


# Display filter according to selected function
if df_uploaded is not None:

    with st.sidebar:
        st.header(":open_file_folder: Select Function")

        selected_function = st.selectbox(
            "Please select a function for analysis...", df_uploaded["Function"].unique())

        df_selected_function = load_selected_function(selected_function)

    st.header(":bar_chart: Filter Data By Function")


# Data display & overall metrics display
if df_uploaded is not None:
    left_column_selection, right_column_selection = st.columns(2)

    with left_column_selection:
        st.subheader(f":open_file_folder: Function '{selected_function}'")
        st.dataframe(df_selected_function)

    with right_column_selection:
        st.subheader(":clipboard:Overall Performance Metrics")
        st.markdown("##")

        calculate_metadata(df_selected_function)

    # Data plot of Function;s Time vs Timestamp
if df_uploaded is not None:
    st.subheader(":chart_with_upwards_trend:Time vs TimeStamp")
    plot_selected_data(df_selected_function)

    st.markdown("---")
