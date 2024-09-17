###################### Import Libraries ####################

import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt 
from numerize.numerize import numerize
from PIL import Image
import os

################### Configure Dashboard ###################

st.set_page_config(page_title = 'CitiBike NYC Analysis (2022)',layout='wide')

# Drop Down Menu #

page = st.sidebar.selectbox('Analysis Detail',
   ["Introduction", "Riders & Rideables", "Weather Impact on Rider Activity",
  "Popular Stations",
     "Interactive Map with NYC Landmarks and Ride Paths", "Interactive Map with Citibike Stations", "Recommendations", "Conclusion"])

################### Import Data ###########################

# Get the directory of the current script (will need for streamlit)
script_dir = os.path.dirname(__file__) 

# define paths for data
data_path = os.path.join(script_dir, 'Data/FINAL DATA SETS', 'Final_Sample.csv')
daily_ride_counts_path = os.path.join(script_dir, 'Data/FINAL DATA SETS', 'Daily_ride_counts_ONLY.csv')
member_types_path = os.path.join(script_dir, 'Data/FINAL DATA SETS', 'member_types.csv')
rideable_types_path = os.path.join(script_dir, 'Data/FINAL DATA SETS', 'rideable_types.csv')
trip_length_seasons_path = os.path.join(script_dir, 'Data/FINAL DATA SETS', 'trip_length_seasons.csv')

# Read the CSV files
df = pd.read_csv(data_path, index_col=0)
df_temp = pd.read_csv(daily_ride_counts_path, index_col=0)
member_types = pd.read_csv(member_types_path, index_col=0)
rideable_types = pd.read_csv(rideable_types_path, index_col=0)
trip_length_seasons = pd.read_csv(trip_length_seasons_path, index_col=0)

################### Introduction ##################################

if page == "Introduction":
    st.header("Citibike NYC Analysis Dashboard")
    st.markdown("This purpose of this dashboard is to identify trends in rider activity to aid in the development of business strategies.")
    st.markdown("The primary pain point is limited bicycle availabity. This analysis encompasses several factors that can impact aforementioned availability and proposes recommendations to facilitate CitiBike's success in the future. These include:")
    st.markdown("- Rider and Rideable Profiles")
    st.markdown("- Weather Impact on Rider Activity")
    st.markdown("- Popular Stations with Seasonal Impact")
    st.markdown(" - Interactive Map with Top Ride Paths and NYC Landmarks")
    st.markdown(" - Interactive Map with Citibike Stations")
    st.markdown(" - Recommendations")
    st.markdown("The dropdown menu on the left can be utilized to view different aspects of the analysis and recommendations page.")


    # Define path
    intro_image_path = os.path.join(script_dir, 'Images', 'CitiBike.jpg')

    # Open the image
    intro_image = Image.open(intro_image_path)

    # Resize
    resized_image = intro_image.resize((1150, 500))

    # Display
    st.image(resized_image)

################### Rider Profile Page ##################################

