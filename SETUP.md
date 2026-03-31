# 🚀 NeuralHire — Setup Guide

Follow these steps exactly to get NeuralHire running on your machine.

---

## ✅ Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Python | **3.11 only** | https://www.python.org/downloads/release/python-3119/ |
| Pinecone Account | Free tier | https://pinecone.io |

> ⚠️ **Python 3.12 and 3.13 will NOT work.** ML packages (numpy, sentence-transformers) require Python 3.11.

---

## Step 1 — Get a Pinecone API Key

1. Go to **https://pinecone.io** → Sign Up (free)
2. Dashboard → click **API Keys**
3. Copy your API key — you'll need it in Step 3

---

## Step 2 — Install Python 3.11

1. Download: https://www.python.org/downloads/release/python-3119/
2. Run the installer
3. ✅ **Check "Add Python to PATH"** during install
4. Verify in CMD/PowerShell:
```bash
py -3.11 --version
# Should show: Python 3.11.x
```

---

## Step 3 — Setup Backend

Open **PowerShell** or **Command Prompt** (NOT Git Bash):

```powershell
cd path\to\neuralhire\backend
```

Create a virtual environment with Python 3.11:
```powershell
py -3.11 -m venv venv
```

Activate it:
```powershell
venv\Scripts\activate
```
> You should see `(venv)` at the start of your terminal line.

Install all packages:
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Step 4 — Configure Environment

Create your `.env` file:
```powershell
copy .env.example .env
```

Open `.env` in Notepad (or VS Code) and replace with your values:
```
PINECONE_API_KEY=paste-your-pinecone-key-here
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX_NAME=neuralhire-candidates
DEBUG=false
SECRET_KEY=any-random-string-here
EMBEDDING_MODEL=all-MiniLM-L6-v2
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

> ⚠️ Make sure the file is saved as `.env` not `.env.txt`

---

## Step 5 — Seed Sample Candidates

This uploads 6 sample candidate profiles to your Pinecone index:
```powershell
python seed_candidates.py
```

You only need to do this **once**.

---

## Step 6 — Start the Backend

```powershell
uvicorn app.main:app --reload --port 8000
```

Wait for this message:
```
INFO: Uvicorn running on http://127.0.0.1:8000
```

**Leave this terminal open.** The backend must stay running.

---

## Step 7 — Open the Frontend

1. Open **File Explorer**
2. Navigate to `neuralhire\frontend\public\`
3. **Double-click `index.html`**

It opens in your browser. That's it! ✅

---

## ✅ It's Working When...

- Frontend loads with a dark-themed dashboard
- You can see a job description in the left panel
- Clicking **Analyse & Match** returns ranked candidates with scores
- API docs work at: http://127.0.0.1:8000/api/docs

---

## 🔁 Every Time You Want to Start Again

```powershell
cd neuralhire\backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Then double-click `frontend\public\index.html`. Done!

---

## 🛑 To Stop Everything

In the backend terminal:
```
Ctrl + C
deactivate
```

Close the browser tab.

---

## ❓ Common Errors

| Error | Fix |
|-------|-----|
| `metadata-generation-failed` for numpy | You're using Python 3.12/3.13 — must use 3.11 |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` with venv activated |
| `ValidationError for Settings` | Your `.env` file has typos — check variable names |
| `Unable to connect` in browser | Backend is not running — start uvicorn first |
| Frontend is blank | Don't open via Live Server — double-click the file directly |
| Pinecone connection error | Check your `PINECONE_API_KEY` in `.env` |
