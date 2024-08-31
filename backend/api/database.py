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
                port="5432",
                database="postgres"
            )
            self.cursor = self.connection.cursor()
            # self.create_tables()
            print("Connected to the database and tables created successfully")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def create_tables(self):
        # Create tables in the correct order to handle foreign key dependencies
        tables = {
            "organizations": '''
                CREATE TABLE IF NOT EXISTS organizations (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name TEXT UNIQUE NOT NULL,
                    contact_email TEXT UNIQUE NOT NULL,
                    contact_phone_number TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
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
            "vehicles": '''
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
                )
            '''
        }

        for table_name, create_query in tables.items():
            self.cursor.execute(create_query)
            print(f"Table '{table_name}' created successfully")
        
        self.connection.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def create_customer(self, name, email, phone_number, password):
        try: 
            insert_query = '''
            INSERT INTO customers (name, email, phone_number, password)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            '''
            self.cursor.execute(insert_query, (name, email, phone_number, password))
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def read_customer(self, customer_id):
        try: 
            select_query = '''
            SELECT * FROM customers WHERE id = %s
            '''
            self.cursor.execute(select_query, (customer_id,))
            return self.cursor.fetchone()
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def update_customer(self, customer_id, name=None, email=None, phone_number=None, password=None):
        try: 
            update_fields = []
            values = []

            if name:
                update_fields.append("name = %s")
                values.append(name)
            if email:
                update_fields.append("email = %s")
                values.append(email)
            if phone_number:
                update_fields.append("phone_number = %s")
                values.append(phone_number)
            if password:
                update_fields.append("password = %s")
                values.append(password)

            values.append(customer_id)
            update_query = f'''
            UPDATE customers SET {", ".join(update_fields)}
            WHERE id = %s
            '''
            self.cursor.execute(update_query, values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def delete_customer(self, customer_id):
        try:
            delete_query = '''
            DELETE FROM customers WHERE id = %s
            '''
            self.cursor.execute(delete_query, (customer_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def create_driver(self, name, rating, license_number, phone_number, password, organization_id):
        try: 
            insert_query = '''
            INSERT INTO drivers (name, rating, license_number, phone_number, password, organization_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            '''
            self.cursor.execute(insert_query, (name, rating, license_number, phone_number, password, organization_id))
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def read_driver(self, driver_id):
        try: 
            select_query = '''
            SELECT * FROM drivers WHERE id = %s
            '''
            self.cursor.execute(select_query, (driver_id,))
            return self.cursor.fetchone()
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def update_driver(self, driver_id, name=None, rating=None, license_number=None, phone_number=None, password=None, organization_id=None):
        try: 
            update_fields = []
            values = []

            if name:
                update_fields.append("name = %s")
                values.append(name)
            if rating:
                update_fields.append("rating = %s")
                values.append(rating)
            if license_number:
                update_fields.append("license_number = %s")
                values.append(license_number)
            if phone_number:
                update_fields.append("phone_number = %s")
                values.append(phone_number)
            if password:
                update_fields.append("password = %s")
                values.append(password)
            if organization_id:
                update_fields.append("organization_id = %s")
                values.append(organization_id)

            values.append(driver_id)
            update_query = f'''
            UPDATE drivers SET {", ".join(update_fields)}
            WHERE id = %s
            '''
            self.cursor.execute(update_query, values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def delete_driver(self, driver_id):
        try: 
            delete_query = '''
            DELETE FROM drivers WHERE id = %s
            '''
            self.cursor.execute(delete_query, (driver_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def create_organization(self, name, contact_email, contact_phone_number, password):
        try:
            insert_query = '''
            INSERT INTO organizations (name, contact_email, contact_phone_number, password)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            '''
            self.cursor.execute(insert_query, (name, contact_email, contact_phone_number, password))
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def read_organization(self, organization_id):
        try: 
            select_query = '''
            SELECT * FROM organizations WHERE id = %s
            '''
            self.cursor.execute(select_query, (organization_id,))
            return self.cursor.fetchone()
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def update_organization(self, organization_id, name=None, contact_email=None, contact_phone_number=None):
        try: 
            update_fields = []
            values = []

            if name:
                update_fields.append("name = %s")
                values.append(name)
            if contact_email:
                update_fields.append("contact_email = %s")
                values.append(contact_email)
            if contact_phone_number:
                update_fields.append("contact_phone_number = %s")
                values.append(contact_phone_number)

            values.append(organization_id)
            update_query = f'''
            UPDATE organizations SET {", ".join(update_fields)}
            WHERE id = %s
            '''
            self.cursor.execute(update_query, values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def delete_organization(self, organization_id):
        try: 
            delete_query = '''
            DELETE FROM organizations WHERE id = %s
            '''
            self.cursor.execute(delete_query, (organization_id,))
            self.connection.commit()

            # Functions for the 'locations' table
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def create_location(self, driver_id, name, latitude, longitude):
        try:
            query = '''
                INSERT INTO locations (driver_id, name, latitude, longitude)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            '''
            self.cursor.execute(query, (driver_id, name, latitude, longitude))
            location_id = self.cursor.fetchone()[0]
            self.connection.commit()
            return location_id
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def get_location(self, location_id):
        try: 
            query = '''
                SELECT * FROM locations WHERE id = %s;
            '''
            self.cursor.execute(query, (location_id,))
            return self.cursor.fetchone()
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def update_location(self, location_id, name=None, latitude=None, longitude=None):
        try: 
            query = '''
                UPDATE locations
                SET name = COALESCE(%s, name),
                    latitude = COALESCE(%s, latitude),
                    longitude = COALESCE(%s, longitude)
                WHERE id = %s;
            '''
            self.cursor.execute(query, (name, latitude, longitude, location_id))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def delete_location(self, location_id):
        try: 
            query = '''
                DELETE FROM locations WHERE id = %s;
            '''
            self.cursor.execute(query, (location_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")


    # Functions for the 'vehicles' table

    def create_vehicle(self, license_plate, capacity, organization_id, vehicle_type, operating_location, status=True):
        try: 
            query = '''
                INSERT INTO vehicles (license_plate, capacity, organization_id, vehicle_type, operating_location, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
            '''
            self.cursor.execute(query, (license_plate, capacity, organization_id, vehicle_type, operating_location, status))
            vehicle_id = self.cursor.fetchone()[0]
            self.connection.commit()
            return vehicle_id
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def get_vehicle(self, vehicle_id):
        try: 
            query = '''
                SELECT * FROM vehicles WHERE id = %s;
            '''
            self.cursor.execute(query, (vehicle_id,))
            return self.cursor.fetchone()
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def update_vehicle(self, vehicle_id, license_plate=None, capacity=None, organization_id=None, vehicle_type=None, operating_location=None, status=None):
        try: 
            query = '''
                UPDATE vehicles
                SET license_plate = COALESCE(%s, license_plate),
                    capacity = COALESCE(%s, capacity),
                    organization_id = COALESCE(%s, organization_id),
                    operating_location = COALESCE(%s, operating_location),
                    status = COALESCE(%s, status),
                    vehicle_type = COALESCE(%s, vehicle_type)
                WHERE id = %s;
            '''
            self.cursor.execute(query, (license_plate, capacity, organization_id, operating_location, status, vehicle_type, vehicle_id))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def update_people_in_vehicle(self, license_plate, people):
        try:
            query = '''
                UPDATE vehicles
                SET people = %s
                WHERE license_plate = %s
            '''
            self.cursor.execute(query, (people, license_plate))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
            self.connection.rollback()
            print(f"Error: {e}")

    def delete_vehicle(self, vehicle_id):
        try: 
            query = '''
                DELETE FROM vehicles WHERE id = %s;
            '''
            self.cursor.execute(query, (vehicle_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def get_all_vehicles_with_drivers(self):
        try:
            query = '''
                SELECT 
                    drivers.name AS driver_name,
                    vehicles.vehicle_type,
                    vehicles.license_plate,
                    vehicles.capacity,
                    locations.latitude,
                    locations.longitude
                FROM 
                    vehicles
                JOIN 
                    drivers 
                ON 
                    vehicles.organization_id = drivers.organization_id
                JOIN 
                    locations 
                ON 
                    drivers.id = locations.driver_id;
            '''
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            # Converting result to a list of dictionaries
            vehicles_list = []
            for row in result:
                vehicle_dict = {
                    "driver_name": row[0],
                    "vehicle_type": row[1],
                    "license_plate": row[2],
                    "capacity": row[3],
                    "latitude": row[4],
                    "longitude": row[5]
                }
                vehicles_list.append(vehicle_dict)
            return vehicles_list

        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")




if __name__ == "__main__":
    # Example usage: 
    # Initialize the database
    db = Database()

    # Example usage for customers
    # Create a customer
    customer_id = db.create_customer(
        name="John Doe",
        email="johndoe@example.com",
        phone_number="555-1234",
        password="password123"
    )
    print(f"Customer created with ID: {customer_id}")

    # Read the customer details
    customer_details = db.read_customer(customer_id)
    print(f"Customer details: {customer_details}")

    # Update the customer details
    db.update_customer(
        customer_id,
        name="John Doe Jr.",
        email="johnjr@example.com"
    )
    print("Customer updated successfully")

    # Delete the customer
    db.delete_customer(customer_id)
    print("Customer deleted successfully")

    # Example usage for organizations
    # Create an organization
    organization_id = db.create_organization(
        name="Guy Rides Inc.",
        contact_email="contact@guyrides.com",
        contact_phone_number="555-5555",
        password="organizationpass"
    )
    print(f"Organization created with ID: {organization_id}")

    # Example usage for drivers
    # Create a driver
    driver_id = db.create_driver(
        name="Alice Smith",
        rating="5 stars",
        license_number="ABC1234",
        phone_number="555-5678",
        password="driverpass",
        organization_id=organization_id  # Use the actual organization ID
    )
    print(f"Driver created with ID: {driver_id}")

    # Read the driver details
    driver_details = db.read_driver(driver_id)
    print(f"Driver details: {driver_details}")

    # Update the driver details
    db.update_driver(
        driver_id,
        rating="4.5 stars"
    )
    print("Driver updated successfully")

    # 1. Create a new location
    location_id = db.create_location(
        driver_id=driver_id,
        name='Location A',
        latitude=12.34,
        longitude=56.78
    )
    print(f"New location created with ID: {location_id}")

    # 2. Retrieve a location by ID
    location = db.get_location(location_id)
    print(f"Retrieved location: {location}")

    # 3. Update a location's details
    db.update_location(
        location_id=location_id,
        name='Updated Location A',
        latitude=13.34,   # Only update the latitude
        longitude=57.78   # Only update the longitude
    )
    updated_location = db.get_location(location_id)
    print(f"Updated location: {updated_location}")

    # 4. Delete a location
    db.delete_location(location_id)
    print(f"Location with ID {location_id} deleted.")


    # ---- CRUD operations for 'vehicles' table ----

    # 1. Create a new vehicle
    vehicle_id = db.create_vehicle(
        license_plate='ABC123',
        capacity=16,
        organization_id=organization_id,
        operating_location='Location A',
        vehicle_type="vehicle_type",
        status=True  # Default is True, but showing it for clarity
    )
    print(f"New vehicle created with ID: {vehicle_id}")

    # 2. Retrieve a vehicle by ID
    vehicle = db.get_vehicle(vehicle_id)
    print(f"Retrieved vehicle: {vehicle}")

    # 3. Update a vehicle's details
    db.update_vehicle(
        vehicle_id=vehicle_id,
        license_plate='XYZ789',  # Updating the license plate
        capacity=5,             # Updating the capacity
        operating_location='Updated Location A',
        vehicle_type="bus"
    )
    updated_vehicle = db.get_vehicle(vehicle_id)
    print(f"Updated vehicle: {updated_vehicle}")

    res = db.update_people_in_vehicle("XYZ789", 5)
    print(f"People in vehicle updated: {res}")

    vehicles = db.get_all_vehicles_with_drivers()
    print(vehicles)

    # 4. Delete a vehicle
    db.delete_vehicle(vehicle_id)
    print(f"Vehicle with ID {vehicle_id} deleted.")

    # Delete the driver
    db.delete_driver(driver_id)
    print("Driver deleted successfully")

    # Delete the organization
    db.delete_organization(organization_id)
    print("Organization deleted successfully")

    # Close the database connection
    db.close()