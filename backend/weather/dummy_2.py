import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import random
from datetime import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Initialize the Dash app
app = dash.Dash(__name__)

# Dark theme styling
dark_theme = {
    'backgroundColor': '#1e1e1e',
    'textColor': '#e1e1e1',
    'graphBackground': '#2b2b2b',
    'axisColor': '#e1e1e1',
    'gridColor': '#444444',
    'highlightColor': '#17becf'
}

# Dummy pollutant data
pollutants = {
    "PM2.5": random.uniform(10, 50),
    "PM10": random.uniform(20, 60),
    "NO2": random.uniform(15, 40),
    "O3": random.uniform(30, 70)
}

# Weather icon mapping based on conditions
weather_icons = {
    'sunny': '☀️',
    'rainy': '🌧️',
    'cloudy': '☁️',
    'stormy': '⛈️',
    'snowy': '❄️',
    'foggy': '🌫️'
}

# Sample current weather condition
current_weather = "sunny"

# Layout of the app with dark theme
app.layout = html.Div([
    html.H1(
        "Real-Time Weather Monitoring",
        style={'color': dark_theme['textColor'], 'textAlign': 'center', 'padding': '10px'}
    ),
    html.Div(
        [
            html.Div(
                [
                    html.H2(f"{weather_icons[current_weather]} {current_weather.capitalize()}"),
                    html.P("Current Pollutants (µg/m³):", style={'fontSize': '18px'}),
                    html.Ul([
                        html.Li(f"{pollutant}: {level:.1f}", style={'fontSize': '16px'}) 
                        for pollutant, level in pollutants.items()
                    ])
                ],
                style={'textAlign': 'center', 'padding': '20px', 'color': dark_theme['textColor']}
            )
        ],
        style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'paddingBottom': '20px'}
    ),
    dcc.Graph(id='temperature-graph', config={'displayModeBar': False}),
    dcc.Graph(id='humidity-graph', config={'displayModeBar': False}),
    html.Div(id='uv-index', style={'textAlign': 'center', 'margin': '20px'}),
    dcc.Graph(id='wind-speed-graph', config={'displayModeBar': False}),
    dcc.Graph(id='rain-possibility-graph', config={'displayModeBar': False}),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # in milliseconds (5000ms = 5s)
        n_intervals=0  # Start at zero
    )
], style={'backgroundColor': dark_theme['backgroundColor'], 'padding': '20px'})

# Initialize data storage with a fixed maximum length
MAX_LENGTH = 20  # Maximum number of points to display
temperatures = []
times = []
humidities = []
wind_speeds = []
rain_possibilities = []

def trim_data(data_list):
    """Trim the data list to the maximum length."""
    if len(data_list) > MAX_LENGTH:
        return data_list[-MAX_LENGTH:]
    return data_list

