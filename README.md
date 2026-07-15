# 🤖 Sentinel AI

**Sentinel AI** is a production-oriented AI assistant built with **FastAPI**, **LangGraph**, and **Large Language Models (LLMs)**. It integrates with **WhatsApp Cloud API** to provide intelligent conversations, document analysis, spreadsheet insights, image understanding, voice transcription, internet search, and persistent memory.

Designed with modularity and scalability in mind, Sentinel AI combines modern AI orchestration with production-ready backend engineering, making it suitable for business automation, customer support, productivity, and intelligent personal assistance.

---

# ✨ Features

* 🤖 AI-powered conversational assistant
* 💬 WhatsApp Cloud API integration
* 🧠 Persistent user memory using PostgreSQL
* 🔒 User authorization and access control
* 🚫 Duplicate webhook detection
* 🌐 Internet search integration
* 📄 PDF document analysis
* 📊 Spreadsheet analysis and insights
* 🖼️ Image understanding
* 🎤 Audio transcription and conversation
* 📝 Structured application logging
* ⚡ LangGraph agent workflow
* 💾 Conversation persistence
* 🔄 Multi-session support
* 🧩 Modular architecture for future expansion

---

# 🏗 Architecture

```text
WhatsApp User
       │
       ▼
Meta WhatsApp Cloud API
       │
       ▼
FastAPI Webhook
       │
       ▼
Authorization
       │
       ▼
Duplicate Detection
       │
       ▼
Sentinel Agent (LangGraph)
       │
 ┌─────┼────────────┬───────────────┐
 │     │            │               │
 ▼     ▼            ▼               ▼
Memory Search   Internet Search   AI Models   External Services
 │                                  │
 ▼                                  ▼
Supabase PostgreSQL         Groq / Gemini
       │
       ▼
WhatsApp Response
```

---

# 🚀 Current Capabilities

### Conversational AI

* Context-aware conversations
* Multi-turn dialogue
* Session-based memory
* Personalized responses

### Document Intelligence

* PDF parsing
* Document summarization
* Question answering from uploaded PDFs

### Spreadsheet Intelligence

* CSV/XLS/XLSX support
* Automatic dataset profiling
* Descriptive statistics
* Missing value analysis
* AI-generated insights and recommendations

### Audio Intelligence

* Voice message transcription
* AI responses from speech

### Image Processing

* Image download and processing
* Vision model integration (Gemini)

### Search

* Real-time web search
* AI-assisted search summarization

---

# 🛠 Technology Stack

| Category         | Technology                      |
| ---------------- | ------------------------------- |
| Backend          | FastAPI                         |
| AI Orchestration | LangGraph                       |
| LLM Framework    | LangChain                       |
| Models           | Groq (Llama 3.3), Google Gemini |
| Database         | PostgreSQL (Supabase)           |
| ORM              | SQLAlchemy                      |
| Messaging        | WhatsApp Cloud API              |
| Search           | Tavily Search                   |
| Speech           | Whisper                         |
| Documents        | PyMuPDF                         |
| Data Analysis    | Pandas                          |
| Logging          | Loguru                          |
| Deployment       | Railway (planned)               |

---

# 📁 Project Structure

```text
Sentinel-ai/
│
├── app/
│   ├── agents/
│   ├── config/
│   ├── database/
│   ├── memory/
│   ├── prompts/
│   ├── security/
│   ├── services/
│   ├── utils/
│   ├── whatsapp/
│   └── main.py
│
├── logs/
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Sentinel-ai.git

cd Sentinel-ai
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
APP_NAME=

LLM_PROVIDER=
LLM_API_KEY=
LLM_MODEL=
LLM_BASE_URL=

GEMINI_API_KEY=
GEMINI_TEXT_MODEL=
GEMINI_VISION_MODEL=

TAVILY_API_KEY=

DATABASE_URL=

WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_VERIFY_TOKEN=
META_APP_SECRET=

EMAIL_ADDRESS=
EMAIL_APP_PASSWORD=

ALLOWED_USERS=

CREATOR_NAME=
CREATOR_TITLE=
```

---

# ▶ Running Sentinel AI

Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

Expose your local server (development)

```bash
ngrok http 8000
```

Configure the generated HTTPS URL as the Meta WhatsApp webhook.

---

# 💾 Database

Sentinel AI uses **Supabase PostgreSQL** for persistent storage.

Current tables include:

* Users
* Memories
* Processed Messages

These enable:

* User management
* Conversation memory
* Duplicate webhook prevention

---

# 🔒 Security

* Authorized user whitelist
* Duplicate webhook detection
* Environment-based secrets management
* Modular security layer
* Production-ready logging

---

# 🤝 Contributing

Contributions, suggestions, and feature requests are welcome.

If you find a bug or have an idea for improvement, feel free to open an issue or submit a pull request.

---
---

# 👨‍💻 Author

**Badawi Aminu Muhammed**

AI/ML Engineer • Data Scientist • Research Analyst

Sentinel AI demonstrates the integration of modern AI agents, backend engineering, cloud databases, and conversational interfaces into a production-oriented intelligent assistant.
