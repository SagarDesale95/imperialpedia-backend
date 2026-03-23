# Imperialpedia Backend

## 🚀 Live API
Target Domain: https://ir.baalvion.com

Render Default (before custom domain): https://imperialpedia-backend.onrender.com

## 📄 Swagger Docs
https://ir.baalvion.com/docs

Render Default (before custom domain): https://imperialpedia-backend.onrender.com/docs

## 🛠 Tech Stack
- FastAPI
- PostgreSQL (Neon)
- SQLAlchemy
- Alembic

## 📌 Features
- Articles API (CRUD)
- Categories API (CRUD)
- Tags API
- Glossary API
- SEO APIs
- AI Content Generation API

## 🔐 CORS
Enabled for:
- https://ir.baalvion.com
- https://imperialpedia.com

## ✅ Status
All APIs tested and working (Create, Read, Update, Delete)

## ⚙️ Setup
pip install -r requirements.txt
uvicorn app.main:app --reload

## Environment Variables
- `DATABASE_URL`: Neon PostgreSQL connection string (SSL required).
- `OPENAI_API_KEY` (optional): Used by `POST /api/ai/generate`.
- `MOCK_AI`: Set `1` to return mock AI output without calling OpenAI.
- `CORS_ORIGINS`: Comma-separated allowed frontend origins (defaults to `https://ir.baalvion.com,https://imperialpedia.com`).
