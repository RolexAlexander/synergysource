from database import Database
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List

# init fast api app
app = FastAPI()

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
