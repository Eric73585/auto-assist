-- AutoAssist Database Setup for Supabase
-- Run this SQL in your Supabase SQL Editor

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
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

-- Insert sample car companies data
INSERT INTO car_companies (id, name, logo_url, description) VALUES
('1', 'Maruti Suzuki', 'https://images.unsplash.com/photo-1622788596263-991b12a09eaf?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85', 'India''s leading automotive manufacturer offering reliable automatic vehicles'),
('2', 'Toyota', 'https://images.unsplash.com/photo-1622788596263-991b12a09eaf?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85', 'Global leader in hybrid and automatic transmission technology'),
('3', 'Honda', 'https://images.unsplash.com/photo-1622788596263-991b12a09eaf?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85', 'Innovative Japanese brand known for efficient automatic transmissions'),
('4', 'Hyundai', 'https://images.unsplash.com/photo-1622788596263-991b12a09eaf?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85', 'Korean automotive excellence with advanced automatic features'),
('5', 'Tata Motors', 'https://images.unsplash.com/photo-1622788596263-991b12a09eaf?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85', 'India''s homegrown automotive giant with modern automatic vehicles')
ON CONFLICT (id) DO NOTHING;

-- Insert sample FAQ data
INSERT INTO faqs (id, question, answer, category) VALUES
('1', 'Can I use D mode always?', 'Yes, you can drive in D (Drive) mode for most city and highway driving. It automatically shifts gears as needed.', 'general'),
('2', 'What if I press brake and accelerator together?', 'Never press both pedals simultaneously. This can damage the transmission. The brake will override the accelerator in most modern cars.', 'safety'),
('3', 'How to park on a slope?', 'Use P (Park) mode and engage the handbrake. For steep slopes, turn wheels away from traffic before parking.', 'parking'),
('4', 'When should I use L (Low) gear?', 'Use L gear when going down steep hills or for engine braking. It provides better control and reduces brake wear.', 'gears'),
('5', 'Is it safe to shift from D to R while moving?', 'Never shift from Drive to Reverse while the car is moving. Always come to a complete stop before changing gears.', 'safety'),
('6', 'What is the difference between CVT and AMT?', 'CVT (Continuously Variable Transmission) provides smoother acceleration, while AMT (Automated Manual Transmission) is more fuel-efficient but has slight jerks during gear changes.', 'technical'),
('7', 'How often should I service my automatic car?', 'Service your automatic car every 6 months or 10,000 km, whichever comes first. Regular maintenance ensures smooth transmission operation.', 'maintenance'),
('8', 'Can I tow another vehicle with my automatic car?', 'Most automatic cars can tow light loads, but check your owner''s manual for specific towing capacity and guidelines to avoid transmission damage.', 'general')
ON CONFLICT (id) DO NOTHING;

-- Insert sample car models (for Maruti Suzuki)
INSERT INTO car_models (id, name, company_id, image_url, year_range, price_range, transmission_type, features) VALUES
('maruti_swift_amt', 'Swift AMT', '1', 'https://images.unsplash.com/photo-1637913072630-c863eaa8a271?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwzfHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85', '2020-2024', '₹6-8 lakhs', 'AMT', '["Auto Gear Shift", "Hill Hold Assist", "ESP", "Dual Airbags"]'),
('maruti_baleno_cvt', 'Baleno CVT', '1', 'https://images.unsplash.com/photo-1534675206212-b6bc629ca261?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwyfHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85', '2019-2024', '₹7-10 lakhs', 'CVT', '["CVT Transmission", "SmartPlay Infotainment", "LED Headlamps", "Cruise Control"]'),
('maruti_dzire_amt', 'Dzire AMT', '1', 'https://images.unsplash.com/photo-1606128031531-52ae98c9707a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85', '2020-2024', '₹7-9 lakhs', 'AMT', '["AMT Technology", "Touchscreen Infotainment", "Reverse Camera", "ABS with EBD"]')
ON CONFLICT (id) DO NOTHING;

