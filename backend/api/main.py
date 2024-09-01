from database import Database
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict
import uuid
from fastapi.middleware.cors import CORSMiddleware

# init fast api app
app = FastAPI()

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Initialize the database
db = Database()

# Pydantic models for request bodies
class CustomerCreateRequest(BaseModel):
    name: str
    email: str
    phone_number: str
    password: str

class CustomerUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None

class OrganizationCreateRequest(BaseModel):
    name: str
    contact_email: str
    contact_phone_number: str
    password: str

class DriverCreateRequest(BaseModel):
    name: str
    rating: str
    license_number: str
    phone_number: str
    password: str
    organization_id: UUID

class DriverUpdateRequest(BaseModel):
    rating: Optional[str] = None
    license_number: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None

class LocationCreate(BaseModel):
    driver_id: UUID
    name: str
    latitude: float
    longitude: float

class LocationUpdate(BaseModel):
    name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

class VehicleCreate(BaseModel):
    license_plate: str
    capacity: int
    organization_id: UUID
    operating_location: str
    status: Optional[bool] = True
    vehicle_type: str

class VehicleUpdate(BaseModel):
    license_plate: Optional[str]
    capacity: Optional[int]
    operating_location: Optional[str]
    status: Optional[bool]
    vehicle_type: Optional[str]

class UpdatePeopleRequest(BaseModel):
    license_plate: str
    people: int


class Report(BaseModel):
    reporter_first_name: str
    reporter_last_name: str
    license_number: str
    description: str
    report_type: str
    driver_id: Optional[str] = None

class EmergencyReport(BaseModel):
    reporter_first_name: str
    reporter_last_name: str
    license_plate: str
    severity_level: str
    description: Optional[str] = None
    ratings: Optional[str] = None
    organization_id: Optional[str] = None

class Ride(BaseModel):
    pickup_location: str
    dropoff_location: str
    ride_date: str
    ride_time: str
    number_of_passengers: int
    vehicle_type: str
    license_plate: str
    organization_id: str
    is_completed: Optional[bool] = False
    is_in_progress: Optional[bool] = False

class Hail(BaseModel):
    driver_license: str
    latitude: float
    longitude: float

class Payment(BaseModel):
    customer_id: str
    driver_id: str
    amount: float
    pickup_location: str
    dropoff_location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    pickup_location: Optional[str] = None
    dropoff_location: Optional[str] = None

class SpeedLog(BaseModel):
    license_plate: str
    speed: float

# Customer Endpoints

@app.post("/customers/", response_model=UUID)
def create_customer(customer: CustomerCreateRequest):
    global db
    customer_id = db.create_customer(
        name=customer.name,
        email=customer.email,
        phone_number=customer.phone_number,
        password=customer.password
    )
    return customer_id

@app.get("/customers/{customer_id}")
def read_customer(customer_id: UUID):
    global db
    customer = db.read_customer(str(customer_id))
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"uuid": customer[0], "name": customer[1], "email": customer[2], "phone_number": customer[3], "password": customer[4]}

@app.put("/customers/{customer_id}")
def update_customer(customer_id: UUID, customer: CustomerUpdateRequest):
    global db
    db.update_customer(
        customer_id=str(customer_id),
        name=customer.name,
        email=customer.email,
        phone_number=customer.phone_number,
        password=customer.password
    )
    return {"message": "Customer updated successfully"}

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: UUID):
    global db
    db.delete_customer(str(customer_id))
    return {"message": "Customer deleted successfully"}

# Organization Endpoints

@app.post("/organizations/", response_model=UUID)
def create_organization(organization: OrganizationCreateRequest):
    global db
    organization_id = db.create_organization(
        name=organization.name,
        contact_email=organization.contact_email,
        contact_phone_number=organization.contact_phone_number,
        password=organization.password
    )
    return organization_id

@app.get("/organizations/{organization_id}")
def read_organization(organization_id: UUID):
    global db
    organization = list(db.read_organization(str(organization_id)))
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return {"uuid": organization[0], "name": organization[1], "email": organization[2], "phone_number": organization[3], "password": organization[4]}

@app.put("/organizations/{organization_id}")
def update_organization(organization_id: UUID, organization: OrganizationCreateRequest):
    global db
    db.update_organization(
        organization_id=str(organization_id),
        name=organization.name,
        contact_email=organization.contact_email,
        contact_phone_number=organization.contact_phone_number
    )
    return {"message": "Organization updated successfully"}

