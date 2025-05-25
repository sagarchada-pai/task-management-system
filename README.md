# Task Management System

A full-stack task management application built with Vue 3 (TypeScript) and FastAPI (Python). This application provides a complete solution for managing projects, tasks, and team collaboration with a modern, responsive interface.

## 🌟 Features

### Frontend (Vue 3)
- **User Interface**
  - Modern, responsive design
  - Real-time updates
  - Intuitive task management
  - Interactive dashboards

### Backend (FastAPI)
- **Core Functionality**
  - RESTful API endpoints
  - JWT Authentication
  - Role-based access control
  - Database management

### Full-Stack Features
- **User Management**
  - Registration and authentication
  - Profile management
  - Team collaboration
- **Project Management**
  - Create and organize projects
  - Assign team members
  - Track progress
- **Task Management**
  - Create and assign tasks
  - Set priorities and due dates
  - Task comments and mentions

## 🛠 Tech Stack

### Frontend
- **Framework**: Vue 3 with Composition API
- **Language**: TypeScript
- **State Management**: Pinia
- **Routing**: Vue Router
- **UI Framework**: Tailwind CSS
- **HTTP Client**: Axios
- **Build Tool**: Vite

### Backend
- **Framework**: FastAPI (Python 3.13+)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Data Validation**: Pydantic v2
- **Migrations**: Alembic
- **API Documentation**: OpenAPI (Swagger UI & ReDoc)

## 📋 Prerequisites

- Node.js 18+ (for frontend)
- Python 3.13+ (for backend)
- npm or yarn
- SQLite (included with Python)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/sagarchada-pai/task-management-system.git
cd task-management-system
```

### 2. Backend Setup

#### Set Up Python Environment

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Configure Backend

1. Create a `.env` file in the `backend` directory:
   ```env
   # Application
   ENVIRONMENT=development
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # Database (SQLite)
   DATABASE_URL=sqlite:///./sql_app.db
   
   # CORS (for frontend development)
   FRONTEND_URL=http://localhost:5173
   ```

2. Initialize the database:
   ```bash
   # Run migrations
   alembic upgrade head
   
   # Create initial data (if available)
   python -m app.db.init_db
   ```

3. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`

### 3. Frontend Setup

#### Install Dependencies

```bash
# From the project root
cd frontend
npm install
```

#### Configure Frontend

1. Create a `.env` file in the `frontend` directory:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   # Add other frontend environment variables as needed
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## 📚 Documentation

### API Documentation
Access these when the backend server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗 Project Structure

### Backend
```
backend/
├── app/
│   ├── api/               # API routes
│   ├── core/              # Core functionality
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   └── main.py            # FastAPI application
├── alembic/              # Database migrations
└── tests/                 # Test files
```

### Frontend
```
frontend/
├── public/              # Static files
├── src/
│   ├── assets/          # Images, fonts, etc.
│   ├── components/      # Reusable components
│   ├── router/          # Vue Router config
│   ├── stores/          # Pinia stores
│   ├── views/           # Page components
│   └── main.ts          # App entry point
└── vite.config.ts       # Vite configuration
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test:unit
```

## 🚀 Deployment

### Backend (Production)

1. Update `.env` for production:
   ```env
   ENVIRONMENT=production
   SECRET_KEY=your-strong-secret-key
   ```

2. Install production dependencies:
   ```bash
   pip install gunicorn uvicorn[standard]
   ```

3. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
   ```

   > **Note**: For production, consider using a more robust database like PostgreSQL. Update the `DATABASE_URL` in your `.env` file if you switch to a different database.

### Frontend (Production)
1. Build for production:
   ```bash
   cd frontend
   npm run build
   ```

2. Deploy the `dist` directory to your preferred static file hosting service.

### Using Docker (Optional)

1. Create a `docker-compose.yml` file in the project root with the following content:
   ```yaml
   version: '3.8'
   
   services:
     backend:
       build: 
         context: ./backend
         dockerfile: Dockerfile
       ports:
         - "8000:8000"
       environment:
         - ENVIRONMENT=production
         - SECRET_KEY=your-secret-key-here
         - DATABASE_URL=sqlite:////app/sql_app.db
       volumes:
         - ./sql_app.db:/app/sql_app.db
   
     frontend:
       build:
         context: ./frontend
         dockerfile: Dockerfile
       ports:
         - "5173:80"
       depends_on:
         - backend
   ```

2. Build and start the containers:
   ```bash
   docker-compose up --build -d
   ```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ✨ Features

- **🔐 Authentication & Authorization**
  - JWT-based authentication
  - User registration and profile management
  - Role-based access control

- **📊 Project Management**
  - Create and manage projects
  - Assign team members
  - Track project progress

- **✅ Task Management**
  - Create, update, and track tasks
  - Set priorities and due dates
  - Task status workflow

- **💬 Collaboration**
  - Add comments to tasks
  - Mention team members
  - Activity tracking

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI (Python 3.13+)
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT
- **Data Validation**: Pydantic v2
- **Database Migrations**: Alembic
- **API Documentation**: OpenAPI (Swagger UI & ReDoc)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.13 or higher
- pip (Python package manager)
- SQLite (included with Python)
- (Optional) PostgreSQL for production

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/sagarchada-pai/task-management-system.git
cd task-management-system/backend
```

### 2. Set Up Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `backend` directory with the following content:

```env
# Application
ENVIRONMENT=development
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///./sql_app.db

# CORS (for frontend development)
FRONTEND_URL=http://localhost:5173
```

### 5. Initialize the Database

```bash
# Run database migrations
alembic upgrade head

# Create initial data (optional)
python -m app.db.init_db
```

### 6. Start the Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Project Structure

```
backend/
├── app/
│   ├── api/               # API routes (v1, v2, etc.)
│   │   └── v1/
│   │       ├── endpoints/  # Route handlers
│   │       └── __init__.py
│   ├── core/              # Core functionality
│   │   ├── config.py      # Application configuration
│   │   ├── security.py    # Authentication & authorization
│   │   └── database.py    # Database connection
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── db/                # Database initialization
│   └── main.py            # FastAPI application
├── alembic/              # Database migrations
├── tests/                 # Test files
├── .env                  # Environment variables
└── requirements.txt      # Python dependencies
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app --cov-report=term-missing
```

## 🚀 Deployment

### Production with Uvicorn and Gunicorn

1. Install production dependencies:
   ```bash
   pip install gunicorn uvicorn[standard]
   ```

2. Update your `.env` file for production with your database credentials if you're using a different database than SQLite.

3. Start the production server:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
   ```

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t task-management-api .
   ```

2. Run the container:
   ```bash
   docker run -d --name task-api -p 8000:80 task-management-api
   ```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Getting Started

### Backend Setup

1. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env` file in the frontend directory:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## API Documentation

Once the backend server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
task-management-system/
├── backend/                  # Backend (FastAPI)
│   ├── app/
│   │   ├── api/              # API routes
│   │   ├── core/             # Core functionality
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   └── main.py           # FastAPI application
│   ├── alembic/              # Database migrations
│   └── requirements.txt       # Python dependencies
│
└── frontend/                 # Frontend (Vue 3)
    ├── public/               # Static files
    ├── src/
    │   ├── api/             # API client
    │   ├── assets/           # Static assets
    │   ├── components/       # Vue components
    │   ├── router/           # Vue Router configuration
    │   ├── stores/           # Pinia stores
    │   ├── views/            # Page components
    │   └── App.vue           # Root component
    └── package.json          # Node.js dependencies
```

## Available Scripts

### Backend

- `uvicorn app.main:app --reload` - Start the development server
- `pytest` - Run backend tests
- `alembic revision --autogenerate -m "description"` - Create a new migration
- `alembic upgrade head` - Apply migrations

### Frontend

- `npm run dev` - Start the development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run test:unit` - Run unit tests
- `npm run lint` - Lint and fix files

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm run test:unit
```

## Deployment

### Backend

1. Set up a production-ready ASGI server like Uvicorn with Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
   ```

2. Configure environment variables for production:
   - Set `ENVIRONMENT=production`
   - Update database connection string
   - Set a strong `SECRET_KEY`

### Frontend

1. Build the production assets:
   ```bash
   npm run build
   ```

2. Deploy the generated `dist` folder to a static file hosting service like Vercel, Netlify, or Nginx.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Vue.js](https://vuejs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Pinia](https://pinia.vuejs.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)