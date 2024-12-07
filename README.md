## LLM Chatbot

## Description

This repository contains the code for the Langchain and LlamaIndex chatbots, which utilize natural language to SQL processing with Langchain and LLamaIndex using OpenAI GPT-3.5 Turbo LLM engine. The data source for these chatbots is IPEDS (Integrated Postsecondary Education Data System).

### IPEDS (Integrated Postsecondary Education Data System)

IPEDS is a comprehensive data source maintained by the National Center for Education Statistics (NCES), which collects data from all primary providers of postsecondary education in the United States. It covers various aspects of postsecondary education, including enrollment, graduation rates, financial aid, institutional characteristics, and more.

## Getting Started

Follow these instructions to get the project up and running on your local machine. 

### Prerequisites


Make sure you have Python 3.11 installed on your system. For MacOS Go to https://www.python.org/downloads/macos/ and download Python 3.11.8 - Feb. 6, 2024 Download macOS 64-bit universal2 installer


### 1. Installing Git using Homebrew

Open Terminal on Mac and install Homebrew using the command line below

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Install Git using the command line below 

```bash
brew install git
```

Check if Git installation is successful

```bash
git --version
```

### 2. Installing VSCode (Visual Studio Code)
Download VSCode from the website: https://code.visualstudio.com 

### 3. Cloning the Repository

Launch VSCode, press (Shift+Command+P) and type the following command
to clone the repository 


```bash
git clone https://github.com/hemadataworksai/ipedsllm.git
```

### 4. Setting up a Virtual Environment

### * Add how to access the Virtual env after its created.

#### Windows

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

#### macOS/Linux

```bash
# Create a virtual environment
python3.11 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 5. Installing Requirements

Install the project dependencies using pip:

```bash
pip install -r requirements.txt
```

### 6. Creating `.env` File

Go to IPEDSLLM project and create `.env` file in the root directory of the project and save the following details:

```
DB_URL = <YOUR_DB_URL>
OPENAI_API_KEY = <YOUR_OPENAI_API_KEY>
LANGCHAIN_TRACING_V2 = <YOUR_LANGCHAIN_TRACING_V2_SETTING>
LANGCHAIN_API_KEY = <YOUR_LANGCHAIN_API_KEY>
```

Replace `YOUR_DB_URL` with appropraite values. 
Replace `YOUR_OPENAI_API_KEY` and `YOUR_LANGCHAIN_API_KEY` with keys as below.

#### Creating API keys (fees required)

To create OPENAI_API_KEY, go to: https://platform.openai.com/usage

create an account and purchase tokens starting with minimum credit. 
From Usage > Increase limit > Billing > Add to credit balance > Profile > User_API_keys 
and then copy & paste the key to .env file.

To create LANGCHAIN_API_KEY, go to: https://smith.langchain.com/

From Settings > API_keys > Create API_keys and then copy & paste the key
to .env file. 


### 5. Running the Chatbots

To run the Langchain chatbot with Streamlit, use the following command:

```bash
streamlit run src/langchain_chatbot/components/main.py
```

To run the LlamaIndex chatbot with Streamlit, use the following command:

```bash
streamlit run src/llamaIndex_chat/components/main.py
```
#### The embedded model: 

You can download the embedded model from: https://drive.google.com/drive/folders/18v-9ts2KdGxEmZ3hg0BSxvsC3-f6HWZb?usp=drive_link
