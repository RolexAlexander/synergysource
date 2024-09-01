# Backend Services

This repository contains various backend services for our team's 2024 Innovation Challenge Hackathon. These services work together to provide a comprehensive backend solution for our ride system.

## Services

### 1. Geospatial Regression Backend

This service performs geospatial regression to predict passenger hotspots based on historical data. It helps in optimizing planning and resource allocation by identifying areas with high demand.

- **Technologies**: Python, GeoPandas, Scikit-learn
- **Key Features**:
  - Geospatial regression to predict hotspots
  - Visualization of predicted hotspots on maps

### 2. Live Weather Updates Backend

Provides real-time weather updates for our system. This service fetches weather data from an external API and delivers up-to-date weather information.

- **Technologies**: Python, API Integration (weatherbit.io)
- **Key Features**:
  - Real-time weather updates
  - Weather data visualization and reporting

### 3. Passenger Counter Backend

This service uses YOLO (You Only Look Once) models to count the number of passengers in vehicles and logs this data to our database for real-time monitoring.

- **Technologies**: Python, YOLO, OpenCV
- **Key Features**:
  - Real-time passenger counting
  - Integration with the database for live data logging

### 4. Speed Tracker Backend

Tracks vehicle speeds using a combination of GPS data and computer vision. It logs the speed information and updates the database accordingly.

- **Technologies**: Python, Ultralytics, Roboflow, Supervision
- **Key Features**:
  - Vehicle speed tracking
  - Integration with the database for speed data logging

### 5. Hotspots Backend

This service plots and analyzes hotspots on maps based on passenger data. It provides insights into high-demand areas for better planning.

- **Technologies**: Python, GeoPandas, Matplotlib
- **Key Features**:
  - Hotspot plotting on maps
  - Analysis of passenger data for hotspot prediction

### 6. API Backend for System Management

Handles API requests and interactions for system management. This service provides endpoints for various functionalities required by the frontend and other services.

- **Technologies**: FastAPI, Python
- **Key Features**:
  - System management API endpoints
  - Integration with other backend services

### 7. Database Backend (PostgreSQL)

Manages the PostgreSQL database that stores all the relevant data for the system. It includes schemas and configurations required for proper database operations.

- **Technologies**: PostgreSQL, Docker
- **Key Features**:
  - PostgreSQL database setup and management
  - Database schemas and initialization scripts

## Setup and Running

For detailed setup instructions and configurations, refer to the respective service folders.