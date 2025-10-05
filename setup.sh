#!/bin/bash

# SD Browser - Development Setup Script

set -e

echo "🚀 Setting up SD Browser Development Environment"

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is required but not installed"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before continuing"
    echo "   Especially update these required values:"
    echo "   - JWT_SECRET (use a strong secret key)"
    echo "   - ENCRYPTION_KEY (exactly 32 characters)"
    echo "   - SD_APPID (your Schedules Direct app ID)"
    echo ""
    read -p "Press Enter when you've updated the .env file..."
fi

# Build and start services
echo "🏗️  Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d db redis

echo "⏳ Waiting for database to be ready..."
sleep 10

# Run database migrations
echo "🗄️  Running database migrations..."
docker-compose run --rm api alembic upgrade head

echo "📦 Installing frontend dependencies..."
docker-compose run --rm web npm install

# Start all services
echo "🌟 Starting all services..."
docker-compose up -d

# Show status
echo ""
echo "🎉 SD Browser is now running!"
echo ""
echo "📍 Access points:"
echo "   • Frontend: http://localhost:3000"
echo "   • API Docs: http://localhost:8000/docs"
echo "   • Health Check: http://localhost:8000/health"
echo ""
echo "🛠️  Useful commands:"
echo "   • View logs: docker-compose logs -f"
echo "   • Stop services: docker-compose down"
echo "   • Rebuild: docker-compose build"
echo "   • Database shell: docker-compose exec db psql -U sd_user -d sd_browser"
echo ""
echo "📚 Next steps:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Create a user account"
echo "   3. Connect your Schedules Direct account"
echo "   4. Add lineups and start browsing!"
echo ""

# Check service health
echo "🔍 Checking service health..."
sleep 5

if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend is not accessible"
fi

echo ""
echo "✨ Setup complete! Happy browsing!"