elif page == "Riders & Rideables":
    st.header("General Composition of Rider and Rideable Types")
    st.markdown("Understanding the primary rider and rideable types can give insight into future demand and potential marketing strategies. CitiBike currently offers two membership types in the NYC area along with both classic and electric bicycles. Members pay a subscription fee then receive unlimited rides on classic bike types and reduced fees on e-bikes. Casual riders do not pay the subscription fee, and instead pay for usage time in predetermined increments.")

    # Adding a sidebar for smmber type selection:
    with st.sidebar:
         member_filter = st.multiselect(label= 'Select rider type', options=df['member_casual'].unique(),
     default=df['member_casual'].unique())

    # Filtering the df for member selection (start)
    df1 = df.query('member_casual == @member_filter')
    df1['start_value'] = 1

    # creating a total_member counter
    total_members = float(df1['member_casual'].count())
    with st.sidebar:
        st.metric(label = 'Total Rider Count:', value = numerize(total_members))

    # creating a ride_length counter
    avg_ride_length = float(df1['trip_length_minutes'].mean())
    with st.sidebar:
        st.metric(label = 'Average Trip Length (Minutes):', value = numerize(avg_ride_length))

    
    #defining custom colors for these plots
    rideable_colors = ['#904941','#213148']
    season_colors = ['#456083', '#8b9cb2','#ac7771','#904941']

    # Creating columns to display plots side by side
    rideable_column, trip_length_column = st.columns(2)


    # filtering the df for member type for rideables
    df1 = df.query('member_casual == @member_filter')
    df1['rideable_count'] = 1

    # creating the groups for the charts (rideable type)
    df1['rideable_count'] = 1
    rideable_type_bar = df1.groupby('rideable_type', as_index = False).agg({'rideable_count': 'count'}) 

    #creating groups for charts (seasonal avg ride length):
    avg_trip_length_bar = df1.groupby('season', as_index = False).agg({'trip_length_minutes': 'mean'})


    ################## Rideable Type ###############
    
    # filtering the df for member type for rideables
    df1 = df.query('member_casual == @member_filter')
    df1['rideable_count'] = 1
    rideable_type_bar = df1.groupby('rideable_type', as_index = False).agg({'rideable_count': 'count'}) 

    rideable_fig = go.Figure(go.Bar(
            x = rideable_type_bar['rideable_type'],
            y = rideable_type_bar['rideable_count'],
            marker = {'color': rideable_colors}))
    
    # Update the layout
    rideable_fig.update_layout(
        title='Distribution of Rideable Type',
        xaxis_title='Rideable Type',
        yaxis_title='Count',
        plot_bgcolor='white',
        xaxis=dict(gridcolor='lightgrey'),  # Lighter grid lines on x-axis
        yaxis=dict(gridcolor='lightgrey'),  # Lighter grid lines on y-axis
        width=500,
        height=400)
    rideable_column.plotly_chart(rideable_fig, use_container_width=False)

    
    ################## SEASON Trip Length ############

    # Let's show Average trip Length by season
    avg_trip_length_fig = go.Figure(go.Bar(
        x=avg_trip_length_bar['season'],
        y=avg_trip_length_bar['trip_length_minutes'],
        marker = {'color':season_colors}))

    avg_trip_length_fig.update_layout(
        title='Average Trip Length by Season',
        xaxis_title='Season',
        yaxis_title='Average Trip Length (Minutes)',
        plot_bgcolor='white',
        xaxis=dict(gridcolor='lightgrey'),
        yaxis=dict(gridcolor='lightgrey'),
        width=500,
        height=400)
    trip_length_column.plotly_chart(avg_trip_length_fig, use_container_width = False)

    
    st.markdown('Currently Citibike members comprise 77.9% of the total riders in the NYC area. This indicates a need for consistent availability for returning users. While members tend to have a shorter ride length by nearly 10 minutes relative to casual riders. With the majority of Citibikes being of the classic variety (60.7%), and e-bikes being incentivized to members, this indicates an opportunity for expansion and increased profit as e-bike demand increases. A seasonal effect in total ride time can be noted, with summer and winter months having the shortest and longest ride times respectively. This seasonal effect also comes into play when assessing popularity of certain starting and ending stations for all Citibike riders.')

################### Popular Stations Page ##################################

elif page == "Popular Stations":
    st.header("Most Popular Start and End Stations")
    ### Markdown discussing impact of bar charts ##
    st.markdown('While many of the top 20 starting and ending stations are the same, there are some differences: namely Central Park and Univeristy Place stations being more popular ending stations than starting stations. This gives us an idea of how members and casual riders move throughout the city. When we remove rides taken in spring and summer months, it can be seen that Central Park stations are no longer in the top 20 in either list, yet the University Place station has notably increased in popularity. This could suggest that Citibike users are staying closer to home in the colder months.')## 

    # Adding a sidebar for season selection:
    with st.sidebar:
         season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
     default=df['season'].unique())

    # Filtering the df for season selection (start)
    df1 = df.query('season == @season_filter')
    df1['start_value'] = 1
    start_group_bar = df1.groupby('start_station_name', as_index = False).agg({'start_value': 'sum'}) 
    top20start = start_group_bar.nlargest(20, 'start_value')

    # filtering the df for season selection (end)
    df1 = df.query('season == @season_filter')
    df1['end_value'] = 1
    end_group_bar = df1.groupby('end_station_name', as_index = False).agg({'end_value': 'sum'}) 
    top20end = end_group_bar.nlargest(20, 'end_value')

    # creating a total_rides counter
    total_rides = float(df1['daily_ride_count'].count())
    with st.sidebar:
        st.metric(label = 'Total Bike Rides', value= numerize(total_rides))

    # creating a ride_length counter for season:
    avg_ride_length = float(df1['trip_length_minutes'].mean())
    with st.sidebar:
        st.metric(label = 'Average Trip Length (Minutes):', value= numerize(avg_ride_length))
    
    
    ## Bar Chart (Top 20 Starting Stations)
    start_fig = go.Figure(go.Bar(
            x = top20start['start_station_name'],
            y = top20start['start_value'],
            marker = {'color':top20start['start_value'], 'colorscale' : 'RdBu'}
                      ))
    start_fig.update_layout(
     title = 'Top 20 Starting Stations in NYC (2022)',
     xaxis_title = 'Start Stations',
     yaxis_title = 'Sum of Trips',
    plot_bgcolor='white',
    xaxis=dict(gridcolor='lightgrey'),
    yaxis=dict(gridcolor='lightgrey'),
     width = 1100, height = 350)
    st.plotly_chart(start_fig, use_container_width = True)

    ## Bar Chart (Top 20 Ending Stations)

    end_fig = go.Figure(go.Bar(x = top20end['end_station_name'],
                       y = top20end['end_value'],
                       marker = {'color':top20start['start_value'], 'colorscale' : 'RdBu'}
                      ))
    end_fig.update_layout(
     title = 'Top 20 Ending Stations in NYC (2022)',
     xaxis_title = 'End Stations',
     yaxis_title ='Sum of Trips',
    plot_bgcolor='white',
    xaxis=dict(gridcolor='lightgrey'),
    yaxis=dict(gridcolor='lightgrey'),
     width = 1100, height = 350)
    st.plotly_chart(end_fig, use_container_width = True)


