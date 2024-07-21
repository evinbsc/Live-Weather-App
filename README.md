# Weather Monitoring App with Streamlit and MySQL

This project implements a weather monitoring application built using Streamlit, which connects to a MySQL database to fetch and display live temperature and humidity data. The application leverages various Python libraries to achieve its functionality, providing an interactive dashboard to view real-time data.

## Purpose

The purpose of this project is to demonstrate how a simple weather monitoring system can be built using Python and Streamlit, offering a user-friendly interface to monitor live temperature and humidity data from a MySQL database.

## Key Features

- **Live Data Display**: Continuously fetches and displays the latest temperature and humidity readings.
- **Interactive Charts**: Uses Plotly to create interactive line and area charts for temperature and humidity data.
- **Real-Time Updates**: Automatically updates the displayed data at regular intervals.
- **Responsive Design**: Utilizes Streamlit’s layout features to create a responsive and accessible web interface.

## Technical Implementation

### Libraries Used

- **pandas**: For data manipulation and analysis.
- **streamlit**: For creating the web application and interactive dashboard.
- **plotly.express**: For generating interactive charts.
- **time**: For handling sleep intervals between data fetches.

### Steps

1. **Setup Streamlit Configuration**:
    - Configured the Streamlit page with a title, icon, and layout settings.
    - Created placeholders for data display and charts.

2. **Initialize Database Connection**:
    - Established a connection to the MySQL database using Streamlit's connection manager.
    
3. **Fetch Data from MySQL**:
    - Defined a function `fetch_data` to query the MySQL database and return the data as a DataFrame.
    - Cached the data fetching function with a Time To Live (TTL) of 55 seconds to optimize performance.

4. **Main Loop for Real-Time Data Update**:
    - Continuously fetched the latest data at regular intervals.
    - Extracted the current and previous temperature and humidity values.
    - Calculated the changes in temperature and humidity.
    - Constructed a timestamp string for the latest data.
    - Updated the data display section with the latest values and changes.
    - Updated the temperature and humidity graphs using Plotly.

5. **Visual Display**:
    - Displayed the latest data and changes using Streamlit's metric components.
    - Visualized the temperature and humidity trends with interactive charts using Plotly.
