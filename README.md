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

Installing Docker:

https://docs.docker.com/engine/install/

### Build the Docker Image:
```bash
docker-compose build --no-cache
```


### Build the Docker Image with Cache (Faster Rebuild):
```bash
docker-compose build
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

Certainly! Here's an updated version of the README section with the addition of `docker ps`:

---

## Troubleshooting Docker

When working with Docker, you may encounter a variety of issues. Below is a guide to help you diagnose and troubleshoot common problems.

### 1. **Docker Daemon Not Running**

If you're getting errors like `Cannot connect to the Docker daemon`, it means the Docker daemon is not running. To start Docker:

- **On Linux:**
  ```bash
  sudo systemctl start docker
  ```

- **On macOS and Windows:** Docker should start automatically. If not, manually start Docker from the Docker Desktop application.

You can verify the Docker daemon is running by checking its status:
```bash
sudo systemctl status docker
```

### 2. **Permission Denied Error**

You might encounter `Permission Denied` when trying to run Docker commands. This typically occurs when you're not in the `docker` group.

To fix this:

1. Add your user to the `docker` group:
   ```bash
   sudo usermod -aG docker $USER
   ```
2. Log out and log back in, or restart your computer to apply the changes.

### 3. **Docker Container Crashes**

If a container crashes immediately after starting, it could be due to a misconfiguration, resource limits, or application errors.

- **Check logs for errors:**
  ```bash
  docker logs <container_name_or_id>
  ```

- If your container is exiting because of a configuration issue, such as missing environment variables, fix the issue and try again.

### 4. **Out of Memory (OOM) Errors**

Sometimes, containers run out of memory, especially when you're dealing with resource-intensive applications.

- **Increase the memory limit** in your Docker settings or configure memory limits for your containers using `-m` or `--memory` flags:
  ```bash
  docker run -m 4g my_image
  ```

- Ensure that your containerized application is optimized to use memory efficiently.

### 5. **Port Conflicts**

If you’re unable to bind ports, make sure no other services are using the same port on your system. You can check which service is using a port with:
- **On Linux/macOS:**
  ```bash
  sudo lsof -i :<port_number>
  ```

- **On Windows:**
  ```bash
  netstat -ano | findstr :<port_number>
  ```

### 6. **Docker Images Not Found**

If Docker can’t find the image you’re trying to pull or use, make sure that the image name is correct and exists in the Docker registry.

- Verify the image is available:
  ```bash
  docker search <image_name>
  ```

- If the image is private, ensure you have access by logging into the registry:
  ```bash
  docker login
  ```

### 7. **Network Issues in Containers**

If your containers are not able to reach external services, there might be issues with Docker’s network settings.

- Check the network configuration of your container:
  ```bash
  docker network ls
  docker network inspect <network_name>
  ```

- If your container needs external access, ensure that the network mode is set to `host` or configure proper port mapping with `-p` when running the container.

### 8. **Build Failures**

If your Docker build fails, check the build logs for errors. Common issues include:

- **Missing dependencies** in the Dockerfile.
- **Permissions issues** in files being copied into the container.
- **Incorrect commands** or invalid syntax in the Dockerfile.

To debug build errors, use the `--no-cache` option to avoid using cached layers:
```bash
docker build --no-cache -t my_image .
```

### 9. **Viewing Running Containers**

You can view all running Docker containers using the `docker ps` command:

```bash
docker ps
```

This will list all the currently running containers, showing their container IDs, names, status, ports, and more. If you want to see all containers, including stopped ones, you can use the `-a` flag:

```bash
docker ps -a
```

If you need more detailed information about a specific container, including its logs and resource usage, you can use:

```bash
docker inspect <container_name_or_id>
```

This will provide a detailed JSON output of the container’s configuration and current state.

---

This should give you a good starting point for troubleshooting Docker-related issues, including managing running containers with `docker ps`.




