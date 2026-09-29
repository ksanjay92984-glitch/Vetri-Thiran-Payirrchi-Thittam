# PocketSmart AI

A FastAPI + Jinja2 + SQLite + Gemini-based budget recommendation assistant for:
- Home interior planning
- Party planning
- Jewelry recommendations with optional outfit image

## 1. VS Code setup

Install Python 3.11+ and open this folder in VS Code.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and add your Gemini API key.

## 2. Run

```powershell
python -m uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000

API docs:

http://127.0.0.1:8000/docs

## 3. Test

1. Register an account.
2. Open Planner.
3. Try Home, Party and Jewelry.
4. Upload an outfit image in Jewelry if desired.
5. Open History.

If `GEMINI_API_KEY` is empty, the app still runs with deterministic fallback recommendations. This is useful for testing the UI and API before configuring Gemini.

## 4. Gemini configuration

The documentation supplied for this project describes Gemini 1.5 Flash Pro. The code keeps the model name configurable through `GEMINI_MODEL`, so set the exact model available to your Google account there.

Do not commit `.env` or your API key to GitHub.

## 5. Architecture

```text
Browser
  |
  v
Jinja2 + HTML/CSS/JS
  |
  v
FastAPI
  |-- Auth/JWT
  |-- Planner routes
  |-- History
  |
  v
Gemini service
  |
  +-- Gemini API
  |
  +-- Fallback recommendation logic
  |
  v
SQLite
```

## Notes

The documentation mentions Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO as sources. This starter implementation labels platforms in recommendations but does not scrape or claim live inventory/prices. Real product/vendor integrations should be added through official APIs or permitted affiliate/search APIs.
