# API Layer

This folder contains the FastAPI layer used to interact with the database. It provides the API endpoints necessary to manage and interact with the data stored in the PostgreSQL database.

## Running the API

To run the API, you need to start the Docker container. Use the following command:

```bash
docker-compose up
```

However, note that this will start the API server alone. All other necessary services, including the PostgreSQL database, need to be running and properly configured for the API to function correctly. Ensure your PostgreSQL service is up and accessible.

Additionally, you will need to update the hardcoded credentials in database.py so that the API connects seamlessly to your running PostgreSQL service.

[LIVE API SERVER](https://observant-integrity-production.up.railway.app/docs)
## API Documentation

Once the API is running, you can visit the following URL to access the interactive API documentation:

[http://localhost:8000/docs](http://localhost:8000/docs)

This documentation provides a convenient way to explore and test the available endpoints.

## Database Population

To facilitate testing and initial setup, a `data` folder and a `populate.py` script have been added. These resources allow you to easily populate the database with sample data.

### Important Note

Please note that when running the `populate.py` script, operations must be executed sequentially. Some operations, such as creating initial entries, return IDs that are required for creating subsequent records in the database. Running multiple operations simultaneously may lead to errors due to missing dependencies.

### How to Populate the Database

1. Ensure the Docker container is running by using `docker-compose up`.
2. Run the `populate.py` script to populate the database:
   ```bash
   python populate.py
   ```
3. Follow the script's instructions to ensure that the database is populated in the correct order.

