# AI Assistant Chatbot Application

A simple, modern, full-stack chatbot application built with **FastAPI** (Python) on the backend and **vanilla HTML, CSS, and JavaScript** on the frontend.

---

## 📁 Project Structure

```text
chatbot-app/
├── backend/
│   ├── main.py              # FastAPI application with CORS & chat endpoint
│   └── requirements.txt     # Backend Python dependencies
├── frontend/
│   ├── index.html           # Semantic, responsive chatbot markup
│   ├── style.css            # Custom CSS with responsive & modern design
│   └── script.js            # Dynamic DOM manipulation & fetch API integration
└── README.md                # Documentation & setup guide
```

---

## 🚀 Getting Started

### 1. Backend Setup (FastAPI)

1. Open a terminal and navigate to the `backend/` directory:

   ```bash
   cd chatbot-app/backend
   ```

2. (Optional but recommended) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   source venv/Scripts/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   _(Or with `uv`: `uv pip install -r requirements.txt`)_

4. Start the FastAPI development server:

   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. The backend API is now running at:
   - Base URL: `http://localhost:8000`
   - Interactive Swagger Docs: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/api/health`

---

### 2. Frontend Setup

The frontend uses zero external frameworks or build tools. You can run it directly:

- **Option A (Direct in Browser):** Simply double-click `frontend/index.html` to open it in any web browser.
- **Option B (Local HTTP Server):**
  ```bash
  cd chatbot-app/frontend
  python -m http.server 3000
  ```
  Then visit `http://localhost:3000` in your browser.

---

## 📡 API Specification

### Chatbot Endpoint

- **Method**: `POST`
- **URL**: `http://localhost:8000/api/chat`
- **Headers**: `Content-Type: application/json`

#### Request Body

```json
{
  "message": "Hello"
}
```

#### Response Body

```json
{
  "response": "Hello! How can I help you?"
}
```

#### Dummy Response Rules:

- `"hello"` → `"Hello! How can I help you?"`
- `"hi"` → `"Hi there! 👋"`
- `"how are you"` → `"I'm doing great! How can I help you today?"`
- Unknown message → `"This is a dummy chatbot response. AI integration can be added later."`

---

## ✨ Features

- **Pydantic Validation**: Ensures non-empty messages and validates length on the backend.
- **CORS Configured**: Seamless frontend-backend cross-origin requests.
- **Dynamic Messaging**: All messages rendered via JavaScript DOM APIs without hardcoded chat history.
- **Typing Indicator**: Shows an animated bouncing typing indicator while waiting for the server.
- **Error Handling**: Graceful network failure detection with clear notifications.
- **Mobile Responsive**: Adapts smoothly to mobile screens (full height/width) and desktop screens (centered card view).
