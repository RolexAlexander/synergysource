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
        insert_query = '''
        INSERT INTO customers (name, email, phone_number, password)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        '''
        self.cursor.execute(insert_query, (name, email, phone_number, password))
        self.connection.commit()
        return self.cursor.fetchone()[0]

    def read_customer(self, customer_id):
        select_query = '''
        SELECT * FROM customers WHERE id = %s
        '''
        self.cursor.execute(select_query, (customer_id,))
        return self.cursor.fetchone()

    def update_customer(self, customer_id, name=None, email=None, phone_number=None, password=None):
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

    def delete_customer(self, customer_id):
        delete_query = '''
        DELETE FROM customers WHERE id = %s
        '''
        self.cursor.execute(delete_query, (customer_id,))
        self.connection.commit()

    def create_driver(self, name, rating, license_number, phone_number, password, organization_id):
        insert_query = '''
        INSERT INTO drivers (name, rating, license_number, phone_number, password, organization_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        '''
        self.cursor.execute(insert_query, (name, rating, license_number, phone_number, password, organization_id))
        self.connection.commit()
        return self.cursor.fetchone()[0]

    def read_driver(self, driver_id):
        select_query = '''
        SELECT * FROM drivers WHERE id = %s
        '''
        self.cursor.execute(select_query, (driver_id,))
        return self.cursor.fetchone()

    def update_driver(self, driver_id, name=None, rating=None, license_number=None, phone_number=None, password=None, organization_id=None):
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

    def delete_driver(self, driver_id):
        delete_query = '''
        DELETE FROM drivers WHERE id = %s
        '''
        self.cursor.execute(delete_query, (driver_id,))
        self.connection.commit()

    def create_organization(self, name, contact_email, contact_phone_number, password):
        insert_query = '''
        INSERT INTO organizations (name, contact_email, contact_phone_number, password)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        '''
        self.cursor.execute(insert_query, (name, contact_email, contact_phone_number, password))
        self.connection.commit()
        return self.cursor.fetchone()[0]

    def read_organization(self, organization_id):
        select_query = '''
        SELECT * FROM organizations WHERE id = %s
        '''
        self.cursor.execute(select_query, (organization_id,))
        return self.cursor.fetchone()

    def update_organization(self, organization_id, name=None, contact_email=None, contact_phone_number=None):
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

    def delete_organization(self, organization_id):
        delete_query = '''
        DELETE FROM organizations WHERE id = %s
        '''
        self.cursor.execute(delete_query, (organization_id,))
        self.connection.commit()

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
        name="Safe Rides Inc.",
        contact_email="contact@saferides.com",
        contact_phone_number="555-9999",
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

    # Delete the driver
    db.delete_driver(driver_id)
    print("Driver deleted successfully")

    # Delete the organization
    db.delete_organization(organization_id)
    print("Organization deleted successfully")

    # Close the database connection
    db.close()