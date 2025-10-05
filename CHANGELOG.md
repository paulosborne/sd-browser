# Changelog

All notable changes to the SD Browser project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure and architecture
- FastAPI backend with PostgreSQL database
- React frontend with TypeScript and TailwindCSS
- Docker Compose development environment
- User authentication system with JWT tokens
- Schedules Direct API integration client
- Database schema for EPG data and user preferences
- Basic API endpoints for auth and SD integration
- Frontend routing and page structure
- Database migrations with Alembic
- Nginx reverse proxy configuration
- Background job processing with RQ
- Prometheus metrics and health checks
- Security features (encryption, rate limiting, CORS)
- Development setup script and documentation

### Infrastructure
- Docker multi-stage builds for production
- Redis for caching and job queue
- Proper logging configuration
- Environment-based configuration management

### Security
- Encrypted storage of Schedules Direct credentials
- Rate limiting on authentication endpoints
- Security headers in Nginx configuration
- Input validation and sanitization

## [0.1.0] - 2025-10-05

### Added
- Initial release with basic foundation
- User registration and authentication
- Schedules Direct account connection
- Basic frontend application structure
- Development environment setup

---

## Planned Features

### v0.2.0 - Core EPG Features
- [ ] EPG grid view with virtualized scrolling
- [ ] Program detail modal with metadata
- [ ] Search functionality with filters
- [ ] Favourites management
- [ ] Basic recording rules

### v0.3.0 - Data Pipeline
- [ ] Background job processing
- [ ] Automatic schedule refresh
- [ ] Program metadata fetching
- [ ] XMLTV export functionality

### v0.4.0 - Advanced Features
- [ ] Calendar integration with iCal export
- [ ] Notification system
- [ ] Admin dashboard
- [ ] Rule conflict detection

### v1.0.0 - Production Ready
- [ ] Full test coverage
- [ ] Performance optimizations
- [ ] Production deployment guides
- [ ] Comprehensive documentation