@app.delete("/organizations/{organization_id}")
def delete_organization(organization_id: UUID):
    global db
    db.delete_organization(str(organization_id))
    return {"message": "Organization deleted successfully"}

# Driver Endpoints

@app.post("/drivers/", response_model=UUID)
def create_driver(driver: DriverCreateRequest):
    global db
    driver_id = db.create_driver(
        name=driver.name,
        rating=driver.rating,
        license_number=driver.license_number,
        phone_number=driver.phone_number,
        password=driver.password,
        organization_id=str(driver.organization_id)
    )
    return driver_id

@app.get("/drivers/{driver_id}")
def read_driver(driver_id: UUID):
    global db
    driver = db.read_driver(str(driver_id))
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return {"uuid":driver[0], "name": driver[1], "rating": driver[2], "license": driver[3], "phone_number": driver[4], "password": driver[5], "organization_id": driver[6], "created_at": driver[7]}

@app.put("/drivers/{driver_id}")
def update_driver(driver_id: UUID, driver: DriverUpdateRequest):
    global db
    db.update_driver(
        driver_id=str(driver_id),
        rating=driver.rating,
        license_number=driver.license_number,
        phone_number=driver.phone_number,
        password=driver.password
    )
    return {"message": "Driver updated successfully"}

@app.delete("/drivers/{driver_id}")
def delete_driver(driver_id: UUID):
    global db
    db.delete_driver(str(driver_id))
    return {"message": "Driver deleted successfully"}

@app.post("/locations/", response_model=UUID)
def create_location(location: LocationCreate):
    location_id = db.create_location(
        driver_id=str(location.driver_id),
        name=location.name,
        latitude=location.latitude,
        longitude=location.longitude
    )
    return location_id

@app.get("/locations/{location_id}")
def get_location(location_id: UUID):
    location = db.get_location(str(location_id))
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    print(f"location: {location}")
    return {"uuid": location[0], "driver_id": location[1], "name": location[2], "latitude": location[3], "longitude": location[4], "created_at": location[5]}

@app.put("/locations/{location_id}")
def update_location(location_id: UUID, location: LocationUpdate):    
    db.update_location(
        location_id=str(location_id),
        name=location.name,
        latitude=location.latitude,
        longitude=location.longitude
    )
    return {"message": "Location updated successfully"}

@app.delete("/locations/{location_id}")
def delete_location(location_id: UUID):
    db.delete_location(str(location_id))
    return {"message": "Location deleted successfully"}

# ---- Endpoints for 'vehicles' ----

@app.post("/vehicles/", response_model=UUID)
def create_vehicle(vehicle: VehicleCreate):
    vehicle_id = db.create_vehicle(
        license_plate=vehicle.license_plate,
        capacity=vehicle.capacity,
        organization_id=str(vehicle.organization_id),
        operating_location=vehicle.operating_location,
        vehicle_type=vehicle.vehicle_type,
        status=vehicle.status
    )
    return vehicle_id

@app.get("/vehicles/{vehicle_id}")
def get_vehicle(vehicle_id: UUID):
    vehicle = db.get_vehicle(str(vehicle_id))
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {"uuid": vehicle[0], "license_plate": vehicle[1], "vehicle_type": vehicle[2], "capacity": vehicle[3], "people": vehicle[4], "organization_id": vehicle[5], "operating_location": vehicle[6], "status": vehicle[7], "created_at": vehicle[8]}

@app.put("/vehicles/{vehicle_id}")
def update_vehicle(vehicle_id: UUID, vehicle: VehicleUpdate):
    db.update_vehicle(
        vehicle_id=str(vehicle_id),
        license_plate=vehicle.license_plate,
        capacity=vehicle.capacity,
        operating_location=vehicle.operating_location,
        status=vehicle.status,
        vehicle_type=vehicle.vehicle_type
    )
    return {"message": "Vehicle updated successfully"}

@app.get("/ListAllVehicles/", response_model=List)
def get_vehicles():
    vehicles = db.get_all_vehicles_with_drivers()
    if not vehicles:
        raise HTTPException(status_code=404, detail="No vehicles found")
    return vehicles

