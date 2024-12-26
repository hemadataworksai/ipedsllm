# LLM Chatbot - IPEDS (Integrated Postsecondary Education Data System)

## Overview
This repository contains the code for a Language Model (LLM) chatbot framework built using LangChain to process natural language queries into SQL. The chatbot utilizes data from IPEDS (Integrated Postsecondary Education Data System) to query postsecondary education statistics.

IPEDS is a comprehensive data source maintained by the National Center for Education Statistics (NCES), collecting data from all primary providers of postsecondary education in the United States. It covers various aspects of postsecondary education, including enrollment, graduation rates, financial aid, institutional characteristics, and more.

---

## Getting Started
Follow these instructions to set up the project on your local machine.

### Prerequisites
- **Python 3.11**
    - Download for macOS: [Python 3.11](https://www.python.org/downloads/macos/)
    - Recommended version: Python 3.11.8 (macOS 64-bit universal2 installer)

---

## Setup Steps

### 1. Install Git Using Homebrew

#### Install Homebrew:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Install Git:
```bash
brew install git
```

#### Verify Git Installation:
```bash
git --version
```

---

### 2. Install VSCode (Visual Studio Code)
Download and install Visual Studio Code from the [official website](https://code.visualstudio.com).

---

### 3. Clone the Repository

#### Clone the Repository:
```bash
git clone https://github.com/hemadataworksai/ipedsllm.git
```

---

### 4. Set Up a Virtual Environment

#### Windows:
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

#### macOS/Linux:
```bash
# Create a virtual environment
python3.11 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

---

### 5. Install Requirements
Install project dependencies using `pip`:
```bash
pip install -r apps/langchain_bot/requirements.txt
```

---

### 6. Create an `.env` File
In the root directory of the project, create a `.env` file and add the following details:

```
OPENAI_API_KEY=xxx
LLM_PROVIDER=ollama  # Options: ollama or openai
DB_URL=xxx
REDIS_URL=redis://host.docker.internal:6379  # Use redis://localhost:6379 if needed
REDIS_TOKEN=1233
TOKENIZERS_PARALLELISM=true
OLLAMA_HOST=http://host.docker.internal:11434  # Use http://localhost:11434 if needed
```

- Replace `DB_URL` with the appropriate database connection string.
- Set `LLM_PROVIDER` to `ollama` or `openai`.
- If using `openai`, provide a valid `OPENAI_API_KEY`.

#### Create an OpenAI API Key (if using OpenAI):
1. Go to [OpenAI Platform](https://platform.openai.com/usage).
2. Create an account and purchase credits.
3. Navigate to **Profile > User API Keys**.
4. Copy the key and paste it into the `.env` file under `OPENAI_API_KEY`.

---

### 7. Run the Chatbot

#### Start the Chatbot:
```bash
PYTHONPATH=. python run apps/langchain_bot/app_run.py
```

- If using `ollama` as the provider, wait for the local LLM model to download.
- Access the chatbot at: [http://localhost:8001/playground/](http://localhost:8001/playground/)

#### Embedded Model Setup:
1. Download the embedding model from [Google Drive](https://drive.google.com/drive/folders/1ANo_rGZ_bScGuDaTetj07YjxxFr9CC7G).
2. Create a folder `models/embedding_model/embedding_question2context`.
3. Unzip and copy all files into this folder.

---

## Docker Compose

### Build the Docker Image:
```bash
docker-compose build --no-cache
```

### Run the Docker Container:
```bash
docker-compose up -d
```

- Access the chatbot at: [http://localhost:8001/playground/](http://localhost:8001/playground/)

### Destroy the Docker Container:
```bash
docker-compose down
```

---

