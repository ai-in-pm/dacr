# Digital AI Currency Reserve (DACR) System

A digital currency system for AI services, pegged 1:1 to the US Dollar (₳1 = $1).
![image](https://github.com/user-attachments/assets/cc473c83-f437-4c04-a41b-b63c160810cd)
![image](https://github.com/user-attachments/assets/5b29d1f2-6e00-4e84-bd95-05a8c8ae247e)



## Overview

The Digital AI Currency Reserve (DACR) system manages the Digital AI Currency (DAC), a digital representation of the US Dollar designed specifically for funding and powering Large Language Models (LLMs). The system implements a comprehensive framework for currency generation, distribution, and management.

## Features

- 1:1 USD pegging (₳1 = $1)
- Transparent currency generation and issuance
- Robust reserve management
- Real-time supply control mechanisms
- Secure transaction processing
- API integration capabilities
- Comprehensive reporting and analytics

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Architecture

The system consists of several key components:
- Currency Generation Engine
- Reserve Management System
- Distribution Controller
- Security and Governance Framework
- API Gateway
- Analytics and Reporting Module

## Deployment

### Using Docker (Recommended)

1. Make sure you have Docker and Docker Compose installed
2. Create a `.env` file with required environment variables:
   ```bash
   SECRET_KEY=your-secret-key-here
   ```
3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
4. The API will be available at `http://localhost:8000`
5. Access the API documentation at `http://localhost:8000/docs`

### Manual Deployment

1. Install PostgreSQL and create a database
2. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set environment variables:
   ```bash
   export DATABASE_URL=postgresql://user:password@localhost/dacr
   export SECRET_KEY=your-secret-key-here
   ```
5. Run database migrations:
   ```bash
   alembic upgrade head
   ```
6. Start the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## API Documentation

The API documentation is available at `/docs` when the application is running. Here are the main endpoints:

### Currency Management
- `GET /api/v1/currency/info`: Get current currency information
- `POST /api/v1/currency/issue`: Issue new currency
- `POST /api/v1/currency/transfer`: Transfer currency between addresses

### Reserves
- `GET /api/v1/reserves/status`: Get current reserve status
- `GET /api/v1/reserves/history`: Get reserve history

### Analytics
- `GET /api/v1/analytics/supply`: Get supply metrics
- `GET /api/v1/analytics/transactions`: Get transaction metrics
- `GET /api/v1/analytics/reserves`: Get reserve metrics

### Governance
- `POST /api/v1/governance/proposals`: Create new proposal
- `GET /api/v1/governance/proposals`: List proposals
- `POST /api/v1/governance/vote`: Vote on proposal

## Security

The system implements several security measures:
- JWT-based authentication
- Role-based access control
- Secure transaction processing
- Input validation and sanitization
- Rate limiting
- Audit logging

## Monitoring

The application exposes metrics for monitoring:
- Prometheus metrics at `/metrics`
- Health check endpoint at `/health`
- Detailed logging for all operations

## License

MIT License
