# Development Notes

## Architecture Overview

The SD Browser application follows a modern full-stack architecture:

### Backend (Python/FastAPI)
- **Framework**: FastAPI with async support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis for session storage and API caching
- **Jobs**: RQ (Redis Queue) for background processing
- **Authentication**: JWT tokens with refresh mechanism
- **Security**: Encrypted SD credentials, rate limiting, CORS protection

### Frontend (React/TypeScript)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development and building
- **State Management**: Zustand for app state, TanStack Query for server state
- **Styling**: TailwindCSS with custom component classes
- **Routing**: React Router v6

### Infrastructure
- **Development**: Docker Compose with hot reloading
- **Reverse Proxy**: Nginx with rate limiting and security headers
- **Observability**: Prometheus metrics, structured JSON logging
- **Database Migrations**: Alembic for schema versioning

## Key Features Implemented

### ✅ Authentication System
- User registration and login
- JWT access/refresh token flow
- Password hashing with bcrypt
- Basic user session management

### ✅ Schedules Direct Integration
- SD API client with retry logic and rate limiting
- Encrypted credential storage
- Lineup management endpoints
- Token refresh handling

### ✅ Database Schema
- Complete normalized schema for EPG data
- User data (favourites, rules, notifications)
- Proper indexing for performance
- PostgreSQL-specific features (ARRAY, JSON columns)

### ✅ API Structure
- RESTful endpoints following OpenAPI standards
- Proper error handling and validation
- Rate limiting and security middleware
- Health checks and metrics endpoints

### ✅ Frontend Foundation
- Modern React application structure
- Type-safe development with TypeScript
- Responsive design with TailwindCSS
- Client-side routing and state management

## Next Implementation Steps

### 🔄 Core EPG Features
1. **Guide Grid Component**
   - Virtualized grid with react-window
   - Time-based channel lineup display
   - Program detail drawer/modal
   - Efficient data fetching and caching

2. **Program Search**
   - Full-text search with PostgreSQL
   - Advanced filtering (genre, date, etc.)
   - Search result pagination
   - Auto-complete suggestions

3. **Favourites & Rules**
   - Add/remove program favourites
   - Create series recording rules
   - Conflict detection for overlapping rules
   - Notification system for matches

### 🔄 Data Pipeline
1. **Background Jobs**
   - Nightly schedule refresh jobs
   - Program metadata fetching
   - Image downloading and caching
   - Rule matching and notifications

2. **XMLTV Export**
   - Standards-compliant XML generation
   - Configurable channel selection
   - Downloadable file generation
   - Caching for performance

### 🔄 Advanced Features
1. **Calendar Integration**
   - iCal feed generation
   - Upcoming recordings view
   - Time zone handling
   - Agenda/week/month views

2. **Admin Dashboard**
   - Job queue monitoring
   - System health metrics
   - User management
   - Performance analytics

## Development Workflow

### Starting Development
```bash
# Initial setup
./setup.sh

# Start with logs
docker-compose up

# Or start in background
docker-compose up -d
docker-compose logs -f api web
```

### Database Operations
```bash
# Create new migration
docker-compose exec api alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec api alembic upgrade head

# Database shell
docker-compose exec db psql -U sd_user -d sd_browser
```

### Testing
```bash
# Backend tests
docker-compose exec api pytest

# Frontend tests
docker-compose exec web npm test

# E2E tests (when implemented)
docker-compose exec web npx playwright test
```

## API Integration Notes

### Schedules Direct API
- Base URL: https://json.schedulesdirect.org/20141201
- Requires valid subscription and app registration
- Rate limited: ~5000 requests per day
- Uses SHA1 password hashing for authentication
- Supports gzip compression and ETag caching

### Key Endpoints Used
- `POST /token` - Authentication
- `GET /lineups` - Available lineups
- `GET /lineups/{id}` - Lineup details with stations
- `POST /schedules` - Batch schedule fetching
- `POST /programs` - Program metadata
- `POST /metadata/programs` - Program images

## Security Considerations

### Data Protection
- SD credentials encrypted at rest using Fernet
- JWT secrets properly configured
- Rate limiting on authentication endpoints
- CORS configured for production domains

### Privacy
- PII minimization in logs
- Secure session handling
- No SD data redistribution to non-members
- Proper data retention policies needed

## Performance Optimizations

### Database
- Proper indexing on frequently queried columns
- Composite primary keys for efficiency
- ARRAY and JSON columns for complex data
- Connection pooling

### Caching Strategy
- Redis for API response caching
- Program detail cache with TTL
- Guide grid data cached by time window
- ETags for conditional requests

### Frontend
- Code splitting and lazy loading
- Virtualized lists for large datasets
- Optimistic updates for better UX
- Proper error boundaries

## Deployment Notes

### Production Checklist
- [ ] Environment variables properly set
- [ ] Database backups configured
- [ ] SSL certificates installed
- [ ] Monitoring and alerting setup
- [ ] Log aggregation configured
- [ ] Rate limits tuned for production
- [ ] SD API quotas monitored

### Scaling Considerations
- Horizontal scaling of API workers
- Database read replicas for queries
- CDN for static assets
- Redis clustering for high availability
- Load balancing for multiple instances