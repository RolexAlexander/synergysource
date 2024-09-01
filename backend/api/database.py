import psycopg2

class Database:
    def __init__(self):
        # TODO: Add configuration for init database
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            # creds were hard coded for now
            # TODO: move to env vars
            self.connection = psycopg2.connect(
                user="postgres",
                password="VwYbRMxFVmVXQggoFYxHiCuZckYCyMjQ",
                host="autorack.proxy.rlwy.net",
                port="52796",
                database="postgres"
            )
            self.cursor = self.connection.cursor()
            self.create_tables()
            print("Connected to the database and tables created successfully")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def create_tables(self):
        # all table schemas were hard coded for now
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
            ''',
            "reports": '''
                CREATE TABLE IF NOT EXISTS reports (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    reporter_first_name TEXT NOT NULL,
                    reporter_last_name TEXT NOT NULL,
                    license_number TEXT NOT NULL REFERENCES drivers(license_number),
                    description TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    type TEXT NOT NULL,
                    driver_id UUID REFERENCES drivers(id)
                )
            ''',
            "emergency_reports": '''
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
                )
            ''',
            "ride": '''
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
                )
            ''',
            "hail": '''
                    CREATE TABLE IF NOT EXISTS hail (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        driver_license TEXT NOT NULL REFERENCES drivers(license_number),
                        latitude FLOAT NOT NULL,
                        longitude FLOAT NOT NULL,
                        hail_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            "payments": '''
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
                )
            ''',
            "vehicle_speed": '''
                CREATE TABLE IF NOT EXISTS vehicle_speeds (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    license_plate TEXT NOT NULL REFERENCES vehicles(license_plate),
                    speed DECIMAL(5, 2) NOT NULL,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT unique_license_plate UNIQUE (license_plate)
                )
            ''',
        }

        # create tables
        for table_name, create_query in tables.items():
            self.cursor.execute(create_query)
            print(f"Table '{table_name}' created successfully")
        
        self.connection.commit()

    def close(self):
        # function to close the connection
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
                    vehicles.people,
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
                    "people": row[4],
                    "latitude": row[5],
                    "longitude": row[6]
                }
                vehicles_list.append(vehicle_dict)
            return vehicles_list

        except Exception as e:
            self.connection.rollback()  # Roll back the transaction on error
            print(f"Error occurred: {e}")

    def create_report(self, reporter_first_name, reporter_last_name, license_number, description, report_type, driver_id=None):
        try:
            insert_query = '''
            INSERT INTO reports (reporter_first_name, reporter_last_name, license_number, description, type, driver_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            '''
            self.cursor.execute(insert_query, (reporter_first_name, reporter_last_name, license_number, description, report_type, driver_id))
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")

    def get_report_by_id(self, report_id):
        try:
            select_query = '''
            SELECT * FROM reports WHERE id = %s
            '''
            self.cursor.execute(select_query, (report_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error occurred: {e}")

    def update_report(self, report_id, description=None, report_type=None):
        try:
            update_query = '''
            UPDATE reports
            SET description = COALESCE(%s, description), type = COALESCE(%s, type)
            WHERE id = %s
            RETURNING id
            '''
            self.cursor.execute(update_query, (description, report_type, report_id))
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")
    
    def delete_report(self, report_id):
        try:
            delete_query = '''
            DELETE FROM reports WHERE id = %s
            '''
            self.cursor.execute(delete_query, (report_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")

    def create_emergency_report(self, reporter_first_name, reporter_last_name, license_plate, severity_level, description=None, ratings=None, organization_id=None):
        try:
            insert_query = '''
            INSERT INTO emergency (reporter_first_name, reporter_last_name, license_plate, severity_level, description, ratings, organization_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            '''
            self.cursor.execute(insert_query, (reporter_first_name, reporter_last_name, license_plate, severity_level, description, ratings, organization_id))
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")

    def get_emergency_report_by_id(self, emergency_id):
        try:
            select_query = '''
            SELECT * FROM emergency WHERE id = %s
            '''
            self.cursor.execute(select_query, (emergency_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error occurred: {e}")

    def update_emergency_report(self, emergency_id, status=None, resolved_at=None):
        try:
            update_query = '''
            UPDATE emergency
            SET status = COALESCE(%s, status), resolved_at = COALESCE(%s, resolved_at)
            WHERE id = %s
            RETURNING id
            '''
            self.cursor.execute(update_query, (status, resolved_at, emergency_id))
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")

    def delete_emergency_report(self, emergency_id):
        try:
            delete_query = '''
            DELETE FROM emergency WHERE id = %s
            '''
            self.cursor.execute(delete_query, (emergency_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")

    def create_ride(self, pickup_location, dropoff_location, ride_date, ride_time, number_of_passengers, vehicle_type, license_plate, organization_id, is_completed=False, is_in_progress=False):
        try:
            insert_query = '''
            INSERT INTO ride (pickup_location, dropoff_location, ride_date, ride_time, number_of_passengers, vehicle_type, license_plate, organization_id, is_completed, is_in_progress)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            '''
            self.cursor.execute(insert_query, (pickup_location, dropoff_location, ride_date, ride_time, number_of_passengers, vehicle_type, license_plate, organization_id, is_completed, is_in_progress))
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")

    def get_ride_by_id(self, ride_id):
        try:
            select_query = '''
            SELECT * FROM ride WHERE id = %s
            '''
            self.cursor.execute(select_query, (ride_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error occurred: {e}")

    def update_ride(self, ride_id, is_completed=None, is_in_progress=None, completed_at=None):
        try:
            update_query = '''
            UPDATE ride
            SET is_completed = COALESCE(%s, is_completed), is_in_progress = COALESCE(%s, is_in_progress), completed_at = COALESCE(%s, completed_at)
            WHERE id = %s
            RETURNING id
            '''
            self.cursor.execute(update_query, (is_completed, is_in_progress, completed_at, ride_id))
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")

    def delete_ride(self, ride_id):
        try:
            delete_query = '''
            DELETE FROM ride WHERE id = %s
            '''
            self.cursor.execute(delete_query, (ride_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")

    def create_hail(self, driver_license, latitude, longitude):
        try:
            insert_query = '''
            INSERT INTO hail (driver_license, latitude, longitude)
            VALUES (%s, %s, %s)
            RETURNING id
            '''
            self.cursor.execute(insert_query, (driver_license, latitude, longitude))
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")

    def get_hail_by_id(self, hail_id):
        try:
            select_query = '''
            SELECT * FROM hail WHERE id = %s
            '''
            self.cursor.execute(select_query, (hail_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error occurred: {e}")

    def update_hail(self, hail_id, latitude=None, longitude=None):
        try:
            update_query = '''
            UPDATE hail
            SET latitude = COALESCE(%s, latitude), longitude = COALESCE(%s, longitude)
            WHERE id = %s
            RETURNING id
            '''
            self.cursor.execute(update_query, (latitude, longitude, hail_id))
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")

    def delete_hail(self, hail_id):
        try:
            delete_query = '''
            DELETE FROM hail WHERE id = %s
            '''
            self.cursor.execute(delete_query, (hail_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")

    def create_payment(self, customer_id, driver_id, amount, pickup_location, dropoff_location, latitude=None, longitude=None):
        try:
            insert_query = '''
            INSERT INTO payment (customer_id, driver_id, amount, pickup_location, dropoff_location, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            '''
            self.cursor.execute(insert_query, (customer_id, driver_id, amount, pickup_location, dropoff_location, latitude, longitude))
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")

    def get_payment_by_id(self, payment_id):
        try:
            select_query = '''
            SELECT * FROM payment WHERE id = %s
            '''
            self.cursor.execute(select_query, (payment_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error occurred: {e}")

    def update_payment(self, payment_id, amount=None, pickup_location=None, dropoff_location=None):
        try:
            update_query = '''
            UPDATE payment
            SET amount = COALESCE(%s, amount), pickup_location = COALESCE(%s, pickup_location), dropoff_location = COALESCE(%s, dropoff_location)
            WHERE id = %s
            RETURNING id
            '''
            self.cursor.execute(update_query, (amount, pickup_location, dropoff_location, payment_id))
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")

    def delete_payment(self, payment_id):
        try:
            delete_query = '''
            DELETE FROM payment WHERE id = %s
            '''
            self.cursor.execute(delete_query, (payment_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")

    def list_reports_by_organization(self, organization_id):
        try:
            query = '''
            SELECT r.id, r.reporter_first_name, r.reporter_last_name, r.license_number, r.description, r.created_at, r.type 
            FROM reports r
            JOIN drivers d ON r.driver_id = d.id
            WHERE d.organization_id = %s
            '''
            self.cursor.execute(query, (organization_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error occurred: {e}")

    def list_drivers_by_organization(self, organization_id):
        try:
            query = '''
            SELECT id, name, rating, license_number, phone_number, created_at 
            FROM drivers
            WHERE organization_id = %s
            '''
            self.cursor.execute(query, (organization_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error occurred: {e}")

    def list_all_organizations_drivers_vehicles_locations(self):
        try:
            query = '''
            SELECT o.id AS organization_id, o.name AS organization_name, o.contact_email, o.contact_phone_number, 
                d.id AS driver_id, d.name AS driver_name, d.rating, d.license_number, 
                v.id AS vehicle_id, v.license_plate, v.vehicle_type, v.capacity, v.status, 
                l.id AS location_id, l.name AS location_name, l.latitude, l.longitude
            FROM organizations o
            LEFT JOIN drivers d ON o.id = d.organization_id
            LEFT JOIN vehicles v ON o.id = v.organization_id
            LEFT JOIN locations l ON d.id = l.driver_id
            '''
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error occurred: {e}")

    def list_rides_by_user_driver_organization(self, user_id=None, driver_id=None, organization_id=None):
        try:
            query = '''
            SELECT r.id, r.pickup_location, r.dropoff_location, r.ride_date, r.ride_time, r.is_completed, r.is_in_progress, r.created_at
            FROM ride r
            WHERE (%s IS NULL OR r.organization_id = %s)
            AND (%s IS NULL OR EXISTS (
                SELECT 1
                FROM payments p
                WHERE p.customer_id = %s
                AND p.ride_id = r.id
            ))
            AND (%s IS NULL OR EXISTS (
                SELECT 1
                FROM payments p
                WHERE p.driver_id = %s
                AND p.ride_id = r.id
            ))
            '''
            self.cursor.execute(query, (organization_id, organization_id, user_id, user_id, driver_id, driver_id))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error occurred: {e}")
    def list_available_rides(self):
        try:
            query = '''
            SELECT id, pickup_location, dropoff_location, ride_date, ride_time, vehicle_type, license_plate
            FROM ride
            WHERE is_completed = FALSE AND is_in_progress = FALSE
            '''
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error occurred: {e}")

    def list_dispatched_rides(self):
        try:
            query = '''
            SELECT id, pickup_location, dropoff_location, ride_date, ride_time, vehicle_type, license_plate
            FROM ride
            WHERE is_in_progress = TRUE AND is_completed = FALSE
            '''
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error occurred: {e}")

    def hail_by_customer_driver_organization(self, customer_id=None, driver_id=None, organization_id=None):
        try:
            query = '''
            SELECT h.id, h.driver_license, h.latitude, h.longitude, h.hail_time
            FROM hail h
            JOIN drivers d ON h.driver_license = d.license_number
            WHERE (%s IS NULL OR EXISTS (SELECT 1 FROM payments p WHERE p.customer_id = %s))
            AND (%s IS NULL OR h.driver_license = %s)
            AND (%s IS NULL OR d.organization_id = %s)
            '''
            self.cursor.execute(query, (customer_id, customer_id, driver_id, driver_id, organization_id, organization_id))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error occurred: {e}")

    def list_payment_history(self):
        try:
            query = '''
            SELECT p.id, p.amount, p.payment_date, p.pickup_location, p.dropoff_location, p.latitude, p.longitude, p.created_at
            FROM payments p
            JOIN customers c ON p.customer_id = c.id
            JOIN drivers d ON p.driver_id = d.id
            '''
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error occurred: {e}")

    def get_location_by_driver_id_or_license(self, driver_id=None, license_number=None):
        try:
            query = '''
            SELECT l.id, l.name, l.latitude, l.longitude, l.created_at
            FROM locations l
            JOIN drivers d ON l.driver_id = d.id
            WHERE (%s IS NOT NULL AND l.driver_id = %s) OR (%s IS NOT NULL AND d.license_number = %s)
            '''
            self.cursor.execute(query, (driver_id, driver_id, license_number, license_number))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error occurred: {e}")

    def get_vehicle_status(self, vehicle_id=None, license_plate=None):
        try:
            query = '''
            SELECT v.id, v.license_plate, v.vehicle_type, v.capacity, v.status
            FROM vehicles v
            WHERE (%s IS NOT NULL AND v.id = %s) OR (%s IS NOT NULL AND v.license_plate = %s)
            '''
            self.cursor.execute(query, (vehicle_id, vehicle_id, license_plate, license_plate))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error occurred: {e}")

    def get_driver_details(self, driver_id=None, license_number=None):
        try:
            query = '''
            SELECT d.id, d.name, d.rating, d.license_number, d.phone_number, d.created_at
            FROM drivers d
            WHERE (%s IS NOT NULL AND d.id = %s) OR (%s IS NOT NULL AND d.license_number = %s)
            '''
            self.cursor.execute(query, (driver_id, driver_id, license_number, license_number))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error occurred: {e}")

    def get_organization_details(self, organization_id):
        try:
            query = '''
            SELECT id, name, contact_email, contact_phone_number, created_at
            FROM organizations
            WHERE id = %s
            '''
            self.cursor.execute(query, (organization_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error occurred: {e}")

    def get_active_rides_by_organization(self, organization_id):
        try:
            query = '''
            SELECT id, pickup_location, dropoff_location, ride_date, ride_time, vehicle_type, license_plate, is_in_progress, is_completed
            FROM ride
            WHERE organization_id = %s AND is_in_progress = TRUE AND is_completed = FALSE
            '''
            self.cursor.execute(query, (organization_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error occurred: {e}")

    def log_speed(self, license_plate, speed):
        try:
            # Upsert query: if the license_plate already exists, update the speed; otherwise, insert a new entry.
            upsert_query = '''
            INSERT INTO vehicle_speeds (license_plate, speed, recorded_at)
            VALUES (%s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (license_plate) 
            DO UPDATE SET speed = EXCLUDED.speed, recorded_at = EXCLUDED.recorded_at;
            '''
            self.cursor.execute(upsert_query, (license_plate, speed))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")



    def get_vehicle_speeds(self, license_plate):
        try:
            select_query = '''
            SELECT * FROM vehicle_speeds WHERE license_plate = %s ORDER BY recorded_at DESC
            '''
            self.cursor.execute(select_query, (license_plate,))
            return self.cursor.fetchall()
        except Exception as e:
            self.connection.rollback()
            print(f"Error occurred: {e}")
            return None


if __name__ == "__main__":
    # Example usage: 
    # Initialize the database
    db = Database()

    # PLEASE DON'T RUN ALL AT ONCE. It was NOT intended to be utilised that way.
    # Its intended to show how to utilise the methods within the database class.
    
    # Example usage for customers
    # Create a customer
    # customer_id = db.create_customer(
    #     name="John Doe",
    #     email="johe@doqwe.com",
    #     phone_number="2321234",
    #     password="password123"
    # )
    # print(f"Customer created with ID: {customer_id}")

    # # Read the customer details
    # customer_details = db.read_customer(customer_id)
    # print(f"Customer details: {customer_details}")

    # # Update the customer details
    # db.update_customer(
    #     customer_id,
    #     name="John Doe Jr.",
    #     email="johnqwjr@example.com"
    # )
    # print("Customer updated successfully")

    # # Example usage for organizations
    # # Create an organization
    # organization_id = db.create_organization(
    #     name="Major Ridaaaes Inc.",
    #     contact_email="zzzzzwe@guyrides.com",
    #     contact_phone_number="9655-5555",
    #     password="organizationpass"
    # )
    # print(f"Organization created with ID: {organization_id}")

    # # Example usage for drivers
    # # Create a driver
    # driver_id = db.create_driver(
    #     name="Alice Smith",
    #     rating="5 stars",
    #     license_number="CCB1234",
    #     phone_number="559345-5678",
    #     password="driverpass",
    #     organization_id=organization_id  # Use the actual organization ID
    # )
    # print(f"Driver created with ID: {driver_id}")

    # # Read the driver details
    # driver_details = db.read_driver(driver_id)
    # print(f"Driver details: {driver_details}")

    # # Update the driver details
    # db.update_driver(
    #     driver_id,
    #     rating="4.5 stars"
    # )
    # print("Driver updated successfully")

    # # 1. Create a new location
    # location_id = db.create_location(
    #     driver_id=driver_id,
    #     name='Location A',
    #     latitude=12.34,
    #     longitude=56.78
    # )
    # print(f"New location created with ID: {location_id}")

    # # 2. Retrieve a location by ID
    # location = db.get_location(location_id)
    # print(f"Retrieved location: {location}")

    # # 3. Update a location's details
    # db.update_location(
    #     location_id=location_id,
    #     name='Updated Location A',
    #     latitude=13.34,   # Only update the latitude
    #     longitude=57.78   # Only update the longitude
    # )
    # updated_location = db.get_location(location_id)
    # print(f"Updated location: {updated_location}")

    # # 4. Delete a location
    # db.delete_location(location_id)
    # print(f"Location with ID {location_id} deleted.")


    # # ---- CRUD operations for 'vehicles' table ----

    # # 1. Create a new vehicle
    # vehicle_id = db.create_vehicle(
    #     license_plate='ABC1234',
    #     capacity=16,
    #     organization_id=organization_id,
    #     operating_location='Location A',
    #     vehicle_type="vehicle_type",
    #     status=True  # Default is True, but showing it for clarity
    # )
    # print(f"New vehicle created with ID: {vehicle_id}")

    # # 2. Retrieve a vehicle by ID
    # vehicle = db.get_vehicle(vehicle_id)
    # print(f"Retrieved vehicle: {vehicle}")

    # # 3. Update a vehicle's details
    # db.update_vehicle(
    #     vehicle_id=vehicle_id,
    #     license_plate='XYZ789444',  # Updating the license plate
    #     capacity=5,             # Updating the capacity
    #     operating_location='Updated Location A',
    #     vehicle_type="bus"
    # )
    # updated_vehicle = db.get_vehicle(vehicle_id)
    # print(f"Updated vehicle: {updated_vehicle}")

    # print("Driver location by ID:")
    # print(db.get_location_by_driver_id_or_license(driver_id=driver_id))

    # res = db.update_people_in_vehicle("XYZ789", 5)
    # print(f"People in vehicle updated: {res}")

    # vehicles = db.get_all_vehicles_with_drivers()
    # print(vehicles)

    # # Create a report
    # report_id = db.create_report(
    #     reporter_first_name="John",
    #     reporter_last_name="Doe",
    #     license_number="ABC1234",
    #     description="A minor accident",
    #     report_type="Accident",
    #     driver_id=driver_id
    # )
    # print(f"Created report with ID: {report_id}")

    # # Get a report by ID
    # report = db.get_report_by_id(report_id)
    # print("Report Details:", report)

    # # Update the report's description and type
    # updated_report_id = db.update_report(
    #     report_id=report_id,
    #     description="A minor collision with no injuries",
    #     report_type="Minor Accident"
    # )
    # print(f"Updated report with ID: {updated_report_id}")

    # # Delete the report
    # db.delete_report(report_id)
    # print(f"Deleted report with ID: {report_id}")

    # # Create an emergency report
    # emergency_report_id = db.create_emergency_report(
    #     reporter_first_name="Jane",
    #     reporter_last_name="Smith",
    #     license_plate="XYZ789",
    #     severity_level="High",
    #     description="Emergency: Vehicle fire",
    #     ratings=4.5,
    #     organization_id=organization_id
    # )
    # print(f"Created emergency report with ID: {emergency_report_id}")

    # # Get an emergency report by ID
    # emergency_report = db.get_emergency_report_by_id(str(emergency_report_id))
    # print("Emergency Report Details:", emergency_report)

    # # Update the emergency report's status and resolved_at timestamp
    # updated_emergency_report_id = db.update_emergency_report(
    #     emergency_id=str(emergency_report_id),
    #     status="Resolved",
    #     resolved_at="2024-08-31 10:00:00"
    # )
    # print(f"Updated emergency report with ID: {updated_emergency_report_id}")

    # # Delete the emergency report
    # db.delete_emergency_report(str(emergency_report_id))
    # print(f"Deleted emergency report with ID: {emergency_report_id}")

    # # Create a ride
    # ride_id = db.create_ride(
    #     pickup_location="Downtown",
    #     dropoff_location="Uptown",
    #     ride_date="2024-09-01",
    #     ride_time="08:00:00",
    #     number_of_passengers=3,
    #     vehicle_type="SUV",
    #     license_plate="XYZ789",
    #     organization_id=organization_id
    # )
    # print(f"Created ride with ID: {ride_id}")

    # # Get a ride by ID
    # ride = db.get_ride_by_id(str(ride_id))
    # print("Ride Details:", ride)

    # # Update the ride's status to completed and set completed_at timestamp
    # updated_ride_id = db.update_ride(
    #     ride_id=str(ride_id),
    #     is_completed=True,
    #     completed_at="2024-09-01 08:45:00"
    # )
    # print(f"Updated ride with ID: {updated_ride_id}")

    # # Delete the ride
    # db.delete_ride(ride_id)
    # print(f"Deleted ride with ID: {ride_id}")

    # # Create a hail
    # hail_id = db.create_hail(
    #     driver_license="ABC1234",
    #     latitude=40.712776,
    #     longitude=-74.005974
    # )
    # print(f"Created hail with ID: {hail_id}")

    # # Get a hail by ID
    # hail = db.get_hail_by_id(str(hail_id))
    # print("Hail Details:", hail)

    # # Update the hail's location
    # updated_hail_id = db.update_hail(
    #     hail_id=str(hail_id),
    #     latitude=40.730610,
    #     longitude=-73.935242
    # )
    # print(f"Updated hail with ID: {updated_hail_id}")

    # # Delete the hail
    # db.delete_hail(str(hail_id))
    # print(f"Deleted hail with ID: {hail_id}")

    # driver_id=db.create_driver(name="John Doe the third", rating="4.5", license_number="ABweweC123", phone_number="111123-456-7890", password="password", organization_id=organization_id)
    # print(f"Created driver with ID: {driver_id}")

    # # Create a payment
    # payment_id = db.create_payment(
    #     customer_id=customer_id,
    #     driver_id=driver_id,
    #     amount=50.00,
    #     pickup_location="Central Park",
    #     dropoff_location="Times Square",
    #     latitude=40.785091,
    #     longitude=-73.968285
    # )
    # print(f"Created payment with ID: {payment_id}")

    # # Get a payment by ID
    # payment = db.get_payment_by_id(str(payment_id))
    # print("Payment Details:", payment)

    # # Update the payment details
    # updated_payment_id = db.update_payment(
    #     payment_id=str(payment_id),
    #     amount=55.00,
    #     pickup_location="Central Park West",
    #     dropoff_location="Times Square"
    # )
    # print(f"Updated payment with ID: {updated_payment_id}")

    # # Delete the payment
    # db.delete_payment(str(payment_id))
    # print(f"Deleted payment with ID: {payment_id}")

    # # List all reports by organization
    # reports = db.list_reports_by_organization(organization_id)
    # print("Reports by Organization:", reports)

    # # List all drivers by organization
    # drivers = db.list_drivers_by_organization(organization_id)
    # print("Drivers by Organization:", drivers)

    # # List all organizations with their drivers, vehicles, and locations
    # organizations_info = db.list_all_organizations_drivers_vehicles_locations()
    # print("Organizations Information:", organizations_info)

    # # Test list_rides_by_user_driver_organization
    # print("Testing list_rides_by_user_driver_organization:")
    # rides_by_user = db.list_rides_by_user_driver_organization(user_id=customer_id)
    # print(rides_by_user)

    # rides_by_driver = db.list_rides_by_user_driver_organization(driver_id=driver_id)
    # print(rides_by_driver)

    # rides_by_organization = db.list_rides_by_user_driver_organization(organization_id=organization_id)
    # print(rides_by_organization)

    # # Test list_available_rides
    # print("\nTesting list_available_rides:")
    # available_rides = db.list_available_rides()
    # print(available_rides)

    # # Test list_dispatched_rides
    # print("\nTesting list_dispatched_rides:")
    # dispatched_rides = db.list_dispatched_rides()
    # print(dispatched_rides)
    
    # # Example calls to the methods
    # print("Available rides:")
    # print(db.list_available_rides())
    
    # print("Dispatched rides:")
    # print(db.list_dispatched_rides())
    
    # print("Payment history:")
    # print(db.list_payment_history())
    
    # print("Vehicle status by ID:")
    # print(db.get_vehicle_status(vehicle_id=vehicle_id))
    
    # print("Driver details by license number:")
    # print(db.get_driver_details(license_number="ABC123"))
    
    # print("Organization details:")
    # print(db.get_organization_details(organization_id=organization_id))
    
    # print("Active rides by organization:")
    # print(db.get_active_rides_by_organization(organization_id=organization_id))
    

    # # Delete the customer
    # db.delete_customer(customer_id)
    # print("Customer deleted successfully")

    
    # # 4. Delete a vehicle
    # db.delete_vehicle(vehicle_id)
    # print(f"Vehicle with ID {vehicle_id} deleted.")

    # # Delete the driver
    # db.delete_driver(driver_id)
    # print("Driver deleted successfully")

    # # Delete the organization
    # db.delete_organization(organization_id)
    # print("Organization deleted successfully")

    # Close the database connection
    db.close()