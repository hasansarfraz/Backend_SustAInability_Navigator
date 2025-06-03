import os
import sys
import json
import shutil
from pathlib import Path

def setup_project_structure():
    """Create the proper project directory structure"""
    
    directories = [
        "app",
        "app/models",
        "app/routes", 
        "app/services",
        "tests",
        "data",
        "logs"
    ]
    
    print("📁 Creating project structure...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   Created: {directory}/")
    
    # Create __init__.py files
    init_files = [
        "app/__init__.py",
        "app/models/__init__.py",
        "app/routes/__init__.py", 
        "app/services/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"   Created: {init_file}")

def validate_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8+ required!")
        print(f"   Current version: {sys.version}")
        return False
    else:
        print(f"✅ Python version OK: {sys.version.split()[0]}")
        return True

def check_dbo_scenarios():
    """Validate DBO scenarios file"""
    print("📊 Checking DBO scenarios file...")
    
    if not os.path.exists("dbo_scenarios.json"):
        print("❌ Error: dbo_scenarios.json not found!")
        print("   Please copy your DBO scenarios file to the project root.")
        return False
    
    try:
        with open("dbo_scenarios.json", "r") as f:
            scenarios = json.load(f)
        
        if not isinstance(scenarios, list) or len(scenarios) == 0:
            print("❌ Error: Invalid scenarios file format!")
            return False
        
        # Validate scenario structure
        required_fields = ["scenario", "description", "recommendations", "estimated_savings"]
        first_scenario = scenarios[0]
        
        missing_fields = [field for field in required_fields if field not in first_scenario]
        if missing_fields:
            print(f"⚠️  Warning: Missing fields in scenarios: {missing_fields}")
            return False
        
        print(f"✅ DBO scenarios validated: {len(scenarios)} scenarios found")
        return True
        
    except Exception as e:
        print(f"❌ Error validating scenarios: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    print("⚙️  Setting up environment file...")
    
    if os.path.exists(".env"):
        print("✅ .env file already exists")
        return True
    
    env_content = """# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Environment Settings
ENVIRONMENT=development

# Optional: SERP API for web search
SERPAPI_KEY=your_serpapi_key_here

# Logging Level
LOG_LEVEL=INFO
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("📝 .env file created")
    print("⚠️  Important: Add your OpenAI API key to .env file!")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("📦 Checking dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "openai", 
        "langchain",
        "requests",
        "python-dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package}")
    
    if missing_packages:
        print(f"\n📋 Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies are installed")
        return True

def create_run_script():
    """Create a simple run script"""
    print("🚀 Creating run script...")
    
    run_script_content = '''#!/usr/bin/env python3
"""
Run script for SustAInability Navigator Backend
"""
import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("🌱 Starting SustAInability Navigator Backend...")
    print("🔗 API Documentation: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/health")
    print("💬 Chat API: http://localhost:8000/api/v1/chat/")
    print()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.environment == "development" else False,
        log_level=settings.log_level.lower()
    )
'''
    
    with open("run.py", "w") as f:
        f.write(run_script_content)
    
    # Make it executable on Unix systems
    if os.name != 'nt':
        os.chmod("run.py", 0o755)
    
    print("✅ Run script created: run.py")

def generate_readme():
    """Generate comprehensive README"""
    print("📚 Generating README...")
    
    readme_content = """# SustAInability Navigator - Professional Backend

## 🌱 Overview
Advanced AI-powered sustainability assistant for Siemens Tech for Sustainability 2025 campaign.
Combines GreenPath AI and SustAIneers solutions into a comprehensive, production-ready backend.

## ✨ Features
- 🤖 **LangChain AI Integration** - Intelligent conversational responses
- 🎭 **Persona-Aware Intelligence** - Tailored responses for different user types
- 📊 **Enhanced DBO Scenarios** - Detailed sustainability decision optimization
- 🔍 **Advanced Search** - Smart scenario discovery and filtering
- 📈 **Analytics & Insights** - Comprehensive sustainability metrics
- 🏢 **Siemens Integration** - Native product mapping and ecosystem alignment

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Setup project structure (if needed)
python setup.py

# Configure environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 2. Run Server
```bash
# Using the run script
python run.py

# Or directly
python main.py
```

### 3. Test System
```bash
python test_comprehensive.py run
```

### 4. Access API
- **Main API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure
```
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables
├── run.py                    # Server run script
├── setup.py                  # Project setup script
├── test_comprehensive.py     # Complete test suite
├── dbo_scenarios.json        # Your DBO scenarios data
├── app/
│   ├── config.py            # Configuration settings
│   ├── models/
│   │   ├── personas.py      # Persona definitions
│   │   ├── chat.py          # Chat data models
│   │   └── dbo.py           # DBO data models
│   ├── routes/
│   │   ├── chat.py          # Chat API endpoints
│   │   ├── dbo.py           # DBO API endpoints
│   │   └── analytics.py     # Analytics endpoints
│   └── services/
│       ├── dbo_service.py   # Enhanced DBO service
│       └── langchain_service.py # LangChain AI service
└── tests/                   # Test files
```

## 🎭 Personas

### Zuri - Enterprise Sustainability Leader
- **Focus**: ESG compliance, global scalability, investor relations
- **Industry**: Technology (10,000+ employees)
- **Priorities**: Strategic sustainability, regulatory compliance

### Amina - Cost-Conscious Business Owner  
- **Focus**: Cost optimization, quick ROI, operational efficiency
- **Industry**: Manufacturing (50-200 employees)
- **Priorities**: Financial returns, resource management

### Björn - Siemens Customer (Finance)
- **Focus**: Technology integration, vendor relationships, proven solutions
- **Industry**: Construction (500+ employees)
- **Priorities**: System compatibility, risk management

### Arjun - Sustainability Champion
- **Focus**: Sustainability impact, competitive advantage, brand positioning
- **Industry**: Retail (80-300 employees)
- **Priorities**: Environmental metrics, stakeholder engagement

## 🔧 Configuration

### Environment Variables (.env)
```bash
OPENAI_API_KEY=your_openai_api_key_here
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### OpenAI API Key
1. Get your API key from: https://platform.openai.com/api-keys
2. Add it to your .env file
3. The system will use fallback responses if no API key is provided

## 🧪 Testing

### Run Comprehensive Tests
```bash
python test_comprehensive.py run
```

### Test Categories
- ✅ **Health & Status** - System health and service status
- ✅ **Persona Chat** - AI responses for all personas
- ✅ **DBO Scenarios** - Scenario listing and detailed analysis
- ✅ **Search & Analytics** - Advanced search and insights
- ✅ **Performance** - Response times and system performance

### Expected Results
- **95%+ success rate** for production readiness
- **<5 second response times** for all endpoints
- **Full persona coverage** with tailored responses
- **Complete scenario enhancement** with financial analysis

## 📊 API Endpoints

### Chat & AI
- `POST /api/v1/chat/` - Intelligent chat with persona awareness
- `GET /api/v1/chat/personas` - Available persona configurations

### DBO Scenarios
- `GET /api/v1/dbo/scenarios` - List all scenarios
- `POST /api/v1/dbo/scenario` - Get detailed scenario analysis
- `GET /api/v1/dbo/scenarios/search` - Advanced scenario search

### Analytics
- `GET /api/v1/analytics/summary` - System analytics and insights
- `GET /api/v1/analytics/performance` - Performance metrics
- `GET /api/v1/analytics/recommendations/trends` - Trending recommendations

## 🔗 Frontend Integration

### SustAIneers Frontend
The backend is designed to work seamlessly with the SustAIneers frontend:
- **Compatible API endpoints** matching frontend expectations
- **CORS configuration** for frontend domain
- **Persona-aware responses** aligned with UI design
- **Real-time chat functionality** with session management

### Integration URL
```bash
# Frontend URL
https://spectacular-dusk-cc7b08.netlify.app/dashboard

# Backend URL (local development)
http://localhost:8000
```

## 🚀 Production Deployment

### Docker Deployment
```bash
# Build image
docker build -t sustainability-navigator .

# Run container
docker run -p 8000:8000 --env-file .env sustainability-navigator
```

### Environment Configuration
```bash
OPENAI_API_KEY=your_production_api_key
ENVIRONMENT=production
LOG_LEVEL=WARNING
```

## 📈 Monitoring & Maintenance

### Health Monitoring
- **Health endpoint**: `/health`
- **Metrics tracking**: Response times, error rates, scenario load status
- **Logging**: Structured logging with correlation IDs

### Data Updates
- **Scenario updates**: Replace `dbo_scenarios.json` file
- **Persona configurations**: Update in `app/models/personas.py`
- **AI prompts**: Modify in `app/services/langchain_service.py`

## 👥 Team

- **Backend Development**: GreenPath AI Team
- **Frontend Development**: SustAIneers Team  
- **Integration**: Combined Team for Siemens Co-creation

## 🎯 Ready for Siemens Tech for Sustainability 2025

This professional backend demonstrates:
- ✅ **Technical Excellence** - Enterprise-grade architecture
- ✅ **Business Intelligence** - Deep sustainability domain knowledge
- ✅ **Siemens Integration** - Native ecosystem alignment
- ✅ **Scalability** - Production-ready design and performance
- ✅ **Innovation** - AI-powered personalization and decision support

---

**Built for Siemens Tech for Sustainability 2025 Co-creation Phase**
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ README.md generated")

def main():
    """Main setup function"""
    print("🚀 SustAInability Navigator Backend Setup")
    print("=" * 60)
    
    # Run all setup checks
    checks = [
        validate_python_version(),
        setup_project_structure(),
        check_dbo_scenarios(),
        create_env_file(),
        check_dependencies()
    ]
    
    # Create additional files
    create_run_script()
    generate_readme()
    
    # Final assessment
    passed_checks = sum(checks)
    total_checks = len(checks)
    
    print("\n" + "=" * 60)
    print("📊 Setup Summary")
    print("=" * 60)
    print(f"Checks passed: {passed_checks}/{total_checks}")
    
    if passed_checks == total_checks:
        print("🎉 Setup completed successfully!")
        print("\n🎯 Next Steps:")
        print("1. Add your OpenAI API key to .env file")
        print("2. Run server: python run.py")
        print("3. Test system: python test_comprehensive.py run")
        print("4. Access API docs: http://localhost:8000/docs")
        print("5. Integrate with SustAIneers frontend")
    else:
        print("⚠️  Setup completed with issues")
        print("Please address the failed checks before proceeding")
    
    print(f"\n📚 Documentation: README.md")
    print(f"🔧 Project structure created")
    print(f"🚀 Ready for development!")

if __name__ == "__main__":
    main()