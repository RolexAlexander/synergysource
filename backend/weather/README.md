# Weather Folder

This folder contains scripts for generating weather graphs using both mockup and real weather data.

## Overview

- **`main.py`**: This script uses mockup data to generate weather graphs. It can be run without any external dependencies or API keys, making it ideal for testing and development purposes.

- **`api.py`**: This script generates weather graphs using real data from the [Weatherbit API](https://api.weatherbit.io). To run this script, you will need an API key from Weatherbit. The real-time weather data fetched from the API is then processed and visualized.

## Setup and Usage

1. **Mockup Data (main.py)**:
   - Simply run the `main.py` script to generate weather graphs using predefined mockup data.
   - No external API or internet connection is required.

   ```bash
   python main.py
   ```

2. **Real Data (api.py)**:
   - Obtain an API key from [Weatherbit](https://www.weatherbit.io/).
   - Replace the placeholder with your API key in `api.py`.
   - Run the `api.py` script to generate weather graphs using live data from Weatherbit.

   ```bash
   python api.py
   ```

## Requirements

- To run `api.py`, ensure you have the following:
  - A valid Weatherbit API key.
  - Internet connection to fetch real-time data from the Weatherbit API.

This setup allows you to switch between mockup data and real weather data depending on your needs.