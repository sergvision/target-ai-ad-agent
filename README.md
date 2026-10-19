
# Target AI Ad Agent

AI agent for website analysis and targeted advertising content generation.

## Project overview

The application analyzes a public website, processes its HTML content, uses an LLM to generate structured marketing insights, and creates advertising post examples.

## Features

- Website HTML retrieval and text extraction
- Multi-step AI analysis
- Marketing insights and audience analysis
- Generation of advertising post examples
- FastAPI backend with interactive Swagger documentation
- React + Vite frontend
- Docker and Docker Compose configuration

## Live links

- Frontend: https://sergvision.github.io/target-ai-ad-agent/
- Backend API: https://target-ai-ad-agent-latest.onrender.com
- API documentation: https://target-ai-ad-agent-latest.onrender.com/docs
- Health check: https://target-ai-ad-agent-latest.onrender.com/health

## Technologies

- Python
- FastAPI
- React
- Vite
- Docker
- Docker Compose
- Google Gemini API

## Local setup

1. Clone this repository.
2. Create a `.env` file in the project root.
3. Add your API configuration to `.env`:

   `GEMINI_API_KEY=your_api_key`

4. Install Docker and Docker Compose if they are not already installed.
5. Start the services:

   `docker compose up --build`

Do not commit `.env` or publish API keys.

## API usage

Open `/docs` on the deployed backend to inspect the API and test available endpoints.

## Project status

The backend API has been deployed and tested. The frontend has been published through GitHub Pages; full frontend functionality still requires verification.
