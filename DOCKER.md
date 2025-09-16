# VN Stock Advisor - Docker Setup

This document explains how to run the VN Stock Advisor application using Docker.

## Quick Start

### 1. Setup Environment
```bash
# Create .env file from template
make docker-setup-env

# Edit .env file with your API keys
nano .env
```

### 2. Run with Docker Compose (Recommended)
```bash
# Start the application
make docker-compose-up

# View logs
make docker-compose-logs

# Stop the application
make docker-compose-down
```

### 3. Run with Docker directly
```bash
# Build the image
make docker-build

# Run the container
make docker-run
```

## Environment Configuration

The application requires API keys for external services. Copy `env.docker.template` to `.env` and fill in your keys:

### Required API Keys:
- `GEMINI_API_KEY`: Google Gemini API key (for AI analysis)
- `SERPER_API_KEY`: Serper API key (for web search)

### Optional API Keys:
- `FIRECRAWL_API_KEY`: Firecrawl API key (for web scraping)
- AWS credentials (if using AWS Bedrock models)

## Docker Commands

| Command | Description |
|---------|-------------|
| `make docker-build` | Build Docker image |
| `make docker-run` | Run container with .env file |
| `make docker-compose-up` | Start with Docker Compose |
| `make docker-compose-down` | Stop Docker Compose services |
| `make docker-compose-logs` | Show Docker Compose logs |
| `make docker-compose-restart` | Restart services |
| `make docker-setup-env` | Create .env from template |
| `make docker-clean` | Clean Docker resources |

## API Endpoints

Once running, the API will be available at:
- **API Documentation**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Data Persistence

The Docker setup includes volume mounts for:
- `./db` - Database files (ChromaDB)
- `./knowledge` - Knowledge base files

These directories will persist data between container restarts.

## Production Deployment

For production deployment:

1. **Security**: Update CORS settings in `api.py`
2. **Environment**: Use proper secrets management
3. **Monitoring**: Add logging and monitoring
4. **Scaling**: Use Docker Swarm or Kubernetes
5. **SSL**: Add reverse proxy with SSL termination

## Troubleshooting

### Container won't start
- Check if port 8000 is available
- Verify .env file exists and has valid API keys
- Check logs: `make docker-compose-logs`

### API not responding
- Wait for health check to pass (up to 40 seconds)
- Check if all required environment variables are set
- Verify API keys are valid

### Performance issues
- Increase container memory limits
- Check external API rate limits
- Monitor resource usage

## Development

For development with hot reload:

```bash
# Run locally with uv
make install
make run

# Or run specific commands
uv run api_server
uv run run_crew
```

## Architecture

The Docker setup includes:
- **Base Image**: Python 3.11 slim
- **Package Manager**: uv (faster than pip)
- **Web Server**: FastAPI with Uvicorn
- **Security**: Non-root user
- **Health Checks**: Built-in health monitoring
- **Data Persistence**: Volume mounts for database and knowledge files
