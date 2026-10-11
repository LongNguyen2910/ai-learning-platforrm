# AI Learning Platform (LMS)

## Project Overview
This repository contains the source code for the AI Learning Platform, a personal learning management system integrated with Retrieval-Augmented Generation (RAG) capabilities. 

The project follows a Modular Monolith architecture within a single repository (Monorepo), designed for maintainability, ease of local development, and strict dependency management.

## System Architecture & Tech Stack

*   **Architecture Pattern:** Modular Monolith (Monorepo)
*   **Frontend:** Next.js (App Router), Tailwind CSS, shadcn/ui.
*   **Backend:** Python 3.12+, FastAPI, LlamaIndex.
*   **Database & Infrastructure:**
    *   Relational DB: PostgreSQL 15
    *   Vector Search: Qdrant
    *   Message Broker / Cache: Redis 7
*   **Containerization:** Docker & Docker Compose
*   **Package Managers:** `pnpm` (Frontend), `uv` (Backend)

---

## Prerequisites

All team members must ensure their local development environment meets the following requirements before proceeding.

### 1. Container Runtime
Choose the appropriate Docker setup based on your role and operating system:
*   **Application Developers (Windows/macOS):** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/). Ensure the Docker engine is running before starting the database services.

### 2. Frontend Dependencies
*   **Node.js:** Version 20.x or higher.
*   **pnpm:** Installed globally via `npm install -g pnpm`.

### 3. Backend Dependencies
*   **uv:** The ultra-fast Python package installer and resolver.
    *   macOS/Linux/WSL: `curl -LsSf https://astral.sh/uv/install.sh | sh`
    *   Windows: `irm https://astral.sh/uv/install.ps1 | iex`

---

## Strict Tooling & Dependency Guidelines

To prevent lockfile conflicts, environment pollution, and deployment failures, the following rules are strictly enforced. Violating these may result in failed CI/CD pipelines.

1.  **Frontend Package Management:**
    *   **DO NOT use `npm install` or `yarn`.**
    *   All package additions must use: `pnpm add <package-name>`
2.  **Backend Package Management:**
    *   **DO NOT use `pip install`.**
    *   All package additions must use: `uv pip install <package-name>`
    *   After installation, you must freeze dependencies: `uv pip freeze > requirements.txt`
3.  **Infrastructure Mutability:**
    *   Do not modify `docker-compose.yml` (e.g., changing exposed ports, adding new services) without prior review and approval from the infrastructure lead.

---

## Local Development Setup

Follow these steps sequentially to spin up the local development environment. Open three separate terminal sessions at the root of the repository.

### Step 1: Initialize Infrastructure Services
Start the PostgreSQL, Qdrant, and Redis containers in detached mode.
```bash
docker compose up -d
```
*Verify services are running by executing `docker ps`. Services will be available at 5432 (Postgres), 6333 (Qdrant), and 6379 (Redis).*

### Step 2: Start the Backend (FastAPI)
Navigate to the backend directory, initialize the virtual environment, and install dependencies.
```bash
cd backend

# Initialize and activate virtual environment (Linux/macOS/WSL)
uv venv
source .venv/bin/activate
# For Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```
*(Note: Duplicate `.env.example` to `.env` before running the application. Server start commands will be documented here once the API entry point is established).*

### Step 3: Start the Frontend (Next.js)
Navigate to the frontend directory, install dependencies, and start the development server.
```bash
cd frontend

# Install dependencies via pnpm
pnpm install

# Start the development server
pnpm dev
```
*The frontend application will be accessible at `http://localhost:3000`.*

---

## Version Control & Git Convention

To maintain a clean and readable commit history, all contributions must adhere to the following conventions:

### Branching Strategy
Create a new branch for every task. Do not push directly to the `main` branch.
*   Feature: `feature/<descriptive-name>` (e.g., `feature/pdf-upload`)
*   Bugfix: `fix/<descriptive-name>` (e.g., `fix/button-alignment`)

### Commit Messages
We follow the Conventional Commits specification. Every commit message must include a valid prefix:
*   `feat:` A new feature.
*   `fix:` A bug fix.
*   `chore:` Routine tasks, configuration updates, or dependency upgrades.
*   `docs:` Documentation changes.
*   `refactor:` Code changes that neither fix a bug nor add a feature.

**Example:** `feat: integrate Qdrant client for document retrieval`