@app.delete("/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: UUID):
    db.delete_vehicle(str(vehicle_id))
    return {"message": "Vehicle deleted successfully"}

@app.put("/vehicles/update_people/")
def update_people(vehicles: UpdatePeopleRequest):
    return db.update_people_in_vehicle(vehicles.license_plate, vehicles.people)

@app.post("/reports/", response_model=str)
def create_report(report: Report):
    report_id = db.create_report(
        report.reporter_first_name,
        report.reporter_last_name,
        report.license_number,
        report.description,
        report.report_type,
        report.driver_id
    )
    if report_id:
        return {"id": report_id}
    raise HTTPException(status_code=500, detail="Error creating report")

@app.get("/reports/{report_id}", response_model=dict)
def get_report_by_id(report_id: str):
    report = db.get_report_by_id(report_id)
    if report:
        return report
    raise HTTPException(status_code=404, detail="Report not found")

@app.put("/reports/{report_id}", response_model=str)
def update_report(report_id: str, description: Optional[str] = None, report_type: Optional[str] = None):
    updated_id = db.update_report(report_id, description, report_type)
    if updated_id:
        return {"id": updated_id}
    raise HTTPException(status_code=500, detail="Error updating report")

@app.delete("/reports/{report_id}")
def delete_report(report_id: str):
    db.delete_report(report_id)
    return {"detail": "Report deleted"}

@app.post("/emergency-reports/", response_model=str)
def create_emergency_report(emergency_report: EmergencyReport):
    emergency_id = db.create_emergency_report(
        emergency_report.reporter_first_name,
        emergency_report.reporter_last_name,
        emergency_report.license_plate,
        emergency_report.severity_level,
        emergency_report.description,
        emergency_report.ratings,
        emergency_report.organization_id
    )
    if emergency_id:
        return {"id": emergency_id}
    raise HTTPException(status_code=500, detail="Error creating emergency report")

@app.get("/emergency-reports/{emergency_id}", response_model=dict)
def get_emergency_report_by_id(emergency_id: str):
    emergency_report = db.get_emergency_report_by_id(emergency_id)
    if emergency_report:
        return emergency_report
    raise HTTPException(status_code=404, detail="Emergency report not found")

@app.put("/emergency-reports/{emergency_id}", response_model=str)
def update_emergency_report(emergency_id: str, status: Optional[str] = None, resolved_at: Optional[str] = None):
    updated_id = db.update_emergency_report(emergency_id, status, resolved_at)
    if updated_id:
        return {"id": updated_id}
    raise HTTPException(status_code=500, detail="Error updating emergency report")

@app.delete("/emergency-reports/{emergency_id}")
def delete_emergency_report(emergency_id: str):
    db.delete_emergency_report(emergency_id)
    return {"detail": "Emergency report deleted"}

@app.post("/rides/", response_model=str)
def create_ride(ride: Ride):
    ride_id = db.create_ride(
        ride.pickup_location,
        ride.dropoff_location,
        ride.ride_date,
        ride.ride_time,
        ride.number_of_passengers,
        ride.vehicle_type,
        ride.license_plate,
        ride.organization_id,
        ride.is_completed,
        ride.is_in_progress
    )
    if ride_id:
        return {"id": ride_id}
    raise HTTPException(status_code=500, detail="Error creating ride")

@app.get("/rides/{ride_id}", response_model=dict)
def get_ride_by_id(ride_id: str):
    ride = db.get_ride_by_id(ride_id)
    if ride:
        return ride
    raise HTTPException(status_code=404, detail="Ride not found")

@app.put("/rides/{ride_id}", response_model=str)
def update_ride(ride_id: str, is_completed: Optional[bool] = None, is_in_progress: Optional[bool] = None, completed_at: Optional[str] = None):
    updated_id = db.update_ride(ride_id, is_completed, is_in_progress, completed_at)
    if updated_id:
        return {"id": updated_id}
    raise HTTPException(status_code=500, detail="Error updating ride")

@app.delete("/rides/{ride_id}")
def delete_ride(ride_id: str):
    db.delete_ride(ride_id)
    return {"detail": "Ride deleted"}

@app.post("/hails/", response_model=str)
def create_hail(hail: Hail):
    hail_id = db.create_hail(hail.driver_license, hail.latitude, hail.longitude)
    if hail_id:
        return {"id": hail_id}
    raise HTTPException(status_code=500, detail="Error creating hail")

@app.get("/hails/{hail_id}", response_model=dict)
def get_hail_by_id(hail_id: str):
    hail = db.get_hail_by_id(hail_id)
    if hail:
        return hail
    raise HTTPException(status_code=404, detail="Hail not found")

@app.put("/hails/{hail_id}", response_model=str)
def update_hail(hail_id: str, latitude: Optional[float] = None, longitude: Optional[float] = None):
    updated_id = db.update_hail(hail_id, latitude, longitude)
    if updated_id:
        return {"id": updated_id}
    raise HTTPException(status_code=500, detail="Error updating hail")

@app.delete("/hails/{hail_id}")
def delete_hail(hail_id: str):
    db.delete_hail(hail_id)
    return {"detail": "Hail deleted"}

@app.post("/payments/", response_model=str)
def create_payment(payment: Payment):
    payment_id = db.create_payment(
        payment.customer_id,
        payment.driver_id,
        payment.amount,
        payment.pickup_location,
        payment.dropoff_location,
        payment.latitude,
        payment.longitude
    )
    if payment_id:
        return {"id": payment_id}
    raise HTTPException(status_code=500, detail="Error creating payment")

@app.get("/payments/{payment_id}", response_model=dict)
def get_payment_by_id(payment_id: str):
    payment = db.get_payment_by_id(payment_id)
    if payment:
        return payment
    raise HTTPException(status_code=404, detail="Payment not found")

@app.put("/payments/{payment_id}")
def update_payment(payment_id: int, update: PaymentUpdate):
    try:
        # Replace with actual database call
        updated_payment_id = db.update_payment(payment_id, update.amount, update.pickup_location, update.dropoff_location)
        return {"payment_id": updated_payment_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.delete("/payments/{payment_id}")
def delete_payment(payment_id: int):
    try:
        db.delete_payment(payment_id)
        return {"message": "Payment deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.get("/reports/{organization_id}")
def list_reports_by_organization(organization_id: int):
    try:
        reports = db.list_reports_by_organization(organization_id)
        return {"reports": reports}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.get("/drivers/{organization_id}")
def list_drivers_by_organization(organization_id: int):
    try:
        drivers = db.list_drivers_by_organization(organization_id)
        return {"drivers": drivers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.get("/all_info")
def list_all_info():
    try:
        all_info = db.list_all_organizations_drivers_vehicles_locations()
        return {"info": all_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.get("/rides")
def list_rides_by_user_driver_organization(
    user_id: Optional[int] = None,
    driver_id: Optional[int] = None,
    organization_id: Optional[int] = None
):
    try:
        rides = db.list_rides_by_user_driver_organization(user_id, driver_id, organization_id)
        return {"rides": rides}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.get("/available_rides")
def list_available_rides():
    try:
        rides = db.list_available_rides()
        return {"rides": rides}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.get("/dispatched_rides")
def list_dispatched_rides():
    try:
        rides = db.list_dispatched_rides()
        return {"rides": rides}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.get("/hail")
def hail_by_customer_driver_organization(
    customer_id: Optional[int] = None,
    driver_id: Optional[int] = None,
    organization_id: Optional[int] = None
):
    try:
        hails = db.hail_by_customer_driver_organization(customer_id, driver_id, organization_id)
        return {"hails": hails}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.get("/payment_history")
def list_payment_history():
    try:
        payments = db.list_payment_history()
        return {"payments": payments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.get("/locations")
def get_location_by_driver_id_or_license(
    driver_id: Optional[int] = None,
    license_number: Optional[str] = None
):
    try:
        locations = db.get_location_by_driver_id_or_license(driver_id, license_number)
        return {"locations": locations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.get("/vehicle_status")
def get_vehicle_status(
    vehicle_id: Optional[int] = None,
    license_plate: Optional[str] = None
):
    try:
        vehicles = db.get_vehicle_status(vehicle_id, license_plate)
        return {"vehicles": vehicles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.get("/driver_details")
def get_driver_details(
    driver_id: Optional[int] = None,
    license_number: Optional[str] = None
):
    try:
        drivers = db.get_driver_details(driver_id, license_number)
        return {"drivers": drivers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.get("/organizations/{organization_id}")
def get_organization_details(organization_id: int):
    try:
        organization = db.get_organization_details(organization_id)
        return {"organization": organization}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.get("/active_rides/{organization_id}")
def get_active_rides_by_organization(organization_id: int):
    try:
        rides = db.get_active_rides_by_organization(organization_id)
        return {"rides": rides}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.post("/log_speed/")
def log_vehicle_speed(speed_log: SpeedLog):
    try:
        db.log_speed(speed_log.license_plate, speed_log.speed)
        return {"message": "Speed logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vehicle_speeds/{license_plate}")
def get_vehicle_speeds(license_plate: str):
    speeds = db.get_vehicle_speeds(license_plate)
    if speeds is None:
        raise HTTPException(status_code=404, detail="Vehicle not found or no speed data available")
    return {
        "id": speeds[0][0],
        "license_plate": speeds[0][1],
        "speed": speeds[0][2],
        "recorded_at": speeds[0][3]
    }