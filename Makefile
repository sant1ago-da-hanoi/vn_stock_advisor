# VN Stock Advisor API Makefile
# Quick commands to run the API server

.PHONY: help install run clean setup-env check-env

# Default target
help:
	@echo "🚀 VN Stock Advisor API - Available Commands:"
	@echo ""
	@echo "📦 Setup & Installation:"
	@echo "  make install          - Install dependencies using uv"
	@echo "  make setup-env        - Create .env template file"
	@echo "  make check-env        - Check if .env file exists"
	@echo ""
	@echo "🏃 Running the API Server:"
	@echo "  make run        	   - Start FastAPI server on port 8000"
	@echo ""
	@echo "🔧 Utilities:"
	@echo "  make clean            - Clean cache and temporary files"
	@echo "  make logs             - Show recent logs"
	@echo ""
	@echo "🐳 Docker Commands:"
	@echo "  make dbuild     - Build Docker image"
	@echo "  make drun       - Run container with .env file"
	@echo "  make dcompose-up    - Start with Docker Compose"
	@echo "  make dcompose-down  - Stop Docker Compose services"
	@echo "  make dcompose-logs   - Show Docker Compose logs"
	@echo "  make dsetup-env     - Create .env from template"
	@echo "  make dclean         - Clean Docker resources"
	@echo ""
	@echo "📊 API Endpoints (when server is running):"
	@echo "  http://localhost:8000/docs      - Interactive API documentation"
	@echo "  http://localhost:8000/redoc     - Alternative API docs"
	@echo "  http://localhost:8000/health    - Health check"

# Installation
install:
	@echo "📦 Installing dependencies..."
	uv sync
	@echo "✅ Dependencies installed successfully!"

# Environment setup
setup-env:
	@echo "📝 Creating .env template file..."
	@if [ ! -f .env ]; then \
		echo "GEMINI_API_KEY=your_gemini_api_key" > .env; \
		echo "GEMINI_MODEL=gemini/gemini-2.0-flash-001" >> .env; \
		echo "GEMINI_REASONING_MODEL=gemini/gemini-2.5-flash-preview-04-17" >> .env; \
		echo "SERPER_API_KEY=your_serper_api_key" >> .env; \
		echo "USE_AWS_MODELS=false" >> .env; \
		echo "USE_GEMINI_MODELS=true" >> .env; \
		echo "✅ .env template created! Please edit with your API keys."; \
	else \
		echo "⚠️  .env file already exists. Skipping creation."; \
	fi

check-env:
	@echo "🔍 Checking environment configuration..."
	@if [ -f .env ]; then \
		echo "✅ .env file found"; \
		@echo "📋 Current configuration:"; \
		@grep -E "^(GEMINI_|SERPER_|USE_)" .env | sed 's/=.*/=***/' || true; \
	else \
		echo "❌ .env file not found. Run 'make setup-env' to create one."; \
	fi

# Running the API server
run:
	@echo "🚀 Starting VN Stock Advisor API server..."
	@echo "📊 API Documentation: http://localhost:8000/docs"
	@echo "🔍 Interactive API: http://localhost:8000/redoc"
	@echo "💡 Health Check: http://localhost:8000/health"
	@echo ""
	uv run api_server

# Utilities
clean:
	@echo "🧹 Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache/ 2>/dev/null || true
	rm -rf .coverage 2>/dev/null || true
	@echo "✅ Cleanup completed!"

logs:
	@echo "📋 Recent application logs:"
	@if [ -f "crewai.log" ]; then \
		tail -20 crewai.log; \
	else \
		echo "No log file found. Run the application to generate logs."; \
	fi

# Docker commands
dbuild:
	@echo "🐳 Building Docker image..."
	docker build -t vn-stock-advisor .

drun:
	@echo "🐳 Running in Docker container..."
	docker run -p 8000:8000 --env-file .env vn-stock-advisor

dcompose-up:
	@echo "🐳 Starting services with Docker Compose..."
	docker compose up -d --force-recreate --remove-orphans

dcompose-down:
	@echo "🐳 Stopping services with Docker Compose..."
	docker compose down --remove-orphans

dlog:
	@echo "📋 Showing Docker Compose logs..."
	docker compose logs -f

dcompose-restart:
	@echo "🔄 Restarting services with Docker Compose..."
	docker compose restart

dsetup-env:
	@echo "📝 Creating .env file from Docker template..."
	@if [ ! -f .env ]; then \
		cp env.docker.template .env; \
		echo "✅ .env file created from template! Please edit with your API keys."; \
	else \
		echo "⚠️  .env file already exists. Skipping creation."; \
	fi

dclean:
	@echo "🧹 Cleaning Docker resources..."
	docker compose down --volumes --remove-orphans
	@echo "✅ Docker cleanup completed!"

# Show current configuration
config:
	@echo "⚙️  Current configuration:"
	@echo "📁 Project: $(shell pwd)"
	@echo "🐍 Python: $(shell python --version 2>/dev/null || echo 'Not found')"
	@echo "📦 UV: $(shell uv --version 2>/dev/null || echo 'Not found')"
	@echo "🔧 CrewAI: $(shell uv run crewai --version 2>/dev/null || echo 'Not found')"
	@echo ""
	@make check-env
