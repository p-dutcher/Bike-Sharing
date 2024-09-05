###################### Import Libraries ####################

import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt 

################### Configure Dashboard ###################

st.set_page_config(page_title = 'CitiBike NYC Analysis (2022)', layout='wide')
st.markdown("This dashboard identifies trends in rider activity in order to develop a strategic growth plan for CitiBike in NYC")

################### Import Data ###########################

df = pd.read_csv('/Users/piperdutcher/Documents/Data-Visualizations/Bike-Sharing/Data/FINAL DATA SETS/final_SAMPLE_set.csv', index_col = 0)
top20start = pd.read_csv('/Users/piperdutcher/Documents/Data-Visualizations/Bike-Sharing/Data/FINAL DATA SETS/top20starting_stations.csv', index_col = 0)
top20end = pd.read_csv('/Users/piperdutcher/Documents/Data-Visualizations/Bike-Sharing/Data/FINAL DATA SETS/top20ending_stations.csv', index_col = 0)
df_ridecounts_temp = pd.read_csv('/Users/piperdutcher/Documents/Data-Visualizations/Bike-Sharing/Data/FINAL DATA SETS/Daily_ride_counts_ONLY.csv', index_col = 0)

################### Define Charts ###############################

## Bar Chart (Top 20 Starting Stations)

fig = go.Figure(go.Bar(x = top20start['start_station_name'],
                       y = top20start['start_value'],
                       marker = {'color':top20start['start_value'], 'colorscale' : 'cividis'}
                      ))
fig.update_layout(
     title = 'Top 20 Starting Stations in NYC (2022)',
     xaxis_title = 'Start Stations',
     yaxis_title = 'Sum of Trips',
    plot_bgcolor='white',
     width = 900, height = 600)
st.plotly_chart(fig, use_container_width = True)

## Bar Chart (Top 20 Ending Stations)

fig2 = go.Figure(go.Bar(x = top20end['end_station_name'],
                       y = top20end['end_value'],
                       marker = {'color':top20start['start_value'], 'colorscale' : 'cividis'}
                      ))
fig2.update_layout(
     title = 'Top 20 Ending Stations in NYC (2022)',
     xaxis_title = 'End Stations',
     yaxis_title ='Sum of Trips',
    plot_bgcolor='white',
     width = 900, height = 600)
st.plotly_chart(fig2, use_container_width = True)

## Dual Axis Chart (Daily Avg Temp and Bike Ride Count)

fig3 = make_subplots(specs = [[{"secondary_y" : True}]])
fig3.add_trace(
    go.Scatter(x = df_temp['date'],
    y = df_temp['daily_ride_count'],
    name = "Daily Ride Count",
    marker = {'color' : 'steelblue'}),
    secondary_y = False) # false, as this is our FIRST y-axis
fig3.add_trace(
    go.Scatter(x = df_temp['date'],
               y = df_temp['average_temp'],
               name = "Average Daily Temperature",
               marker = {'color' : 'goldenrod'}),
    secondary_y = True)
fig3.update_layout(
     title = 'Daily Average Temperature and Daily Ride Count (NYC 2022)',
     xaxis_title = 'Date',
     width = 1300, height = 700,
    plot_bgcolor='white')
fig3.update_yaxes(title_text='Sum of Trips', secondary_y=False)
fig3.update_yaxes(title_text='Temperature', secondary_y=True)
t.plotly_chart(fig3, use_container_width=True)

#################### More Stuff to Come ###################