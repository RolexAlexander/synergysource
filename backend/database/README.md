# Backend Database Setup

This README provides detailed instructions on setting up and running the backend database for your application using Docker and Docker Compose. The setup includes a PostgreSQL database and pgAdmin for database administration. The database schemas are defined and managed within the API layer.

## Table of Contents

- [Backend Database Setup](#backend-database-setup)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Navigate to the Backend Directory](#2-navigate-to-the-backend-directory)
    - [3. Initialize the Database](#3-initialize-the-database)
    - [5. Start the Services](#5-start-the-services)
  - [Accessing pgAdmin](#accessing-pgadmin)
  - [Database Schemas](#database-schemas)
    - [1. Organizations](#1-organizations)
    - [2. Customers](#2-customers)
    - [3. Drivers](#3-drivers)
    - [4. Locations](#4-locations)
    - [5. Vehicles](#5-vehicles)
    - [6. Reports](#6-reports)
    - [7. Emergency Reports](#7-emergency-reports)
    - [8. Ride](#8-ride)
    - [9. Hail](#9-hail)
    - [10. Payments](#10-payments)
    - [11. Vehicle Speeds](#11-vehicle-speeds)
  - [Testing the Setup](#testing-the-setup)
  - [Notes](#notes)
  - [References](#references)

---

## Prerequisites

Ensure you have the following software installed on your system before proceeding:

- **Docker**: [Download and Install Docker](https://www.docker.com/get-started)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Git**: [Download and Install Git](https://git-scm.com/downloads)

---

## Project Structure

```
backend/
│
├── database/
|   |── docker-compose.yml
|   ├── init.sql
|   └── README.md
└── api/
    └── ...
```

- **`docker-compose.yml`**: Defines the Docker services for PostgreSQL and pgAdmin.
- **`init.sql`**: Contains initial SQL commands to set up the database and insert test data.
- **`api/`**: Contains the API layer responsible for managing database schemas and initialization.
  - **`database.py`**: Defines all the database schemas and functions required to interact with the db.

---

## Getting Started

Follow these steps to set up and run the backend database services.

### 1. Clone the Repository

```bash
git clone https://sbm-digital-factory@dev.azure.com/sbm-digital-factory/Hackathon%20GYN%202024/_git/team-ttr
```

### 2. Navigate to the Backend Directory

```bash
cd team-ttr/backend
```

### 3. Initialize the Database

The database initialization is handled by the API layer. Ensure that the `api/database.py` script is configured to connect to the PostgreSQL service defined in `docker-compose.yml`.

**`api/database.py` example:**
```python
import psycopg2
from schemas import SCHEMAS

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                user="postgres",
                password="xyz",
                host="local",
                port="5432",
                database="postgres"
            )
            self.cursor = self.connection.cursor()
            self.create_tables()
            print("Connected to the database and tables created successfully")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

if __name__ == '__main__':
    # Example usage for customers
    db = Database()

    # Create a customer
    customer_id = db.create_customer(
        name="John Doe",
        email="johe@doqwe.com",
        phone_number="2321234",
        password="password123"
    )
```

**Note:** Ensure the `database` class is initialised after the PostgreSQL service is up and running.

### 5. Start the Services

Run the following command to start PostgreSQL and pgAdmin services:

```bash
docker-compose up -d
```

This command will:

- Pull the latest PostgreSQL and pgAdmin images.
- Start the services in detached mode.
- Mount the necessary volumes for data persistence.
- Expose the services on specified ports.

---

## Accessing pgAdmin

pgAdmin is a web-based GUI for managing PostgreSQL databases.

**Access pgAdmin:**

- Open your browser and navigate to: `http://localhost:15433`
- Login using the credentials provided in the `environment` in the docker-compose.yml file.
  - **Email:** `admin@dev.com`
  - **Password:** `xyz`

**Configure PostgreSQL Server in pgAdmin:**

1. **Add New Server**:
   - Right-click on "Servers" and select "Create" > "Server".
2. **Connection Settings**:
   - **Name:** `PostgreSQL`
   - **Host:** `database`
   - **Port:** `5432`
   - **Username:** `postgres`
   - **Password:** `xyz`
3. **Save**: Click "Save" to connect to the PostgreSQL server.

You should now see the PostgreSQL server connected and can explore the databases and tables.

---

## Database Schemas

The database consists of several tables designed to manage different aspects of the application. Below is an overview of each schema.

### 1. Organizations

Stores information about organizations registered in the system.

```sql
CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL,
    contact_email TEXT UNIQUE NOT NULL,
    contact_phone_number TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Customers

Stores customer information.

```sql
CREATE TABLE IF NOT EXISTS customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Drivers

Stores driver information associated with organizations.

```sql
CREATE TABLE IF NOT EXISTS drivers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    rating TEXT NOT NULL,
    license_number TEXT UNIQUE NOT NULL,
    phone_number TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    organization_id UUID REFERENCES organizations(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Locations

Stores the geographical locations of drivers.

```sql
CREATE TABLE IF NOT EXISTS locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    driver_id UUID REFERENCES drivers(id),
    name TEXT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Vehicles

Stores vehicle information associated with organizations.

```sql
CREATE TABLE IF NOT EXISTS vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    license_plate TEXT UNIQUE NOT NULL,
    vehicle_type TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    people INTEGER DEFAULT 0,
    organization_id UUID REFERENCES organizations(id),
    operating_location TEXT NOT NULL,
    status BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Reports

Stores reports filed regarding drivers.

```sql
CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reporter_first_name TEXT NOT NULL,
    reporter_last_name TEXT NOT NULL,
    license_number TEXT NOT NULL REFERENCES drivers(license_number),
    description TEXT NOT NULL,
    type TEXT NOT NULL,
    driver_id UUID REFERENCES drivers(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7. Emergency Reports

Stores emergency reports associated with vehicles and organizations.

```sql
CREATE TABLE IF NOT EXISTS emergency (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reporter_first_name TEXT NOT NULL,
    reporter_last_name TEXT NOT NULL,
    license_plate TEXT NOT NULL REFERENCES vehicles(license_plate),
    description TEXT,
    ratings TEXT,
    status TEXT DEFAULT 'open',
    severity_level TEXT NOT NULL,
    organization_id UUID REFERENCES organizations(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);
```

### 8. Ride

Stores ride information between pickup and dropoff locations.

```sql
CREATE TABLE IF NOT EXISTS ride (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pickup_location TEXT NOT NULL,
    dropoff_location TEXT NOT NULL,
    ride_date DATE NOT NULL,
    ride_time TIME NOT NULL,
    number_of_passengers INTEGER NOT NULL CHECK (number_of_passengers > 0),
    vehicle_type TEXT NOT NULL,
    license_plate TEXT NOT NULL REFERENCES vehicles(license_plate),
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    is_in_progress BOOLEAN NOT NULL DEFAULT FALSE,
    organization_id UUID REFERENCES organizations(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);
```

### 9. Hail

Stores information about ride hailing events.

```sql
CREATE TABLE IF NOT EXISTS hail (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    driver_license TEXT NOT NULL REFERENCES drivers(license_number),
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    hail_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 10. Payments

Stores payment transaction information between customers and drivers.

```sql
CREATE TABLE IF NOT EXISTS payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL REFERENCES customers(id),
    driver_id UUID NOT NULL REFERENCES drivers(id),
    amount DECIMAL(10, 2) NOT NULL,
    payment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    pickup_location TEXT NOT NULL,
    dropoff_location TEXT NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 11. Vehicle Speeds

Stores the latest speed information for each vehicle.

```sql
CREATE TABLE IF NOT EXISTS vehicle_speeds (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    license_plate TEXT NOT NULL REFERENCES vehicles(license_plate),
    speed DECIMAL(5, 2) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_license_plate UNIQUE (license_plate)
);
```

---

## Testing the Setup

After starting the services and initializing the database, you can perform tests to ensure everything is working correctly.

**Access the PostgreSQL database via pgAdmin and verify the tables:**

1. Open pgAdmin and connect to the PostgreSQL server.
2. Navigate to the `postgres` database.
3. Expand the `Schemas` > `public` > `Tables` section.
4. Verify that all the tables listed in the [Database Schemas](#database-schemas) section are present.
5. Run SQL queries to insert and retrieve data from these tables to ensure they are functioning correctly.

**Example Test Query:**
```sql
SELECT * FROM organizations;
```

---

## Notes

- **API Layer Management**: The API layer handles the creation and management of all database schemas and provides functions to interact with the database. Ensure that the API is properly configured to connect to the PostgreSQL service.
  
- **Docker Compose Modifications**: The `docker-compose.yml` file was modified from its original source ([felipewom/docker-compose-postgres](https://github.com/felipewom/docker-compose-postgres)) to suit the specific needs of this project.

- **Data Persistence**: The use of Docker volumes (`db-data` and `pgadmin-data`) ensures that your data persists across container restarts and recreations.

---


## References

- **Docker Documentation**: [https://docs.docker.com/](https://docs.docker.com/)
- **Docker Compose Documentation**: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
- **PostgreSQL Documentation**: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
- **pgAdmin Documentation**: [https://www.pgadmin.org/docs/](https://www.pgadmin.org/docs/)
- **psycopg2 Documentation**: [https://www.psycopg.org/docs/](https://www.psycopg.org/docs/)
- **Original Docker Compose Source**: [felipewom/docker-compose-postgres](https://github.com/felipewom/docker-compose-postgres)

---

**Maintained by [TTR].**