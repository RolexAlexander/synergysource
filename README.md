# 2024 Innovation Challenge Hackathon

Welcome to the repository for our 2024 Innovation Challenge Hackathon! This project features both frontend and backend components designed to create a robust ride system with various advanced features. Our solution integrates AI and external resources to streamline development and enhance functionality.

## Project Overview

### Frontend
The frontend of this project is designed to deliver a modern and intuitive user experience. It incorporates:
- **Live Passenger Counting/Capacity Control**
- **Speed Tracking** via GPS and computer vision
- **Social Integration** for Facebook call and Instagram
- **Real-time Weather Tracking**
- **Emergency Button**
- **Reporting Capabilities**
- **Route Optimization**
- **Fleet Management**
- **Geospatial Regression** to predict hotspots
- **Maintenance Management**
- **Ride Creation and Assignment**
- **Driver Details on Map (Live)**

### Backend
The backend services power the functionality of the system, handling data processing, real-time updates, and more:
- **Geospatial Regression Backend**: Predicts passenger hotspots using geospatial regression.
- **Live Weather Updates Backend**: Provides real-time weather updates using API integration.
- **Passenger Counter Backend**: Counts passengers using YOLO models and logs data to the database.
- **Speed Tracker Backend**: Tracks vehicle speeds with GPS and computer vision.
- **Hotspots Backend**: Analyzes and plots passenger hotspots on maps.
- **API Backend for System Management**: Manages API requests and interactions.
- **Database Backend (PostgreSQL)**: Manages the PostgreSQL database for storing system data.

## Technologies Used
- **AI & Machine Learning**:
  - **GPT-4**: Utilized for generating code outlines and fast-tracking development.
  - **Ultralytics**: For object detection and speed tracking.
  - **Roboflow**: For model training and deployment.
  - **Supervision**: For speed estimation with computer vision.
- **Frontend**:
  - **Flowbite**
  - **Tailwind CSS**
  - **LeafletJS**
  - **Google Maps**
  - **Flaticon**
- **Backend**:
  - **Darknet**: For YOLO object detection.
  - **PostgreSQL**: Managed using Docker Compose.

## Setup Instructions

### Running the Project

1. **Frontend**: 
   - Navigate to the frontend folder.
   - Install dependencies using: `npm install` or `yarn install`.
   - Start the development server using: `npm start` or `yarn start`.

2. **Backend**:
   - Navigate to the backend folder.
   - Ensure all required services are up and running using Docker Compose: `docker-compose up`.
   - Follow the specific instructions in each service's README for running them individually.

## References
- **Ultralytics**: For speed tracking using YOLO models. [Ultralytics GitHub](https://github.com/ultralytics/yolov5)
- **Roboflow**: For model training and deployment. [Roboflow](https://roboflow.com/)
- **Supervision**: For speed estimation with computer vision. [Supervision GitHub](https://github.com/roboflow/supervision)
- **PostgreSQL Docker Setup**: For PostgreSQL database setup. [Docker Compose PostgreSQL](https://github.com/felipewom/docker-compose-postgres)
- **Flowbite**: UI components for Tailwind CSS. [Flowbite](https://flowbite.com/)
- **Google Maps**: For map integration. [Google Maps](https://developers.google.com/maps)
- **LeafletJS**: For interactive maps. [LeafletJS](https://leafletjs.com/)
- **Tailwind CSS**: For utility-first CSS framework. [Tailwind CSS](https://tailwindcss.com/)
- **Flaticon**: For icons used in the project. [Flaticon](https://www.flaticon.com/)
- **Darknet**: YOLO object detection framework. [Darknet GitHub](https://github.com/pjreddie/darknet)

## Team Members

- **Thraick Jairam**
  - Github: [Thraick Jairam GitHub](https://github.com/Thraick?tab=repositories)
  - Linkedin: [Thraick Jairam LinkedIn](https://www.linkedin.com/in/tharick-jairam-777069208/)

- **Samir Mohammed**
  - Github: [Samir Mohammed GitHub](https://github.com/Dinamush)
  - Linkedin: [Samir Mohammed LinkedIn](https://www.linkedin.com/in/samir-mohammed-42505b178?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)

- **Rolex Alexander (Team Leader)**
  - Github: [Rolex Alexander GitHub](https://github.com/RolexAlexander)
  - Linkedin: [Rolex Alexander LinkedIn](https://linkedin.com/in/rolex-alexander-83766a203)
