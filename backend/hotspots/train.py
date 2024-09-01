import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error

# Generate dummy data for training
np.random.seed(42)
n_samples = 500

# Dummy latitude and longitude for customers
latitudes = np.random.uniform(10.0, 60.0, n_samples)
longitudes = np.random.uniform(-130.0, -60.0, n_samples)

# Dummy time of the day (in hours) when the ride was requested
times = np.random.uniform(0, 24, n_samples)

# Combine latitude, longitude, and time into a dataframe
data = pd.DataFrame({
    'latitude': latitudes,
    'longitude': longitudes,
    'time_of_day': times
})

# Dummy target variable: number of ride requests at that location and time
# (Higher values simulate hotspots)
ride_requests = (np.sin(latitudes) + np.cos(longitudes) + np.sin(times)).clip(min=0) * 100 + np.random.normal(0, 10, n_samples)
data['ride_requests'] = ride_requests

# Train/test split
X = data[['latitude', 'longitude', 'time_of_day']]
y = data['ride_requests']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Polynomial features for non-linear relationships
poly = PolynomialFeatures(degree=2)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Model training
model = LinearRegression()
model.fit(X_train_poly, y_train)

# Predictions
y_pred = model.predict(X_test_poly)

# Calculate error
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Visualize the results: Plot the predicted hotspots
gdf = gpd.GeoDataFrame(X_test, geometry=gpd.points_from_xy(X_test.longitude, X_test.latitude))
gdf['predicted_ride_requests'] = y_pred

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres')) # please download the Natural Earth dataset
ax = world.plot(figsize=(15, 10))
gdf.plot(ax=ax, marker='o', color='red', markersize=gdf['predicted_ride_requests'], alpha=0.6)
plt.title('Predicted Hotspots for Ride Requests')
plt.show()