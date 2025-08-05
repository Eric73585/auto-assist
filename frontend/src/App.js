import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Badge } from './components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from './components/ui/accordion';
import { Car, Settings, HelpCircle, Shield, Phone, BookOpen, Zap } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [currentView, setCurrentView] = useState('login');
  const [user, setUser] = useState(null);
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [cars, setCars] = useState([]);
  const [selectedCar, setSelectedCar] = useState(null);
  const [components, setComponents] = useState([]);
  const [faqs, setFaqs] = useState([]);
  const [drivingGuide, setDrivingGuide] = useState(null);
  const [insuranceInfo, setInsuranceInfo] = useState(null);
  const [contactInfo, setContactInfo] = useState(null);
  const [loginData, setLoginData] = useState({ username: '', password: '' });
  const [registerData, setRegisterData] = useState({ username: '', password: '' });

  useEffect(() => {
    fetchCompanies();
    fetchFAQs();
    fetchDrivingGuide();
    fetchInsuranceInfo();
    fetchContactInfo();
  }, []);

  const fetchCompanies = async () => {
    try {
      const response = await axios.get(`${API}/companies`);
      setCompanies(response.data);
    } catch (error) {
      console.error('Error fetching companies:', error);
    }
  };

  const fetchFAQs = async () => {
    try {
      const response = await axios.get(`${API}/faqs`);
      setFaqs(response.data);
    } catch (error) {
      console.error('Error fetching FAQs:', error);
    }
  };

  const fetchDrivingGuide = async () => {
    try {
      const response = await axios.get(`${API}/driving-guide`);
      setDrivingGuide(response.data);
    } catch (error) {
      console.error('Error fetching driving guide:', error);
    }
  };

  const fetchInsuranceInfo = async () => {
    try {
      const response = await axios.get(`${API}/insurance-policy`);
      setInsuranceInfo(response.data);
    } catch (error) {
      console.error('Error fetching insurance info:', error);
    }
  };

  const fetchContactInfo = async () => {
    try {
      const response = await axios.get(`${API}/contact`);
      setContactInfo(response.data);
    } catch (error) {
      console.error('Error fetching contact info:', error);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API}/login`, loginData);
      setUser(response.data.user);
      setCurrentView('companies');
    } catch (error) {
      alert('Invalid credentials');
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/register`, registerData);
      alert('Registration successful! Please login.');
      setCurrentView('login');
    } catch (error) {
      alert('Registration failed');
    }
  };

  const handleCompanySelect = async (company) => {
    setSelectedCompany(company);
    try {
      const response = await axios.get(`${API}/companies/${company.id}/cars`);
      setCars(response.data);
      setCurrentView('cars');
    } catch (error) {
      console.error('Error fetching cars:', error);
    }
  };

  const handleCarSelect = async (car) => {
    setSelectedCar(car);
    try {
      const response = await axios.get(`${API}/cars/${car.id}/components`);
      setComponents(response.data);
      setCurrentView('features');
    } catch (error) {
      console.error('Error fetching components:', error);
    }
  };

  if (currentView === 'login') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl border border-white/20 p-8 shadow-2xl">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl mb-4">
                <Car className="w-8 h-8 text-white" />
              </div>
              <h1 className="text-3xl font-bold text-white mb-2">AutoAssist</h1>
              <p className="text-gray-300">Your Guide to Automatic Cars</p>
            </div>

            <Tabs defaultValue="login" className="w-full">
              <TabsList className="grid w-full grid-cols-2 mb-6">
                <TabsTrigger value="login">Login</TabsTrigger>
                <TabsTrigger value="register">Register</TabsTrigger>
              </TabsList>
              
              <TabsContent value="login">
                <form onSubmit={handleLogin} className="space-y-4">
                  <Input
                    type="text"
                    placeholder="Username"
                    value={loginData.username}
                    onChange={(e) => setLoginData({...loginData, username: e.target.value})}
                    className="bg-white/10 border-white/20 text-white placeholder-gray-400"
                    required
                  />
                  <Input
                    type="password"
                    placeholder="Password"
                    value={loginData.password}
                    onChange={(e) => setLoginData({...loginData, password: e.target.value})}
                    className="bg-white/10 border-white/20 text-white placeholder-gray-400"
                    required
                  />
                  <Button type="submit" className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
                    Login
                  </Button>
                </form>
              </TabsContent>
              
              <TabsContent value="register">
                <form onSubmit={handleRegister} className="space-y-4">
                  <Input
                    type="text"
                    placeholder="Username"
                    value={registerData.username}
                    onChange={(e) => setRegisterData({...registerData, username: e.target.value})}
                    className="bg-white/10 border-white/20 text-white placeholder-gray-400"
                    required
                  />
                  <Input
                    type="password"
                    placeholder="Password"
                    value={registerData.password}
                    onChange={(e) => setRegisterData({...registerData, password: e.target.value})}
                    className="bg-white/10 border-white/20 text-white placeholder-gray-400"
                    required
                  />
                  <Button type="submit" className="w-full bg-gradient-to-r from-green-500 to-blue-600 hover:from-green-600 hover:to-blue-700">
                    Register
                  </Button>
                </form>
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </div>
    );
  }

  if (currentView === 'companies') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <header className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Car className="w-8 h-8 text-blue-600" />
                <h1 className="text-2xl font-bold text-gray-900">AutoAssist</h1>
              </div>
              <div className="text-gray-600">Welcome, {user?.username}</div>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Choose Your Car Brand</h2>
            <p className="text-xl text-gray-600">Select a car company to explore their automatic vehicles</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {companies.map((company) => (
              <Card key={company.id} className="group hover:shadow-xl transition-all duration-300 cursor-pointer border-0 bg-white/60 backdrop-blur-sm" onClick={() => handleCompanySelect(company)}>
                <CardHeader className="text-center">
                  <div className="w-20 h-20 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <Car className="w-10 h-10 text-blue-600" />
                  </div>
                  <CardTitle className="text-2xl font-bold text-gray-900">{company.name}</CardTitle>
                  <CardDescription className="text-gray-600">{company.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
                    Explore Models
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </main>
      </div>
    );
  }

  if (currentView === 'cars') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <header className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Button variant="outline" onClick={() => setCurrentView('companies')}>← Back</Button>
                <h1 className="text-2xl font-bold text-gray-900">{selectedCompany?.name} Models</h1>
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 py-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {cars.map((car) => (
              <Card key={car.id} className="group hover:shadow-xl transition-all duration-300 cursor-pointer" onClick={() => handleCarSelect(car)}>
                <CardHeader>
                  <img src={car.image_url} alt={car.name} className="w-full h-48 object-cover rounded-lg mb-4" />
                  <CardTitle className="text-xl font-bold">{car.name}</CardTitle>
                  <CardDescription>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>Year:</span>
                        <Badge variant="secondary">{car.year_range}</Badge>
                      </div>
                      <div className="flex justify-between">
                        <span>Price:</span>
                        <Badge variant="secondary">{car.price_range}</Badge>
                      </div>
                      <div className="flex justify-between">
                        <span>Type:</span>
                        <Badge variant="secondary">{car.transmission_type}</Badge>
                      </div>
                    </div>
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="mb-4">
                    <h4 className="font-semibold mb-2">Key Features:</h4>
                    <div className="flex flex-wrap gap-1">
                      {car.features.map((feature, index) => (
                        <Badge key={index} variant="outline" className="text-xs">{feature}</Badge>
                      ))}
                    </div>
                  </div>
                  <Button className="w-full">Select This Car</Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </main>
      </div>
    );
  }

  if (currentView === 'features') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <header className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Button variant="outline" onClick={() => setCurrentView('cars')}>← Back to Cars</Button>
                <h1 className="text-2xl font-bold text-gray-900">{selectedCar?.name} Features</h1>
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 py-8">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 mb-8">
            <Card className="group hover:shadow-xl transition-all duration-300 cursor-pointer" onClick={() => setCurrentView('components')}>
              <CardContent className="p-6 text-center">
                <Settings className="w-12 h-12 mx-auto mb-4 text-blue-600 group-hover:scale-110 transition-transform" />
                <h3 className="font-semibold">Component Guide</h3>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-xl transition-all duration-300 cursor-pointer" onClick={() => setCurrentView('driving')}>
              <CardContent className="p-6 text-center">
                <BookOpen className="w-12 h-12 mx-auto mb-4 text-green-600 group-hover:scale-110 transition-transform" />
                <h3 className="font-semibold">How to Drive</h3>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-xl transition-all duration-300 cursor-pointer" onClick={() => setCurrentView('gear-guide')}>
              <CardContent className="p-6 text-center">
                <Zap className="w-12 h-12 mx-auto mb-4 text-purple-600 group-hover:scale-110 transition-transform" />
                <h3 className="font-semibold">Gear Selector</h3>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-xl transition-all duration-300 cursor-pointer" onClick={() => setCurrentView('faq')}>
              <CardContent className="p-6 text-center">
                <HelpCircle className="w-12 h-12 mx-auto mb-4 text-orange-600 group-hover:scale-110 transition-transform" />
                <h3 className="font-semibold">FAQ</h3>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-xl transition-all duration-300 cursor-pointer" onClick={() => setCurrentView('insurance')}>
              <CardContent className="p-6 text-center">
                <Shield className="w-12 h-12 mx-auto mb-4 text-red-600 group-hover:scale-110 transition-transform" />
                <h3 className="font-semibold">Insurance & Policy</h3>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-xl transition-all duration-300 cursor-pointer" onClick={() => setCurrentView('contact')}>
              <CardContent className="p-6 text-center">
                <Phone className="w-12 h-12 mx-auto mb-4 text-teal-600 group-hover:scale-110 transition-transform" />
                <h3 className="font-semibold">Contact Us</h3>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    );
  }

  if (currentView === 'components') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <header className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center space-x-3">
              <Button variant="outline" onClick={() => setCurrentView('features')}>← Back to Features</Button>
              <h1 className="text-2xl font-bold text-gray-900">Component Guide</h1>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {components.map((component) => (
              <Card key={component.id} className="overflow-hidden">
                <CardHeader>
                  <img src={component.image_url} alt={component.name} className="w-full h-48 object-cover rounded-lg mb-4" />
                  <CardTitle className="text-xl font-bold">{component.name}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">What is it?</h4>
                    <p className="text-gray-600">{component.description}</p>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">How to use it?</h4>
                    <p className="text-gray-600">{component.usage_instructions}</p>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">When to use it?</h4>
                    <p className="text-gray-600">{component.when_to_use}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </main>
      </div>
    );
  }

  if (currentView === 'driving' && drivingGuide) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <header className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center space-x-3">
              <Button variant="outline" onClick={() => setCurrentView('features')}>← Back to Features</Button>
              <h1 className="text-2xl font-bold text-gray-900">{drivingGuide.title}</h1>
            </div>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-4 py-8">
          <div className="space-y-6">
            {drivingGuide.steps.map((step) => (
              <Card key={step.step} className="p-6">
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 font-bold">{step.step}</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 mb-2">{step.title}</h3>
                    <p className="text-gray-600">{step.description}</p>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </main>
      </div>
    );
  }

  if (currentView === 'gear-guide') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <header className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center space-x-3">
              <Button variant="outline" onClick={() => setCurrentView('features')}>← Back to Features</Button>
              <h1 className="text-2xl font-bold text-gray-900">Gear Selector Guide</h1>
            </div>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-4 py-8">
          <Card className="p-6 mb-8">
            <img src="https://images.unsplash.com/photo-1606128031531-52ae98c9707a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxhdXRvbWF0aWMlMjBjYXJ8ZW58MHx8fHwxNzU0Mzc2MTkwfDA&ixlib=rb-4.1.0&q=85" alt="Gear Selector" className="w-full h-64 object-cover rounded-lg mb-6" />
            <h2 className="text-2xl font-bold mb-4">Understanding Automatic Gear Selector</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="p-4 bg-red-50 rounded-lg">
                  <h3 className="font-bold text-red-800 mb-2">P - Park</h3>
                  <p className="text-red-700">Use when parking or stopping for extended periods. Locks transmission.</p>
                </div>
                <div className="p-4 bg-orange-50 rounded-lg">
                  <h3 className="font-bold text-orange-800 mb-2">R - Reverse</h3>
                  <p className="text-orange-700">For backing up. Only use when completely stopped.</p>
                </div>
              </div>
              <div className="space-y-4">
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h3 className="font-bold text-gray-800 mb-2">N - Neutral</h3>
                  <p className="text-gray-700">Engine runs but transmission is disconnected. Rarely used.</p>
                </div>
                <div className="p-4 bg-green-50 rounded-lg">
                  <h3 className="font-bold text-green-800 mb-2">D - Drive</h3>
                  <p className="text-green-700">Normal driving mode. Use for most city and highway driving.</p>
                </div>
              </div>
            </div>
          </Card>
        </main>
      </div>
    );
  }

  if (currentView === 'faq') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <header className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center space-x-3">
              <Button variant="outline" onClick={() => setCurrentView('features')}>← Back to Features</Button>
              <h1 className="text-2xl font-bold text-gray-900">Frequently Asked Questions</h1>
            </div>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-4 py-8">
          <Accordion type="single" collapsible className="w-full space-y-4">
            {faqs.map((faq) => (
              <AccordionItem key={faq.id} value={faq.id} className="bg-white rounded-lg border">
                <AccordionTrigger className="px-6 py-4 text-left hover:no-underline">
                  <div className="flex items-center space-x-3">
                    <Badge variant="outline">{faq.category}</Badge>
                    <span className="font-semibold">{faq.question}</span>
                  </div>
                </AccordionTrigger>
                <AccordionContent className="px-6 pb-4 text-gray-600">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </main>
      </div>
    );
  }

  if (currentView === 'insurance' && insuranceInfo) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <header className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center space-x-3">
              <Button variant="outline" onClick={() => setCurrentView('features')}>← Back to Features</Button>
              <h1 className="text-2xl font-bold text-gray-900">{insuranceInfo.title}</h1>
            </div>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-4 py-8">
          <div className="space-y-6">
            {insuranceInfo.sections.map((section, index) => (
              <Card key={index} className="p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-3">{section.title}</h3>
                <p className="text-gray-600">{section.content}</p>
              </Card>
            ))}
            
            <Card className="p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-3">Required Documents</h3>
              <div className="grid grid-cols-2 gap-4">
                {insuranceInfo.important_documents.map((doc, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <Badge variant="outline">{index + 1}</Badge>
                    <span>{doc}</span>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </main>
      </div>
    );
  }

  if (currentView === 'contact' && contactInfo) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <header className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center space-x-3">
              <Button variant="outline" onClick={() => setCurrentView('features')}>← Back to Features</Button>
              <h1 className="text-2xl font-bold text-gray-900">Contact Information</h1>
            </div>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-4 py-8">
          <Card className="p-8 text-center">
            <div className="w-20 h-20 bg-blue-100 rounded-full mx-auto mb-6 flex items-center justify-center">
              <Phone className="w-10 h-10 text-blue-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">{contactInfo.server_name}</h2>
            <div className="space-y-4 text-gray-600">
              <div>
                <h3 className="font-semibold">Phone Number</h3>
                <p>{contactInfo.contact_number}</p>
              </div>
              <div>
                <h3 className="font-semibold">Email</h3>
                <p>{contactInfo.email}</p>
              </div>
              <div>
                <h3 className="font-semibold">Address</h3>
                <p>{contactInfo.address}</p>
              </div>
            </div>
          </Card>
        </main>
      </div>
    );
  }

  return <div>Loading...</div>;
}

export default App;