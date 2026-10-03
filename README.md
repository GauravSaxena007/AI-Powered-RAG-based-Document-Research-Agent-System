# 🧠 G-Mind AI

**AI-Powered RAG-based Document Research Agent System**

G-Mind AI is an AI-powered document assistant that allows users to upload PDF documents and ask questions about them. The system uses **RAG (Retrieval-Augmented Generation)** to retrieve relevant information from documents and an **LLM** to generate answers.

It also includes an AI agent that can decide whether to retrieve information from the document or use available tools.

---

## 🚀 Features

- 📄 Upload PDF documents
- 🔍 RAG-based document search
- 💬 Chat with your documents
- 🤖 AI agent using LangGraph
- 🔗 LangChain integration
- 🧠 LLM-powered answers
- 🗄️ Vector database for document embeddings
- 🔧 MCP tools
- ⚡ Async FastAPI backend
- 🌐 REST APIs
- 🐳 Docker-ready
- ☸️ Kubernetes-ready
- ☁️ Cloud deployment-ready

---

## 🛠️ Tech Stack

### Frontend
- React
- Vite
- JavaScript

### Backend
- Python
- FastAPI
- AsyncIO

### AI
- LLM
- LangChain
- LangGraph
- RAG
- Embeddings

### Database
- ChromaDB / Vector Database

### Infrastructure
- Docker
- Kubernetes
- Linux
- Cloud

### Tools
- MCP (Model Context Protocol)

---

## 📂 Project Structure

```text
G-mind-ai/
│
├── backend/
│   ├── app/
│   ├── .venv/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

# ⚙️ Installation & Setup

## 1. Clone the repository

```bash
git clone https://github.com/GauravSaxena007/AI-Powered-RAG-based-Document-Research-Agent-System.git
```

Move into the project directory:

```bash
cd G-mind-ai
```

---

# 🐍 Backend Setup

Open a terminal and run:

```powershell
cd G-mind-ai\backend
```

Activate the Python virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start the FastAPI development server:

```powershell
uvicorn app.main:app --reload
```

Backend will run on:

```text
http://127.0.0.1:8000
```

FastAPI API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# ⚛️ Frontend Setup

Open **another terminal**.

Move to the frontend:

```powershell
cd G-mind\frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend will normally run on:

```text
http://localhost:5173
```

---

# 🔑 Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
OPENAI_API_KEY=your_api_key_here
```

Never commit your `.env` file to GitHub.

Use `.env.example` for documenting required environment variables.

---

# 🔄 How It Works

```text
              User
                │
                ▼
         React Frontend
                │
                ▼
          FastAPI REST API
                │
                ▼
        LangGraph AI Agent
           /          \
          /            \
         ▼              ▼
       RAG             MCP Tools
        │
        ▼
   Vector Database
        │
        ▼
      Documents
        │
        ▼
       LLM
        │
        ▼
      Answer
```

### Document Flow

```text
PDF
 ↓
Text Extraction
 ↓
Text Chunking
 ↓
Embeddings
 ↓
Vector Database
 ↓
Semantic Search
 ↓
Relevant Context
 ↓
LLM
 ↓
Answer + Sources
```

---

# 🤖 AI Agent

G-Mind AI uses **LangGraph** to create an agent workflow.

The agent determines how to handle a user's question.

For example:

```text
"What is the revenue mentioned in the PDF?"
                ↓
             RAG Search
                ↓
          Relevant Chunks
                ↓
               LLM
                ↓
             Answer
```

For a tool-based question:

```text
"What is 125 × 48?"
          ↓
      AI Agent
          ↓
    Calculator Tool
          ↓
         6000
```

---

# 🔌 MCP Tools

The project demonstrates MCP (Model Context Protocol) integration.

Example tools include:

- Calculator
- Current date/time

The AI agent can use these tools when required.

---

# 📡 API

Main backend endpoints:

```text
GET  /api/health
POST /api/documents/upload
POST /api/chat
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

# 🐳 Docker

Build and run the project using Docker Compose:

```bash
docker compose up --build
```

Stop containers:

```bash
docker compose down
```

---

# ☸️ Kubernetes

Kubernetes configuration is available in the `k8s/` directory.

Example:

```bash
kubectl apply -f k8s/
```

Check deployments:

```bash
kubectl get deployments
```

Check services:

```bash
kubectl get services
```

---

# 🎯 Purpose of the Project

The main purpose of G-Mind AI is to demonstrate practical **AI Engineering** skills by combining modern LLM application technologies into one working project.

The project demonstrates:

- LLM integration
- Retrieval-Augmented Generation
- Vector search
- LangChain
- LangGraph
- MCP
- Python
- FastAPI
- REST APIs
- AsyncIO
- Docker
- Kubernetes
- Linux
- Cloud deployment concepts

---

# 💡 Example Questions

After uploading a PDF, try asking:

```text
What is this document about?

Summarize the main points.

What are the key findings?

What does the document say about [topic]?

What are the important numbers mentioned in the document?
```

Tool examples:

```text
What is 125 * 48?

What is today's date?
```

---

# 👨‍💻 Author

**Gaurav Saxena**

MERN Stack Developer | AI Engineering Enthusiast

GitHub:  
https://github.com/GauravSaxena007
