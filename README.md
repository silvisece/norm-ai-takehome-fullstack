# Project Overview

This repository contains both client and server codebases for a fictional service based on the "Game of Thrones" series. The server provides access to a list of laws via a FastAPI endpoint, while the client is a Next.js application that interacts with this service.

## Server Setup

The server is implemented using FastAPI and runs inside a Docker container. It provides an API to query laws from the "Game of Thrones" universe.

### Prerequisites

- Docker installed on your machine
- An OpenAI API key (set in the `.env` file)

### Running the Server

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/silvisece/norm-ai-takehome-fullstack.git
   cd your-repo
   ```

2. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory with your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

3. **Build and Run the Docker Container**:
   ```bash
   docker build -t got-laws-api .
   docker run -d -p 80:80 --env-file .env got-laws-api
   ```

4. **Access the API**:
   - The API will be accessible at `http://localhost:80/query`.

## Client Setup

The client is a Next.js application that provides a minimal interface to interact with the server.

### Prerequisites

- Node.js and pnpm installed on your machine

### Running the Client

1. **Navigate to the Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Dependencies**:
   ```bash
   pnpm install
   ```

3. **Run the Development Server**:
   ```bash
   pnpm dev
   ```

4. **Access the Client**:
   - Open your browser and go to `http://localhost:3000` to interact with the application.

## Additional Information

- Ensure that both the server and client are running simultaneously to allow the client to communicate with the server.
- For any issues or questions, please refer to the respective README files in the `app` and `frontend` directories.
