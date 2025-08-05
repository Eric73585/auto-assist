import httpx
import asyncio
import json

SUPABASE_URL = "https://cdxnjrlgacibjawenkvo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNkeG5qcmxnYWNpYmphd2Vua3ZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQzNzUyMDgsImV4cCI6MjA2OTk1MTIwOH0.viTSdKm8HGdGJOFemEqtIONRQ_CQ676GAKkczKQ5Fxg"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# SQL to create tables
create_tables_sql = """
-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create car_companies table  
CREATE TABLE IF NOT EXISTS car_companies (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    logo_url VARCHAR,
    description TEXT
);

-- Create car_models table
CREATE TABLE IF NOT EXISTS car_models (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    company_id VARCHAR REFERENCES car_companies(id),
    image_url VARCHAR,
    year_range VARCHAR,
    price_range VARCHAR,
    transmission_type VARCHAR,
    features JSONB
);

-- Create components table
CREATE TABLE IF NOT EXISTS components (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    usage_instructions TEXT,
    when_to_use TEXT,
    image_url VARCHAR,
    car_model_id VARCHAR REFERENCES car_models(id)
);

-- Create faqs table
CREATE TABLE IF NOT EXISTS faqs (
    id VARCHAR PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR NOT NULL
);
"""

async def setup_tables():
    async with httpx.AsyncClient() as client:
        try:
            # Execute the SQL to create tables
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
                headers=headers,
                json={"sql": create_tables_sql}
            )
            
            if response.status_code in [200, 201]:
                print("✅ Tables created successfully!")
            else:
                print(f"❌ Error creating tables: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(setup_tables())