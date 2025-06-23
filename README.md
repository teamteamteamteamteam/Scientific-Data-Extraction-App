# 🧬 Scientific Data Extraction App

<div align="center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

**An interactive tool for analyzing and visualizing biological data from breast cancer cell research**

</div>

---

## 🎯 Overview

The Scientific Data Extraction App is a sophisticated tool designed for analyzing and visualizing biological data containing breast cancer cells. The application provides an interactive web-based interface for exploring compound data through dynamic visualizations, where each point represents a compound-concentration pair colored by concentration levels or MOA (Mechanism of Action) values.

### 🔬 Key Capabilities

- **Interactive Data Visualization**: Browse data through interactive plots in your browser
- **Compound Analysis**: Detailed information including SMILES notation, MOA values, and concentrations
- **Advanced Processing**: Handles BBBC021 dataset with .csv and .tif image processing
- **2D Dimensionality Reduction**: Uses UMAP algorithm for vector space visualization
- **RESTful API**: FastAPI-powered backend for seamless data access

---

## ✨ Features

### 🌐 React Frontend Features

- **🎯 Interactive Scatter Plots**: Click points for compound details
- **🎨 Real-time Color Switching**: Toggle between concentration and MOA coloring
- **📱 Responsive Design**: Works on desktop and mobile devices
- **⚡ Fast Rendering**: Optimized React components for large datasets

### 📊 Data Processing
- **CSV file formatting** and preprocessing
- **Vector calculation** from Cell Profiler analysis results
- **2D coordinate mapping** using UMAP dimensionality reduction
- **Database integration** for efficient data storage and retrieval

### 🔍 Compound Details
- **SMILES notation** for chemical structure representation
- **MOA values** for mechanism of action analysis
- **Concentration data** for dosage-response relationships
- **Image associations** linking compounds to microscopy data

---

## 🏗️ Architecture

The application follows a clean architecture pattern with clear separation between frontend and backend:

```
📁 Scientific Data Extraction App
├── 🗄️ backend/ (Python + FastAPI)
│   ├── database/ (SQLite + ready database link)
│   ├── CSV Processing & Formatting
│   ├── Vector Calculations (UMAP)
│   └── FastAPI Endpoints
├── 🌐 frontend/ (React)
│   └── Interactive Visualizations
├── 📋 documentation/ (Complete docs)
```

### Core Components

- **`Program`**: Main orchestrator class managing the entire pipeline
- **`DatabaseInterface`**: Abstract interface for database operations
- **`SQLiteDatabase`**: SQLite implementation of database operations
- **`DatabaseCreator`**: Handles database schema creation
- **`DatabaseFiller`**: Populates database with initial data
- **`CsvFormatter`**: Processes and formats CSV files
- **`CalculateVectors`**: Computes vectors and performs 2D conversion
- **`Repository`**: Data access layer for API endpoints

---

## 🚀 Quick Start with Docker

### Prerequisites

- Docker and Docker Compose
- Git

### One-Command Setup

1. **Clone and run**
   ```bash
   git clone https://github.com/yourusername/scientific-data-extraction-app.git
   cd scientific-data-extraction-app
   docker-compose up
   ```

2. **Access the application**
   - Frontend: `http://localhost:3000` (React app)
   - Backend API: `http://localhost:8888` (FastAPI)

### 🗄️ Ready-to-use Database

No need to process data from scratch! We provide a pre-built database:

- **Database location**: `backend/database/database_link.txt`
- **Contains**: Pre-processed compound data with coordinates and colors
- **Ready for**: Immediate visualization and analysis

---

## 🛠️ Development Setup

### Using Docker (Recommended)

```bash
# Development with hot reload
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

### Manual Setup (Alternative)

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🎮 Usage

### 🚀 Getting Started

1. **Start the application**
   ```bash
   docker-compose up
   ```

2. **Open your browser**
   - Navigate to `http://localhost:3000`
   - The React frontend will load with pre-processed data

