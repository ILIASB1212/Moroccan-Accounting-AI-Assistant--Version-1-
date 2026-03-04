# 🇲🇦 Moroccan Accounting AI Assistant
- this is version 1 
## 🎯 Problem Solved
AI-powered assistant for Moroccan accounting standards (CGNC, CGI, Finance Laws)

## ✨ Features
- 🤖 **Multi-Agent RAG System** using LangGraph
- 📚 **5 Specialized Knowledge Bases** (CGNC, CGI, Finance, Plan Comptable, Tax)
- 🔐 **JWT Authentication** with user management
- 💬 **Conversation Memory** with LangGraph checkpoints
- 📄 **Invoice OCR** with Tesseract (French invoices)
- 🛠️ **6 Tools**: CGNC, Finance Law, Tax, Plan Comptable, Web Search, URL Loader
- 🚀 **FastAPI Backend** with proper routing
- 🗄️ **SQLite Database** for users & conversations

## 🏗️ Architecture
- Langgraph workflow archtecture -- see the image in files --

## 🛠️ Tech Stack
- LangChain + LangGraph (Agentic RAG)
- FastAPI (Backend)
- SQLAlchemy + SQLite (Database)
- ChromaDB (Vector stores)
- JWT + OAuth2 (Authentication)
- Tesseract OCR (Invoice processing)
- Docker (Containerization ready)

## 📁 Project Structure
ACCOUNTANT:
├── src/
│   ├── DataBase/         # Database layer
│   ├── router/           # API endpoints
│   ├── auth/             # Authentication
│   ├── data_ingestion/   # RAG pipeline
│   ├── PipeLine/         # Reusable RAG logic
│   └── agent.py          # LangGraph orchestration
├── utils/                 # Tool definitions
├── exception/             # Custom error handling
└── logger/                # Structured logging
│ main.py                  # main api endpoint

## 🚦 Getting Started
- uvicorn main:app --reloaf
