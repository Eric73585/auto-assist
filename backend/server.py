from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import httpx
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Supabase configuration
SUPABASE_URL = "https://cdxnjrlgacibjawenkvo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNkeG5qcmxnYWNpYmphd2Vua3ZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQzNzUyMDgsImV4cCI6MjA2OTk1MTIwOH0.viTSdKm8HGdGJOFemEqtIONRQ_CQ676GAKkczKQ5Fxg"

# Create the main app
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()

# Pydantic Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str

class CarCompany(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    logo_url: str
    description: str

class CarModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    company_id: str
    image_url: str
    year_range: str
    price_range: str
    transmission_type: str
    features: List[str]

class Component(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    usage_instructions: str
    when_to_use: str
    image_url: str
    car_model_id: str

class FAQ(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str
    answer: str
    category: str

class ContactInfo(BaseModel):
    server_name: str = "AutoAssist Support Team"
    contact_number: str = "+91-9876543210"
    email: str = "support@autoassist.com"
    address: str = "123 Tech Park, Bangalore, Karnataka 560001, India"

# Supabase client helper
class SupabaseClient:
    def __init__(self):
        self.url = SUPABASE_URL
        self.key = SUPABASE_KEY
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }
    
    async def insert(self, table: str, data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.url}/rest/v1/{table}",
                headers=self.headers,
                json=data
            )
            if response.status_code not in [200, 201]:
                raise HTTPException(status_code=400, detail=f"Database error: {response.text}")
            return response.json()
    
    async def select(self, table: str, filters: str = ""):
        async with httpx.AsyncClient() as client:
            url = f"{self.url}/rest/v1/{table}"
            if filters:
                url += f"?{filters}"
            response = await client.get(url, headers=self.headers)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail=f"Database error: {response.text}")
            return response.json()

supabase = SupabaseClient()

# Static data for now (since Supabase tables need to be created)
STATIC_COMPANIES = [
    {
        "id": "1",
        "name": "Maruti Suzuki",
        "logo_url": "https://images.unsplash.com/photo-1622788596263-991b12a09eaf?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85",
        "description": "India's leading automotive manufacturer offering reliable automatic vehicles"
    },
    {
        "id": "2",
        "name": "Toyota",
        "logo_url": "https://images.unsplash.com/photo-1622788596263-991b12a09eaf?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85",
        "description": "Global leader in hybrid and automatic transmission technology"
    },
    {
        "id": "3",
        "name": "Honda",
        "logo_url": "https://images.unsplash.com/photo-1622788596263-991b12a09eaf?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85",
        "description": "Innovative Japanese brand known for efficient automatic transmissions"
    },
    {
        "id": "4",
        "name": "Hyundai",
        "logo_url": "https://images.unsplash.com/photo-1622788596263-991b12a09eaf?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85",
        "description": "Korean automotive excellence with advanced automatic features"
    },
    {
        "id": "5",
        "name": "Tata Motors",
        "logo_url": "https://images.unsplash.com/photo-1622788596263-991b12a09eaf?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85",
        "description": "India's homegrown automotive giant with modern automatic vehicles"
    }
]

STATIC_FAQS = [
    {
        "id": "1",
        "question": "Can I use D mode always?",
        "answer": "Yes, you can drive in D (Drive) mode for most city and highway driving. It automatically shifts gears as needed.",
        "category": "general"
    },
    {
        "id": "2",
        "question": "What if I press brake and accelerator together?",
        "answer": "Never press both pedals simultaneously. This can damage the transmission. The brake will override the accelerator in most modern cars.",
        "category": "safety"
    },
    {
        "id": "3",
        "question": "How to park on a slope?",
        "answer": "Use P (Park) mode and engage the handbrake. For steep slopes, turn wheels away from traffic before parking.",
        "category": "parking"
    },
    {
        "id": "4",
        "question": "When should I use L (Low) gear?",
        "answer": "Use L gear when going down steep hills or for engine braking. It provides better control and reduces brake wear.",
        "category": "gears"
    }
]