################### Weather Impact Page ##################################

elif page == "Weather Impact on Rider Activity":
    st.header("Seasonal Impact on Ride Frequency and Length")
    st.markdown("It is no secret that weather can have an impact on how much time a bike rider is willing to spend outside. There are some interesting conclusions that can be drawn when it comes to the temperature and its effect on Citibike users.")

    # Adding a sidebar for season selection:
    with st.sidebar:
         season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
     default=df['season'].unique())

    # Filtering the df for season selection:
    df1 = df.query('season == @season_filter')
    df1['start_value'] = 1
    
    # creating a average daily temp:
    avg_daily_temp = float(df1['average_temp'].mean())
    with st.sidebar:
        st.metric(label = 'Average Daily Temperature:', value= numerize(avg_daily_temp))
        
    ## creating a lowest daily temp ##
    lowest_daily_temp = float(df1['average_temp'].min())
    with st.sidebar:
        st.metric(label = 'Lowest Daily Temperature:', value = numerize(lowest_daily_temp))

    ## creating a highest daily temp ##
    highest_daily_temp = float(df1['average_temp'].max())
    with st.sidebar:
        st.metric(label = 'Highest Daily Temperature:', value = numerize(highest_daily_temp))

    # creating a total_rides counter
    total_rides = float(df1['daily_ride_count'].count())
    with st.sidebar:
        st.metric(label = 'Total Bike Rides', value= numerize(total_rides))
    
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
                   marker = {'color' : 'indianred'}),
        secondary_y = True)
    fig3.update_layout(
         title = 'Daily Average Temperature and Daily Ride Count (NYC 2022)',
         xaxis_title = 'Date',
         width = 1300, height = 500,
        plot_bgcolor='white')
    fig3.update_yaxes(title_text='Sum of Trips', secondary_y=False)
    fig3.update_yaxes(title_text='Temperature', secondary_y=True)
    st.plotly_chart(fig3, use_container_width=True)

    ## markdown discussing weather impact ##
    st.markdown("The average daily temperature and total ride count are closely connected with few exceptions. Rider activity is highest in the summer months and lowest when the temperature drops in the winter months. In fact, rides in the summer account for 34.5% of all rides taken throughout the year, with winter months accounting for just 12.7% rides. It's clear that a seasonal impact is present and warm weather equates to more Citibike users. This insight coincides with the decreased average ride times (as seen in the Riders and Rideables analysis tab) and can be used to identify future need for increased rideable availability in warmer months. It should be noted that when temperature spikes are exceptionally high, rider activity is decreased.")


################### Interactive Map Page ##################################

