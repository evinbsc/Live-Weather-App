import pandas as pd
import streamlit as st
import plotly.express as px
import time

# Set Streamlit page configuration
st.set_page_config(
    page_title="AWS MySQL Testing",
    page_icon="XX",
    layout="wide",
)

# Set title and header for the Streamlit app
st.title('Here is my weather app!')
st.header('Live Data')

# Create empty placeholders for data display and graphs
datadisplay = st.empty()
temp_graph = st.empty()
humid_graph = st.empty()

# Initialize connection to MySQL database
conn = st.connection('mysql', type='sql')

@st.cache_data(ttl=55)
def fetch_data():
    """
    Fetch data from MySQL database and return as a DataFrame.
    
    This function is cached to improve performance, with a Time To Live (ttl)
    of 55 seconds, which works well for projects with frequent data updates.
    
    Returns:
        pd.DataFrame: DataFrame containing temperature, humidity, and timestamp data.
    """
    query = """
        SELECT tempF, humidity, 
               YEAR(date_add(time_stamp,INTERVAL -5 HOUR)) as year, 
               MONTH(date_add(time_stamp,INTERVAL -5 HOUR)) as month, 
               DAY(date_add(time_stamp,INTERVAL -5 HOUR)) as day, 
               HOUR(date_add(time_stamp,INTERVAL -5 HOUR)) as hour, 
               MINUTE(date_add(time_stamp,INTERVAL -5 HOUR)) as minute, 
               SECOND(date_add(time_stamp,INTERVAL -5 HOUR)) as second, 
               date_add(time_stamp,INTERVAL -5 HOUR) as ts 
        FROM esp32_dht20 
        ORDER BY time_stamp DESC 
        LIMIT 5760;
    """
    df = conn.query(query, ttl=1)
    return df

while True:
    # Fetch the latest data
    data = fetch_data()

    # Extract current and previous temperature and humidity values
    current_temp = data.at[data.index[0], "tempF"]
    current_humidity = data.at[data.index[0], "humidity"]
    old_temp = data.at[data.index[1], "tempF"]
    old_humidity = data.at[data.index[1], "humidity"]

    # Calculate changes in temperature and humidity
    temp_delta = int(current_temp) - int(old_temp)
    humid_delta = int(current_humidity) - int(old_humidity)

    # Construct the timestamp string for the latest data
    lasttime_str = f"Time of Last Data: {data.at[data.index[0],'month']}/{data.at[data.index[0],'day']}/{data.at[data.index[0],'year']} at {data.at[data.index[0],'hour']}:{data.at[data.index[0],'minute']}:{data.at[data.index[0],'second']}"

    # Update the data display section
    with datadisplay.container():
        st.text(lasttime_str)
        kpi1, kpi2 = st.columns(2)
        kpi1.metric(label="Temperature F", value=f"{current_temp} F", delta=f"{temp_delta} F")
        kpi2.metric(label="Humidity", value=f"{current_humidity} %", delta=f"{humid_delta} %")

    # Update the temperature graph
    with temp_graph:
        tempdata = data[['ts', 'tempF']].copy()
        fig_t = px.line(tempdata, x="ts", y="tempF", title="Temperature (F)")
        st.plotly_chart(fig_t)

    # Update the humidity graph
    with humid_graph:
        humiddata = data[['ts', 'humidity']].copy()
        fig_h = px.area(humiddata, x="ts", y="humidity", title="Humidity (%)")
        st.plotly_chart(fig_h)

    # Wait for the specified interval before fetching data again
    time.sleep(2)  # Change to required intervals
