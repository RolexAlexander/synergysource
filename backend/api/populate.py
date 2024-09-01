import json
from database import Database

class DatabasePopulator:
    def __init__(self, db):
        self.db = db

    def load_json(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def populate_customers(self, customers_file):
        customers = self.load_json(customers_file)
        for customer in customers:
            customer_id = self.db.create_customer(
                name=customer["name"],
                email=customer["email"],
                phone_number=customer["phone_number"],
                password=customer["password"]
            )
            print(f"Customer created with ID: {customer_id}")

    def populate_organizations(self, organizations_file):
        organizations = self.load_json(organizations_file)
        for organization in organizations:
            organization_id = self.db.create_organization(
                name=organization["name"],
                contact_email=organization["contact_email"],
                contact_phone_number=organization["contact_phone_number"],
                password=organization["password"]
            )
            print(f"Organization created with ID: {organization_id}")

    def populate_drivers(self, drivers_file):
        drivers = self.load_json(drivers_file)
        for driver in drivers:
            driver_id = self.db.create_driver(
                name=driver["name"],
                rating=driver["rating"],
                license_number=driver["license_number"],
                phone_number=driver["phone_number"],
                password=driver["password"],
                organization_id=driver["organization_id"]
            )
            print(f"Driver created with ID: {driver_id}")

    def populate_locations(self, locations_file):
        locations = self.load_json(locations_file)
        for location in locations:
            location_id = self.db.create_location(
                driver_id=location["driver_id"],
                name=location["name"],
                latitude=location["latitude"],
                longitude=location["longitude"]
            )
            print(f"Location created with ID: {location_id}")

    def populate_vehicles(self, vehicles_file):
        vehicles = self.load_json(vehicles_file)
        for vehicle in vehicles:
            vehicle_id = self.db.create_vehicle(
                license_plate=vehicle["license_plate"],
                capacity=vehicle["capacity"],
                organization_id=vehicle["organization_id"],
                operating_location=vehicle["operating_location"],
                vehicle_type=vehicle["vehicle_type"],
                status=vehicle["status"]
            )
            print(f"Vehicle created with ID: {vehicle_id}")

if __name__ == "__main__":
    db = Database()  # Assuming your Database class is already defined
    populator = DatabasePopulator(db)

    populator.populate_customers('./data/customers.json')
    populator.populate_organizations('./data/organisations.json')
    populator.populate_drivers('./data/drivers.json')
    populator.populate_locations('./data/locations.json')
    populator.populate_vehicles('./data/vehicles.json')

    db.close()