STATIC_USERS = {}  # Simple in-memory user storage

async def init_sample_data():
    # Using static data for now
    logging.info("Using static data - Supabase tables will be created later")

# Routes
@api_router.get("/")
async def root():
    return {"message": "AutoAssist API - Your Guide to Automatic Cars"}

@api_router.post("/register")
async def register(user: UserCreate):
    # Check if user already exists
    if user.username in STATIC_USERS:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_data = {
        "id": str(uuid.uuid4()),
        "username": user.username,
        "password": user.password,  # In production, hash this password
        "created_at": datetime.utcnow().isoformat()
    }
    STATIC_USERS[user.username] = user_data
    return {"message": "User registered successfully", "user_id": user_data["id"]}

@api_router.post("/login")
async def login(user: UserLogin):
    if user.username not in STATIC_USERS or STATIC_USERS[user.username]["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user": STATIC_USERS[user.username]}

@api_router.get("/companies")
async def get_companies():
    return STATIC_COMPANIES

@api_router.get("/companies/{company_id}/cars")
async def get_cars_by_company(company_id: str):
    # Find company
    company = None
    for comp in STATIC_COMPANIES:
        if comp["id"] == company_id:
            company = comp
            break
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Sample car models for each company
    sample_cars = {
        "1": [  # Maruti
            {
                "id": str(uuid.uuid4()),
                "name": "Swift AMT",
                "image_url": "https://images.unsplash.com/photo-1637913072630-c863eaa8a271?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwzfHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85",
                "year_range": "2020-2024",
                "price_range": "₹6-8 lakhs",
                "transmission_type": "AMT",
                "features": ["Auto Gear Shift", "Hill Hold Assist", "ESP", "Dual Airbags"]
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Baleno CVT",
                "image_url": "https://images.unsplash.com/photo-1534675206212-b6bc629ca261?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwyfHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85",
                "year_range": "2019-2024",
                "price_range": "₹7-10 lakhs",
                "transmission_type": "CVT",
                "features": ["CVT Transmission", "SmartPlay Infotainment", "LED Headlamps", "Cruise Control"]
            }
        ],
        "2": [  # Toyota
            {
                "id": str(uuid.uuid4()),
                "name": "Innova Crysta AT",
                "image_url": "https://images.unsplash.com/photo-1606128031531-52ae98c9707a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85",
                "year_range": "2018-2024",
                "price_range": "₹18-25 lakhs",
                "transmission_type": "Torque Converter AT",
                "features": ["6-Speed Automatic", "7-Seater", "Diesel Engine", "Premium Interior"]
            }
        ],
        "default": [
            {
                "id": str(uuid.uuid4()),
                "name": "Sample Automatic Car",
                "image_url": "https://images.unsplash.com/photo-1606128031531-52ae98c9707a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85",
                "year_range": "2020-2024",
                "price_range": "₹8-12 lakhs",
                "transmission_type": "Automatic",
                "features": ["Automatic Transmission", "Power Steering", "AC", "Safety Features"]
            }
        ]
    }
    
    return sample_cars.get(company_id, sample_cars["default"])

