import psycopg2

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
                host="localhost",
                port="15432",
                database="postgres"
            )
            self.cursor = self.connection.cursor()
            self.create_tables()
            print("Connected to the database and tables created successfully")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def create_tables(self):
            tables = {
                "customers": '''
                    CREATE TABLE IF NOT EXISTS customers (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        phone_number TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''',
                "drivers": '''
                    CREATE TABLE IF NOT EXISTS drivers (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        name TEXT NOT NULL,
                        rating TEXT NOT NULL,
                        license_number TEXT UNIQUE NOT NULL,
                        phone_number TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        organization_id UUID REFERENCES organizations(id),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''',
                "organizations": '''
                    CREATE TABLE IF NOT EXISTS organizations (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        name TEXT UNIQUE NOT NULL,
                        contact_email TEXT UNIQUE NOT NULL,
                        contact_phone_number TEXT UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''',
                "ai_predictions": '''
                    CREATE TABLE IF NOT EXISTS ai_predictions (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        prediction_type TEXT NOT NULL,
                        prediction_value JSONB NOT NULL,
                        related_trip_id UUID REFERENCES trips(id),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''',
                "passengers": '''
                    CREATE TABLE IF NOT EXISTS passengers (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        name TEXT NOT NULL,
                        trip_id UUID REFERENCES trips(id),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''',
                "locations": '''
                    CREATE TABLE IF NOT EXISTS locations (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        driver_id UUID REFERENCES drivers(id),
                        name TEXT NOT NULL,
                        latitude FLOAT NOT NULL,
                        longitude FLOAT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''',
                "trips": '''
                    CREATE TABLE IF NOT EXISTS trips (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        driver_id UUID REFERENCES drivers(id),
                        vehicle_id UUID REFERENCES vehicles(id),
                        start_location_id UUID REFERENCES locations(id),
                        end_location_id UUID REFERENCES locations(id),
                        start_time TIMESTAMP,
                        end_time TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''',
                "incidents": '''
                    CREATE TABLE IF NOT EXISTS incidents (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        trip_id UUID REFERENCES trips(id),
                        incident_type TEXT NOT NULL,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''',
                "weather": '''
                    CREATE TABLE IF NOT EXISTS weather (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        location_id UUID REFERENCES locations(id),
                        temperature FLOAT NOT NULL,
                        humidity FLOAT NOT NULL,
                        weather_condition TEXT NOT NULL,
                        forecast_time TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''',
                "vehicles": '''
                    CREATE TABLE IF NOT EXISTS vehicles (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        license_plate TEXT UNIQUE NOT NULL,
                        capacity INTEGER NOT NULL,
                        organization_id UUID REFERENCES organizations(id),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                '''
            }

            for table_name, create_query in tables.items():
                self.cursor.execute(create_query)
            
            self.connection.commit()

# Example usage:
db = Database()
db.close()