# FastApi-AI-Interview-Coach

## 🧠 Project Overview

FastApi-AI-Interview-Coach is an AI-powered interview coaching tool built with FastAPI. It simulates real-world interview scenarios, providing users with personalized feedback and guidance to improve their interview skills.

## 🛠️ Key Features

* **FastAPI Backend**: High-performance asynchronous API built with FastAPI.
* **Dockerized Deployment**: Includes Dockerfile and Compose for containerization.
* **Modular Architecture**: Clean separation of concerns (`api`, `auth`, `core`, `services`).
* **Database Integration**: SQLAlchemy ORM and Alembic migrations.
* **Environment Configuration**: `.env` file support for easy config.

## 🚀 Getting Started

### Prerequisites

* Docker and Docker Compose installed
* OpenAI API key

### Installation

1. **Clone the Repository**

```bash
git clone https://github.com/bbtqqrl/FastApi-AI-Interview-Coach.git
cd FastApi-AI-Interview-Coach
```

2. **Create `.env` File**

```ini
OPENAI_API_KEY=your_openai_api_key
DB_HOST=your_db_host
DB_PORT=5432
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
PRIVATE_KEY_PATH=certs/jwt-private.pem
PUBLIC_KEY_PATH=certs/jwt-public.pem
ALGORITHM=RS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. **Build and Run the Application**

```bash
docker compose up --build
```

4. **Access the API Docs**
   Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🔮 Project Structure

```
FastApi-AI-Interview-Coach/
├── alembic/                # DB migrations
├── api/                    # API routers
├── auth/                   # Auth logic
├── core/                   # Configuration, models, helpers
├── services/               # App logic (e.g., AI, Redis)
├── certs/                  # JWT keys
├── Dockerfile              # App Docker image
├── compose.yaml            # Docker Compose config
├── .env                    # Environment variables
├── main.py                 # App entry point
├── requirements.txt        # Python packages
└── README.md               # Project documentation
```

## 🎓 Testing

```bash
pytest
```

## 📄 License

This project is licensed under the MIT License.
