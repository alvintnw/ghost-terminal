# Ghost Terminal AI

Ghost Terminal AI is an interactive, Matrix-themed local AI chat interface powered by **Ollama (Qwen 2.5 7B)** and **Streamlit**. 

![Ghost Terminal Preview](assets/ghost-terminal-preview.png)

## Key Features
- **Local AI Engine**: Powered by `qwen2.5:7b-instruct` running locally via Ollama.
- **Cyberpunk / Matrix UI**: Monospace retro-terminal user interface with customizable theme.
- **Typing Effect**: Real-time typing streaming response simulation.
- **Persistent Memory**: Saves session history locally so context persists across refreshes.
- **Real-Time Health Check**: Live indicator monitoring local Ollama engine connectivity.

## Quick Start

### 1. Prerequisites
- [Ollama](https://ollama.com/) installed and running locally.
- Pull the model:
  ```bash
  ollama pull qwen2.5:7b-instruct
2. Installation
Clone this repository and set up your virtual environment:

Bash
git clone [https://github.com/YOUR_USERNAME/ghost-terminal.git](https://github.com/YOUR_USERNAME/ghost-terminal.git)
cd ghost-terminal

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell

# Install dependencies
pip install -r requirements.txt
3. Run Application
Make sure Ollama is running, then execute:

Bash
streamlit run app.py
Open http://localhost:8501 or http://127.0.0.1:8501 in your browser.

Tech Stack
Frontend: Streamlit (Python Web UI Framework)

Backend / Engine: Ollama (Qwen 2.5 7B Instruct)

Styling: Custom CSS (Retro Terminal Aesthetic)

License
MIT License