-- Insert sample car models (for Toyota)
INSERT INTO car_models (id, name, company_id, image_url, year_range, price_range, transmission_type, features) VALUES
('toyota_innova_crysta_at', 'Innova Crysta AT', '2', 'https://images.unsplash.com/photo-1606128031531-52ae98c9707a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85', '2018-2024', '₹18-25 lakhs', 'Torque Converter AT', '["6-Speed Automatic", "7-Seater", "Diesel Engine", "Premium Interior"]'),
('toyota_camry_hybrid', 'Camry Hybrid', '2', 'https://images.unsplash.com/photo-1637913072630-c863eaa8a271?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwzfHxhdXRvbWF0aWMlMjBjYXI%7C0%7C%7C%7C1754376190%7C0&ixlib=rb-4.1.0&q=85', '2019-2024', '₹40-45 lakhs', 'Hybrid CVT', '["Hybrid Technology", "CVT Transmission", "Premium Features", "Advanced Safety"]')
ON CONFLICT (id) DO NOTHING;

-- Insert sample components for cars
INSERT INTO components (id, name, description, usage_instructions, when_to_use, image_url, car_model_id) VALUES
('gear_selector_prndl', 'Gear Selector (PRNDL)', 'The gear selector allows you to choose different driving modes', 'P - Park (for parking), R - Reverse, N - Neutral, D - Drive, L - Low gear', 'Use P when parked, R for backing up, D for normal driving, L for hills', 'https://images.unsplash.com/photo-1606128031531-52ae98c9707a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85', 'maruti_swift_amt'),
('abs_braking_system', 'Automatic Braking System (ABS)', 'Prevents wheel lockup during emergency braking', 'Press brake pedal firmly in emergency. System automatically prevents skidding', 'Activated automatically during hard braking situations', 'https://images.unsplash.com/photo-1533630217389-3a5e4dff5683?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwxfHxjYXIlMjBkYXNoYm9hcmR8ZW58MHx8fHwxNzU0Mzc2MTk3fDA&ixlib=rb-4.1.0&q=85', 'maruti_swift_amt'),
('infotainment_system', 'Infotainment System', 'Central control for entertainment, navigation, and vehicle settings', 'Touch screen interface for music, maps, and car settings', 'Use while parked or let passenger operate while driving', 'https://images.unsplash.com/photo-1615153633779-5c932c7f4cad?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHw0fHxjYXIlMjBkYXNoYm9hcmR8ZW58MHx8fHwxNzU0Mzc2MTk3fDA&ixlib=rb-4.1.0&q=85', 'maruti_swift_amt'),
('cruise_control', 'Cruise Control', 'Maintains constant speed without keeping foot on accelerator', 'Set desired speed, press cruise control button to activate', 'Use on highways for comfortable long-distance driving', 'https://images.unsplash.com/photo-1585014165903-6d6c6ebad3e9?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwyfHxjYXIlMjBkYXNoYm9hcmR8ZW58MHx8fHwxNzU0Mzc2MTk3fDA&ixlib=rb-4.1.0&q=85', 'maruti_baleno_cvt'),
('keyless_entry', 'Keyless Entry & Start-Stop', 'Push button start with proximity key detection', 'Keep key fob in pocket, press brake and push start button', 'Use for convenient keyless operation of vehicle', 'https://images.unsplash.com/photo-1597386601945-8980df52c3dc?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwzfHxjYXIlMjBkYXNoYm9hcmR8ZW58MHx8fHwxNzU0Mzc2MTk3fDA&ixlib=rb-4.1.0&q=85', 'maruti_baleno_cvt')
ON CONFLICT (id) DO NOTHING;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_car_models_company_id ON car_models(company_id);
CREATE INDEX IF NOT EXISTS idx_components_car_model_id ON components(car_model_id);
CREATE INDEX IF NOT EXISTS idx_faqs_category ON faqs(category);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Enable Row Level Security (RLS) - Optional but recommended
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE car_companies ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE car_models ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE components ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE faqs ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (adjust as needed for your security requirements)
-- CREATE POLICY "Public read access for car_companies" ON car_companies FOR SELECT USING (true);
-- CREATE POLICY "Public read access for car_models" ON car_models FOR SELECT USING (true);
-- CREATE POLICY "Public read access for components" ON components FOR SELECT USING (true);
-- CREATE POLICY "Public read access for faqs" ON faqs FOR SELECT USING (true);

-- Grant necessary permissions
-- GRANT SELECT ON car_companies TO anon, authenticated;
-- GRANT SELECT ON car_models TO anon, authenticated;
-- GRANT SELECT ON components TO anon, authenticated;
-- GRANT SELECT ON faqs TO anon, authenticated;
-- GRANT INSERT, SELECT ON users TO anon, authenticated;

COMMIT;