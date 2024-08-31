from flask import Flask, render_template
import pandas as pd
import folium
from folium.plugins import HeatMap

app = Flask(__name__)

# Dummy data for pickup and dropoff points
data = {
    'latitude': [
        6.818, 6.819, 6.817, 6.818, 6.816, 6.820, 6.821, 6.817, 6.818, 6.819,
        6.820, 6.816, 6.821, 6.817, 6.818, 6.819, 6.820, 6.821, 6.816, 6.818,
        6.817, 6.819, 6.818, 6.820, 6.821, 6.818, 6.819, 6.817, 6.818, 6.820,
        6.821, 6.818, 6.816, 6.820, 6.821, 6.818, 6.819, 6.817, 6.820, 6.821,
        6.818, 6.819, 6.817, 6.820, 6.821, 6.815, 6.822, 6.823, 6.814, 6.824
    ],
    'longitude': [
        -58.119, -58.120, -58.118, -58.121, -58.122, -58.118, -58.119, -58.120, -58.121, -58.122,
        -58.119, -58.120, -58.121, -58.122, -58.119, -58.118, -58.119, -58.120, -58.121, -58.122,
        -58.119, -58.120, -58.121, -58.122, -58.119, -58.120, -58.121, -58.122, -58.119, -58.118,
        -58.119, -58.120, -58.121, -58.122, -58.119, -58.120, -58.121, -58.122, -58.119, -58.118,
        -58.119, -58.120, -58.121, -58.122, -58.119, -58.123, -58.124, -58.124, -58.124, -58.124
    ]
}



df = pd.DataFrame(data)

@app.route('/')
def index():
    # Create a base map centered around Guyana
    map_center = [6.818, -58.119]
    m = folium.Map(location=map_center, zoom_start=13)

    # Create heatmap layer with custom opacity
    heat_data = [[row['latitude'], row['longitude']] for index, row in df.iterrows()]
    HeatMap(heat_data, min_opacity=0.2, max_opacity=0.8, radius=15).add_to(m)

    # Save the map to an HTML file in the templates directory
    m.save('C:/Users/sm94c/Documents/Repositiories/innovation_project/synergysource/backend/hotspots/templates/map.html')

    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
