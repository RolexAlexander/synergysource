# Passenger Counter

This folder contains the code for a passenger counting application that uses YOLO (You Only Look Once) for object detection to count the number of passengers in a vehicle. The application logs the passenger count to a database, providing real-time information on the occupancy of vehicles.

## Setup Instructions

### 1. Download YOLO Weights
Due to the large size of the YOLO weights, they are not included in this repository. To run the application, you will need to download the pre-trained YOLO weights:

- Download the YOLO weights from the official [YOLO website](https://pjreddie.com/darknet/yolo/).
- Save the weights file in the appropriate directory, typically where the YOLO model is loaded in your code.

### 2. Run the Application

- Once the weights are downloaded, you can start the server by running `app.py`.

```bash
python app.py
```

### 3. Passenger Counting and Logging

- The application will predict the number of passengers in a vehicle using YOLO object detection.
- The passenger count is then logged to a database, allowing for real-time tracking of vehicle occupancy.

### Additional Notes

- Ensure that your database is set up and running correctly, as the application will attempt to log data into the database.
- If you encounter any issues with the YOLO weights or model, please verify that the paths and configurations in `app.py` are correct.