elif page == "Interactive Map with NYC Landmarks and Ride Paths":
    st.header("Interactive Map of Ride Paths and Landmarks")
    st.markdown("The following map shows the most popular ride paths relative to popular NYC landmarks. This, coupled with the information we have about rider profile, demonstrates where Citibike needs to increase availability. It can be seen that the rides paths aren't always initiated or concluded near popular landmarks. While this might be surprising, it reinforces the need that Citibike members (potentially residents) might have over the lesser-numbered casual riders (possibly motivated by toursim). While this map doesn't show the exact ride path a user has taken, starting and ending stations near Central Park and along the waterfront appear to be especially popular.")

    ## Interactive Map ##
    ## Interactive Map (Stations) ##
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__) 

    # Define the path to the interactive map HTML file
    map_path = os.path.join(script_dir, 'final_landmark_map.html')

    # Read file and keep in variable 
    with open(map_path, 'r') as f:
         html_data = f.read()

     ## Show in web page ##
    # st.header("Most Popular CitiBike Ride Paths in NYC (2022)")
    st.components.v1.html(html_data, height = 900)
    

#################### Interactive Map w Stations ###########################

elif page == "Interactive Map with Citibike Stations":
    st.header("Interactive Map with Citibike Stations")
    st.markdown("The below map identifies all current Citibike Stations, with red colors representing increased frequency/popularity. When comparing this with the previous map, it is clear that there exists opportunities for Citibike to expand and create several new stations. Some of these are along the waterfront (both Hudson River and West Channel), while other growth opportunities could be surrounding Central Park, due to it's popularity with all types of riders.")

    ## Interactive Map (Stations) ##
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__) 

    # Define the path to the interactive map HTML file
    map_path2 = os.path.join(script_dir, 'Final_Station_Map.html')



    # Read file and keep in variable 
    with open(map_path2, 'r') as e:
         html_data2 = e.read()

     ## Show in web page ##
    # st.header("Most Popular CitiBike Ride Paths in NYC (2022)")
    st.components.v1.html(html_data2,height = 900)
    


################### Recommendations: Page ##################################
elif page == "Recommendations": 
    st.header("Recommendations and Response to Key Business Questions:") 
    st.markdown("")
    st.markdown("- How much would you recommend scaling bikes back between November and April?")
    st.markdown("With the obvious increase in demand in the summer months, scaling back during the winter months is a great way to increase profit margin and reduce costs. The winter and spring months (Nov-Apr) combined only account for 36% of all rides, while summer months account for 34.5% of total rides. Scaling back bike availability by 50% would still leave room for growth and increasing biciyle demand, but reduce the number of bikes not being used.")
    st.markdown("")
    st.markdown("- How could you determine how many more stations to add along the water?")
    st.markdown("To identify potential need along waterfront locales, the first step would be to observe the most popular ride paths and the popularity of current starting and ending stations. Along the Hudson River, there is a long (but popular) ride path that could be shortened by adding a station near the Chelsea Waterslide Park. Ganesvoort Peninsula and Pier 45 are also along this ride path and could be potentially viable stations. Along the West Channel, Citibike could benefit from a station near John Jay Park as it is close to pre-existing popular ride paths. Additional stations surrounding Central Park also demonstrate potential based on popular ride paths. ")
    st.markdown("")
    st.markdown("- What are some ideas for ensuring bikes are always stocked at the most popular stations?")
    st.markdown("To ensure bicycle availability, Citibike could implement a discount or incentive for riders to make round-trips from popular stations. While this might not equate to the exact same bike being returned, a similar rideable would complete the trip. This could be applied in the form of a discount offered to a rider if they return a rideable to the popular station from which they departed within the next 12-24 hours. Due to many riders being members, they're more likely to be consistent users that would benefit from a round-trip type of service.")
    st.markdown("")
    st.markdown("Additional recommendations would include the acquisition of additional electric rideables, as they appear to have slightly increased appeal to member riders (the majority of riders in the NYC area). While noting that casual riders aren't the majority, they are consistently taking significantly longer rides. Marketing efforts to brand Citibike as convenient and efficient could draw in new riders and incentivize additional memberships.")



##################### Conclusion / Mention of Data Limitations ##################

else:
    st.header("Conclusion and Limitations")
    st.markdown("NYC is a vast and lucrative market for Citibike with opportunity for growth and increased profitability. While solutions to several key business questions have been proposed, it is important to note that there were some limitations to this analysis. The primary limiting factor was the size of the dataset. After consistency checks and wrangling steps were performed, the data had to be sampled to improve workability. While the random sample has reproducible results, the total counts of riders and rides are only representative of a fraction of the dataset and actual figures are significantly greater.")

    # Define path for bike_pic
    bike_pic_path = os.path.join(script_dir, 'Images', 'citibike4.jpg')

    # Open the image
    bike_pic = Image.open(bike_pic_path)

    # Resize the image
    resized_bike = bike_pic.resize((1300, 700))

    # Display
    st.image(resized_bike)