# Callback to update the temperature and humidity graphs
@app.callback(
    [Output('temperature-graph', 'figure'),
     Output('humidity-graph', 'figure'),
     Output('uv-index', 'children'),
     Output('wind-speed-graph', 'figure'),
     Output('rain-possibility-graph', 'figure')],
    Input('interval-component', 'n_intervals')
)
def update_graphs(n):
    # Generate dummy data
    prev_temp = 80.0  # Starting with a typical temperature
    prev_humidity = 50.0  # Average humidity
    prev_uv_index = 5.0  # Moderate UV index
    prev_wind_speed = 10.0  # Moderate wind speed
    prev_rain_probability = 10.0  # Low chance of rain

    # Function to generate new data with realistic fluctuations
    def generate_realistic_data(prev_temp, prev_humidity, prev_uv_index, prev_wind_speed, prev_rain_probability):
        temp = round(prev_temp + random.uniform(-1.5, 1.5), 2)
        humidity = round(prev_humidity + random.uniform(-2.0, 2.0), 2)
        uv_index = round(prev_uv_index + random.uniform(-0.2, 0.2), 1)
        uv_index = max(0, min(uv_index, 11))
        wind_speed = round(prev_wind_speed + random.uniform(-0.5, 0.5), 2)
        wind_speed = max(0, wind_speed)
        rain_probability = round(prev_rain_probability + (random.random() - 0.5) * 2, 2)
        rain_probability = max(0, min(rain_probability, 100))

        timestamp = datetime.now().strftime('%H:%M:%S')
        return temp, humidity, uv_index, wind_speed, rain_probability, timestamp

    temp, humidity, uv_index, wind_speed, rain_probability, timestamp = generate_realistic_data(
        prev_temp, prev_humidity, prev_uv_index, prev_wind_speed, prev_rain_probability
    )

    temperatures.append(temp)
    times.append(timestamp)
    humidities.append(humidity)
    wind_speeds.append(wind_speed)
    rain_possibilities.append(rain_probability)

    temperatures[:] = trim_data(temperatures)
    times[:] = trim_data(times)
    humidities[:] = trim_data(humidities)
    wind_speeds[:] = trim_data(wind_speeds)
    rain_possibilities[:] = trim_data(rain_possibilities)

    temp_threshold = 4.0  # e.g., 5°F increase
    humidity_threshold = 10.0  # e.g., 10% increase

    temp_colors = [
        'red' if (i > 0 and (temperatures[i] - temperatures[i - 1]) > temp_threshold) else dark_theme['highlightColor']
        for i in range(len(temperatures))
    ]

    humidity_colors = [
        'red' if (i > 0 and (humidities[i] - humidities[i - 1]) > humidity_threshold) else dark_theme['highlightColor']
        for i in range(len(humidities))
    ]

    temperature_figure = go.Figure(
        data=[go.Scatter(
            x=times,
            y=temperatures,
            mode='lines+markers',
            line=dict(shape='spline', smoothing=1.3),
            marker=dict(color=temp_colors)
        )],
        layout=go.Layout(
            title="Temperature Over Time",
            xaxis=dict(title="Time", color=dark_theme['axisColor'], gridcolor=dark_theme['gridColor']),
            yaxis=dict(title="Temperature (°F)", color=dark_theme['axisColor'], gridcolor=dark_theme['gridColor']),
            margin=dict(l=40, r=20, t=40, b=30),
            paper_bgcolor=dark_theme['graphBackground'],
            plot_bgcolor=dark_theme['graphBackground'],
            font=dict(color=dark_theme['textColor'])
        )
    )
    
    
    humidity_figure = go.Figure(
        data=[go.Scatter(
            x=times,
            y=humidities,
            mode='lines+markers',
            line=dict(shape='spline', smoothing=1.3),
            marker=dict(color=humidity_colors)
        )],
        layout=go.Layout(
            title="Humidity Over Time",
            xaxis=dict(title="Time", color=dark_theme['axisColor'], gridcolor=dark_theme['gridColor']),
            yaxis=dict(title="Humidity (%)", color=dark_theme['axisColor'], gridcolor=dark_theme['gridColor']),
            margin=dict(l=40, r=20, t=40, b=30),
            paper_bgcolor=dark_theme['graphBackground'],
            plot_bgcolor=dark_theme['graphBackground'],
            font=dict(color=dark_theme['textColor'])
        )
    )

    # UV Index Visualization as a Colored Circle
    uv_color = "green" if uv_index < 3 else "yellow" if uv_index < 6 else "orange" if uv_index < 8 else "red"
    uv_gradient = (
        "linear-gradient(135deg, #4caf50, #81c784)" if uv_index < 3 else
        "linear-gradient(135deg, #ffeb3b, #ffc107)" if uv_index < 6 else
        "linear-gradient(135deg, #ff9800, #ffb74d)" if uv_index < 8 else
        "linear-gradient(135deg, #f44336, #e57373)"
    )
    uv_circle = html.Div(
        style={
            'width': '120px', 
            'height': '120px', 
            'borderRadius': '50%', 
            'backgroundImage': uv_gradient,
            'display': 'flex', 
            'justifyContent': 'center', 
            'alignItems': 'center', 
            'color': 'white', 
            'fontSize': '24px', 
            'margin': '0 auto', 
            'boxShadow': '0 4px 15px rgba(0, 0, 0, 0.3)',
            'border': '2px solid rgba(255, 255, 255, 0.5)',
            'textShadow': '0 1px 2px rgba(0, 0, 0, 0.5)'
        },
        children=f"UV: {uv_index}"
    )

    # Wind Speed Gauge
    wind_speed_figure = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=wind_speed,
        gauge={
            'axis': {'range': [0, 20], 'tickcolor': dark_theme['axisColor']},
            'bar': {'color': dark_theme['highlightColor']},
            'steps': [
                {'range': [0, 5], 'color': '#3399FF'},
                {'range': [5, 10], 'color': '#33CCFF'},
                {'range': [10, 15], 'color': '#66FFFF'},
                {'range': [15, 20], 'color': '#99FFFF'}
            ],
            'threshold': {
                'line': {'color': dark_theme['textColor'], 'width': 4},
                'thickness': 0.75,
                'value': 15
            }
        },
        title={'text': "Wind Speed (mph)", 'font': {'color': dark_theme['textColor']}},
        number={'suffix': " mph", 'font': {'color': dark_theme['textColor']}}
    )
    )

    wind_speed_figure.update_layout(
        paper_bgcolor=dark_theme['graphBackground'],
        font=dict(color=dark_theme['textColor']),
        margin=dict(l=40, r=20, t=40, b=30)
    )

    # Rain Possibility Bar Chart
    rain_possibility_figure = go.Figure(
        data=[go.Bar(x=times, y=rain_possibilities, marker_color=dark_theme['highlightColor'])],
        layout=go.Layout(
            title="Rain Possibility Over Time",
            xaxis=dict(title="Time", color=dark_theme['axisColor'], gridcolor=dark_theme['gridColor']),
            yaxis=dict(title="Possibility (%)", color=dark_theme['axisColor'], gridcolor=dark_theme['gridColor']),
            margin=dict(l=40, r=20, t=40, b=30),
            paper_bgcolor=dark_theme['graphBackground'],
            plot_bgcolor=dark_theme['graphBackground'],
            font=dict(color=dark_theme['textColor'])
        )
    )

    return temperature_figure, humidity_figure, uv_circle, wind_speed_figure, rain_possibility_figure

if __name__ == '__main__':
    app.run_server(debug=True)
