# ENSAI-2A-projet-Conception-Logicielle : Rocket League Data Analyst

[![CI/CD Pipeline](https://github.com/morgannder/ENSAI-2A-S2-ConceptionLog/actions/workflows/deploy.yml/badge.svg?branch=develop)](https://github.com/morgannder/ENSAI-2A-S2-ConceptionLog/actions/workflows/deploy.yml)

Welcome to our Rocket League Data Analyst project! This application allows you to search for Rocket League players across all platforms, view their global statistics, and analyze their recent matches.

---

## Live Version (Deployed on SSPCloud)

You don't need to install anything to try the application. It is currently deployed and accessible online:
- **Frontend (Website)**: [http://rocketclstats.api.kub.sspcloud.fr/](http://rocketclstats.api.kub.sspcloud.fr/)
- **Backend API (Swagger)**: [http://rocketcl.api.kub.sspcloud.fr/](http://rocketcl.api.kub.sspcloud.fr/)

---

## Prerequisites & Tools

If you want to run the project locally, you will need the following tools installed on your machine:
- [Visual Studio Code](https://code.visualstudio.com/) (Recommended IDE)
- [Python 3.13](https://www.python.org/) (Backend)
- [Node.js & npm](https://nodejs.org/) (Frontend - Required to run the website)
- [Git](https://git-scm.com/)
- [uv](https://github.com/astral-sh/uv) (Extremely fast Python package installer and resolver)

---
## Local Installation Guide

### 1. Clone the repository
Open Git Bash or your terminal and run the following commands one by one:
* `git clone https://github.com/morgannder/ENSAI-2A-S2-ConceptionLog`
* `cd ENSAI-2A-S2-ConceptionLog`

*Open this folder in Visual Studio Code (File > Open Folder). Make sure ENSAI-2A-S2-ConceptionLog is the root of your Explorer, otherwise the application might not launch properly.*

### 2. Backend Setup (FastAPI / Python)
1. **Sync dependencies**: In your terminal, run the command: `uv sync`
2. **Environment Variables**: Create a `.env` file at the root of the project (use `.env.template` as a guide) and fill in the required variables.
3. **Database Setup**:
   - Download the pre-filled SQLite database (~70,000 matches) here: [rocket_league.db](https://www.dropbox.com/scl/fi/nquvnhja079u5v6gfs1lp/rocket_league.db?rlkey=faf14s3qzon59k5utb2d1xdqs&st=dr943fdl&dl=0)
   - Rename the downloaded file to `rocket_league.db` and place it inside the `src/database/` directory.
4. **Start the API**: Run the command `python main.py`
   *The API will be accessible at http://localhost:8000.*

### 3. Frontend Setup (React / Vite)
To run the website interface, you need to use npm (Node Package Manager).
1. Open a **new** terminal window (keep the backend running in the first one).
2. Navigate to the frontend directory using: `cd frontend/`
3. **Install dependencies**: Run `npm install` (This will download all the required Javascript packages).
4. **Start the development server**: Run `npm run dev`
   *The website will be accessible locally, usually at http://localhost:5173.*

   ---

## API Key Generation (Ballchasing)

To fully use the local version and fetch new matches, you will need a Ballchasing API Key.
1. Create an account on [Ballchasing.com](https://ballchasing.com/) using your Steam account.
2. Go to the **Upload** tab.
3. Under **Upload Token**, generate a new token.
4. Copy this token and paste it into your `.env` file as `BALLCHASING_API_KEY`.

> **Note on Rate Limits**:
> * A standard personal key is limited to **2 requests/second** and **500 requests/hour**.
> * The live version deployed on SSPCloud has an upgraded limit of **1000 requests/hour**.

---

## Repository Overview

### Main Files
| Item | Description |
| --- | --- |
| `README.md` | Provides useful information to present, install, and use the application |
| `LICENSE` | Specifies the usage rights and licensing terms for the repository |
| `main.py` | Entry point to execute and launch the FastAPI backend server |
| `.env.template` | Provides a template to create your own local `.env` configuration file |

### Folders
| Folder | Description |
| --- | --- |
| `src/` | Contains the Python backend code (FastAPI router, database models, etc.) |
| `frontend/` | Contains the React/Vite website source code, assets, and components |
| `kubernetes/` | Contains the YAML deployment files (Ingress, Services, Deployments) |
| `scripts/` | Contains old scripts used to parse JSON files and initialize the DB |
| `tests/` | Contains the Python unit tests for the backend |
| `.github/workflows/` | Contains the CI/CD pipeline configuration (`deploy.yml`) |

> *Note: Before the start of the project, we gathered around 70,000 matches in JSON files. The `scripts/` folder contains the logic we used to initially populate our database. It is not used actively anymore but remains for documentation purposes.*

---

## Unit Tests

To ensure the backend is working correctly, you can run the test suite. In your terminal (at the root of the project), run the command:
* `uv run pytest --cov=src tests/`

This will execute all tests and provide a total coverage report for the `src` directory.