3. **Explore the data**
   - View interactive scatter plot of compounds
   - Switch color modes (concentration vs MOA)
   - Click points for detailed information

### 🗄️ Database Setup

The application comes with a ready-to-use database:

```bash
# Database link is located at:
backend/database/database_link.txt

# Contains pre-processed:
- Compound information
- 2D coordinates (UMAP)
- Color mappings
- Image associations
```

### 🔧 Advanced Usage

1. **Database Initialization**
   ```python
   # Creates database tables and structure
   database_creator = DatabaseCreator()
   database_creator.create_table("compounds")
   ```

2. **CSV Processing**
   ```python
   # Formats and processes CSV files
   csv_formatter = CsvFormatter()
   csv_formatter.run_formatter()
   ```

3. **Vector Calculation**
   ```python
   # Calculates vectors and converts to 2D
   calculator = CalculateVectors()
   calculator.iterate_formatted_folder()
   calculator.convert_vectors_to_2D()
   ```

4. **Data Visualization**
   - Start the FastAPI server
   - Access the web interface
   - Explore compounds through interactive plots

### Interactive Features

- **🎯 Point Selection**: Click on any point to view detailed compound information
- **🎨 Color Modes**: Switch between concentration-based and MOA-based coloring
- **🔍 Data Filtering**: Filter compounds by various criteria
- **📊 Export Options**: Export data and visualizations

---

## 🌐 API Endpoints

The application provides a RESTful API powered by FastAPI:

### Base Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/compounds` | GET | Retrieve all compounds |
| `/compounds/colored_by_concentration` | GET | Get compounds with concentration-based colors |
| `/compounds/colored_by_moa` | GET | Get compounds with MOA-based colors |
| `/compound/details/{name}/{concentration}` | GET | Get detailed compound information |

### Example Response

```json
{
  "name": "Compound_A",
  "concentration": 0.1,
  "x": 12.34,
  "y": 56.78,
  "color": {
    "r": 255,
    "g": 128,
    "b": 0
  },
  "smiles": "CCO",
  "moa": "DNA_DAMAGE"
}
```

---

## 📚 Documentation

Comprehensive documentation is available in the `/documentation` folder:

- **📖 Full Documentation**: `Dokumentacja - ScientificDataExtractionApp.pdf`
- **📋 Documentation Review**: `Przegląd dokumentacji - ScientificDataExtractionApp.pdf`
- **🏗️ UML Diagram**: `UML - ScientificDataExtractonApp.pdf`

### Key Documentation Sections

- **Class Descriptions**: Detailed explanation of each component
- **Method Documentation**: Complete API reference for all methods
- **Data Flow**: Understanding the processing pipeline
- **Database Schema**: Table structures and relationships

---

## 🛠️ Technical Details

## 📁 Project Structure

```
scientific-data-extraction-app/
├── 📁 .github/workflows/     # CI/CD pipelines
│   └── tests.yml            # Automated testing
├── 📁 backend/              # Python FastAPI backend
│   ├── database/            # SQLite database
│   │   └── database_link.txt # Ready-to-use database link
│   ├── main.py             # FastAPI application
│   └── requirements.txt    # Python dependencies
├── 📁 frontend/            # React frontend
│   ├── src/               # React components
│   ├── package.json       # Node dependencies
│   └── vite.config.js     # Vite configuration
├── 📁 documentation/       # Complete documentation
├── 🐳 Dockerfile.backend   # Backend container
├── 🐳 Dockerfile.frontend  # Frontend container
├── 🐳 docker-compose.yml   # Service orchestration
└── 📋 README.md           # This file
```

### 🐳 Docker Configuration

The project includes optimized Docker setup:

- **`Dockerfile.backend`**: Python FastAPI container
- **`Dockerfile.frontend`**: React development/production container  
- **`docker-compose.yml`**: Orchestrates both services with proper networking
- **Exposed Ports**: Frontend (3000), Backend (8000)
- **Volume Mapping**: For development and database persistence

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
