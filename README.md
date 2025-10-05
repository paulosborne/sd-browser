# Schedules Direct EPG Browser

A production-ready web application that integrates with Schedules Direct to fetch, cache, search, and present EPG (Electronic Program Guide) data. Features user management, favorites, recording rules, XMLTV export, and optional PVR integration.

## Features

- **Multi-user Authentication**: Email/password with optional 2FA (TOTP)
- **Schedules Direct Integration**: Secure token storage and API integration
- **EPG Guide**: Grid view (time × channel), Now/Next, single-channel timeline
- **Search & Filters**: Title, person, keyword, genre, channel, date range
- **Favorites & Alerts**: Follow shows/teams/keywords with notifications
- **Recording Rules**: Series pass with conflict detection
- **Calendar Integration**: Agenda view with iCal export
- **XMLTV Export**: Standards-compliant XML for selected channels
- **Admin Dashboard**: Job monitoring, health checks, quota management

## Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn, PostgreSQL, Redis, RQ
- **Frontend**: React 18, TypeScript, Vite, TanStack Query, TailwindCSS
- **Infrastructure**: Docker Compose, Nginx reverse proxy
- **Observability**: OpenTelemetry, Prometheus metrics, structured logging

## Quick Start

1. **Prerequisites**
   ```bash
   docker --version  # Docker 20.10+
   # Either Docker Compose v2 (recommended):
   docker compose version
   # Or Docker Compose v1:
   docker-compose --version
   ```

2. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd sd-browser
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start Services**
   ```bash
   # The setup script will automatically detect your Docker Compose version
   ./setup.sh
   
   # Or manually with Docker Compose v2:
   docker compose up -d
   
   # Or manually with Docker Compose v1:
   docker-compose up -d
   ```

4. **Initialize Database**
   ```bash
   # Docker Compose v2:
   docker compose exec api alembic upgrade head
   
   # Docker Compose v1:
   docker-compose exec api alembic upgrade head
   ```

5. **Access Application**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs
   - Admin: http://localhost:3000/admin

## Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Run Tests
```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm test

# E2E
npx playwright test
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Application
APP_ENV=development
APP_BASE_URL=http://localhost:3000

# Database
DB_URL=postgresql://user:pass@localhost:5432/sd_browser

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
JWT_SECRET=your-secret-key
ENCRYPTION_KEY=your-encryption-key

# Schedules Direct
SD_API_BASE=https://json.schedulesdirect.org/20141201
SD_APPID=your-app-id

# Optional
EMAIL_SMTP_URI=smtp://user:pass@smtp.example.com:587
OBJECT_STORAGE_URI=file:///tmp/exports
```

## API Documentation

- Interactive API docs: http://localhost:8000/docs
- OpenAPI spec: http://localhost:8000/openapi.json

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Frontend    │────│      API        │────│   Schedules     │
│   React + TS    │    │     FastAPI     │    │    Direct       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
            ┌───────────┐ ┌───────┐ ┌───────┐
            │PostgreSQL │ │ Redis │ │  RQ   │
            │    DB     │ │ Cache │ │ Jobs  │
            └───────────┘ └───────┘ └───────┘
```

## Security

- JWT authentication with refresh tokens
- Encrypted SD credentials at rest
- Rate limiting per user
- CORS protection
- Input validation and sanitization
- PII minimization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## License

MIT License - see LICENSE file for details