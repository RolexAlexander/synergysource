import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import requests
import threading
import time
from datetime import datetime

API_KEY = 'a6d5ad09d57e42f4864d7c574ce33024'  # Replace with your Weatherbit API key

# Global variables to store data
temperatures = []
times = []
running = False

def get_weather_data(lat, lon):
    url = f"https://api.weatherbit.io/v2.0/current"
    params = {
        "lat": lat,
        "lon": lon,
        "key": API_KEY,
        "units": "I"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def update_weather_data(lat, lon):
    global running
    while running:
        weather_data = get_weather_data(lat, lon)
        if weather_data:
            temp = weather_data["data"][0]["temp"]
            timestamp = datetime.now().strftime('%H:%M:%S')
            temperatures.append(temp)
            times.append(timestamp)
        time.sleep(5)  # Fetch data every 5 seconds

# Initialize Dash app
app = dash.Dash(__name__)

# Dash layout
app.layout = html.Div([
    html.H1("Real-Time Weather Monitoring"),
    dcc.Input(id='lat', type='number', placeholder="Enter Latitude"),
    dcc.Input(id='lon', type='number', placeholder="Enter Longitude"),
    html.Button('Start Monitoring', id='start-btn', n_clicks=0),
    html.Button('Stop Monitoring', id='stop-btn', n_clicks=0),
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(id='graph-update', interval=1*1000, n_intervals=0),
])

# Start monitoring callback
@app.callback(
    Output('start-btn', 'disabled'),
    Input('start-btn', 'n_clicks'),
    State('lat', 'value'),
    State('lon', 'value')
)
def start_monitoring(n_clicks, lat, lon):
    global running
    if n_clicks > 0 and lat and lon:
        lat = float(lat)
        lon = float(lon)
        running = True
        threading.Thread(target=update_weather_data, args=(lat, lon)).start()
        return True
    return False

# Stop monitoring callback
@app.callback(
    Output('stop-btn', 'disabled'),
    Input('stop-btn', 'n_clicks')
)
def stop_monitoring(n_clicks):
    global running
    if n_clicks > 0:
        running = False
        return True
    return False

# Update graph callback
@app.callback(
    Output('live-graph', 'figure'),
    Input('graph-update', 'n_intervals')
)
def update_graph(n):
    data = go.Scatter(
        x=times,
        y=temperatures,
        mode='lines+markers',
        name='Temperature (°F)'
    )

    layout = go.Layout(
        xaxis=dict(title='Time'),
        yaxis=dict(title='Temperature (°F)'),
        title='Real-Time Temperature Data'
    )

    return {'data': [data], 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)