@api_router.get("/cars/{car_id}/components")
async def get_car_components(car_id: str):
    # Sample components for automatic cars
    components = [
        {
            "id": str(uuid.uuid4()),
            "name": "Gear Selector (PRNDL)",
            "description": "The gear selector allows you to choose different driving modes",
            "usage_instructions": "P - Park (for parking), R - Reverse, N - Neutral, D - Drive, L - Low gear",
            "when_to_use": "Use P when parked, R for backing up, D for normal driving, L for hills",
            "image_url": "https://images.unsplash.com/photo-1606128031531-52ae98c9707a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Automatic Braking System (ABS)",
            "description": "Prevents wheel lockup during emergency braking",
            "usage_instructions": "Press brake pedal firmly in emergency. System automatically prevents skidding",
            "when_to_use": "Activated automatically during hard braking situations",
            "image_url": "https://images.unsplash.com/photo-1533630217389-3a5e4dff5683?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwxfHxjYXIlMjBkYXNoYm9hcmR8ZW58MHx8fHwxNzU0Mzc2MTk3fDA&ixlib=rb-4.1.0&q=85"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Infotainment System",
            "description": "Central control for entertainment, navigation, and vehicle settings",
            "usage_instructions": "Touch screen interface for music, maps, and car settings",
            "when_to_use": "Use while parked or let passenger operate while driving",
            "image_url": "https://images.unsplash.com/photo-1615153633779-5c932c7f4cad?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHw0fHxjYXIlMjBkYXNoYm9hcmR8ZW58MHx8fHwxNzU0Mzc2MTk3fDA&ixlib=rb-4.1.0&q=85"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Cruise Control",
            "description": "Maintains constant speed without keeping foot on accelerator",
            "usage_instructions": "Set desired speed, press cruise control button to activate",
            "when_to_use": "Use on highways for comfortable long-distance driving",
            "image_url": "https://images.unsplash.com/photo-1585014165903-6d6c6ebad3e9?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwyfHxjYXIlMjBkYXNoYm9hcmR8ZW58MHx8fHwxNzU0Mzc2MTk3fDA&ixlib=rb-4.1.0&q=85"
        }
    ]
    return components

@api_router.get("/faqs")
async def get_faqs():
    return STATIC_FAQS

@api_router.get("/contact")
async def get_contact_info():
    return ContactInfo()

@api_router.get("/driving-guide")
async def get_driving_guide():
    return {
        "title": "How to Drive an Automatic Car",
        "steps": [
            {
                "step": 1,
                "title": "Getting Started",
                "description": "Adjust seat, mirrors, and steering wheel. Ensure car is in Park (P) mode."
            },
            {
                "step": 2,
                "title": "Starting the Car",
                "description": "Press brake pedal and press start button or turn key. Car should be in Park."
            },
            {
                "step": 3,
                "title": "Moving Forward",
                "description": "Keep foot on brake, shift to Drive (D), release handbrake, slowly release brake pedal."
            },
            {
                "step": 4,
                "title": "Stopping",
                "description": "Gradually press brake pedal. For parking, shift to Park (P) and engage handbrake."
            },
            {
                "step": 5,
                "title": "Safety Tips",
                "description": "Never shift gears while moving. Always stop completely before changing from D to R or vice versa."
            }
        ]
    }

@api_router.get("/insurance-policy")
async def get_insurance_policy_info():
    return {
        "title": "Car Insurance & Government Policies in India",
        "sections": [
            {
                "title": "Mandatory Third-Party Insurance",
                "content": "As per Motor Vehicles Act 1988, third-party insurance is mandatory for all vehicles in India. It covers liability for damage to third-party property and injury."
            },
            {
                "title": "Comprehensive Insurance",
                "content": "Covers own damage, theft, natural disasters, and third-party liability. Recommended for new cars and valuable vehicles."
            },
            {
                "title": "No Claim Bonus (NCB)",
                "content": "Discount on premium for claim-free years. Can range from 20% to 50% based on consecutive claim-free years."
            },
            {
                "title": "GST on Insurance",
                "content": "18% GST is applicable on motor insurance premiums as per current government policy."
            },
            {
                "title": "Recent Policy Changes",
                "content": "New vehicles get 3-year insurance validity, long-term policies available, and cashless settlement improvements."
            }
        ],
        "important_documents": [
            "Registration Certificate (RC)",
            "Valid Insurance Policy",
            "Pollution Under Control (PUC) Certificate",
            "Valid Driving License"
        ]
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    await init_sample_data()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)