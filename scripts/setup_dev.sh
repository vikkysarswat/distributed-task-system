#!/bin/bash
# Development environment setup script

set -e

echo "Setting up Distributed Task System development environment..."

# Check if Python 3.11+ is installed
if ! command -v python3.11 &> /dev/null; then
    echo "Python 3.11+ is required but not installed."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
echo "Setting up pre-commit hooks..."
pre-commit install

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env file with your configuration"
fi

# Setup database
echo "Setting up database..."
docker-compose up -d postgres redis

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Create sample data
echo "Creating sample data..."
python scripts/create_sample_data.py

echo "Development environment setup complete!"
echo ""
echo "To start the development server:"
echo "  source venv/bin/activate"
echo "  python -m src.api.main"
echo ""
echo "To start all services:"
echo "  docker-compose up -d"
echo ""
echo "Access points:"
echo "  API Documentation: http://localhost:8000/docs"
echo "  Flower (Celery): http://localhost:5555"
echo "  Prometheus: http://localhost:9090"
echo "  Grafana: http://localhost:3000 (admin/admin123)"