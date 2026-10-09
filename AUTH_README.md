# FlyRank Auth API — Supabase + FastAPI + JWT

A secure authentication API built with **Python + FastAPI** and **Supabase Auth**, using **JWT Bearer Tokens** to protect routes.

---

## Setup

### 1. Create a Supabase project
Go to [supabase.com](https://supabase.com), create a project, and get your keys from **Project Settings → API**.

### 2. Set up environment variables
```bash
cp .env.example .env
```
Edit `.env` and fill in your Supabase credentials:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 3. Install dependencies & run
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run_auth.py
```

Server starts at `http://localhost:8000`.
Swagger UI at `http://localhost:8000/docs`.

---

## API Reference

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| GET | `/public/info` | ❌ No | Public info, no token needed |
| POST | `/auth/signup` | ❌ No | Register a new user |
| POST | `/auth/login` | ❌ No | Login, returns JWT token |
| POST | `/auth/logout` | ✅ Bearer Token | Terminate session |
| GET | `/protected/profile` | ✅ Bearer Token | View user profile |
| GET | `/protected/dashboard` | ✅ Bearer Token | View user dashboard |

---

## Status Codes

| Code | Meaning |
|---|---|
| 200 | Success |
| 201 | User created (signup) |
| 204 | Logout successful (no content) |
| 400 | Missing/invalid input |
| 401 | Missing, invalid, or expired token |

---

## How to Test

### 1. Sign up
```bash
curl -i -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### 2. Log in (copy the access_token from the response)
```bash
curl -i -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### 3. Access protected route
```bash
curl -i http://localhost:8000/protected/profile \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

---

## Swagger UI

Click the **🔒 Authorize** button in Swagger UI, paste your JWT token, and use **"Try it out"** on any protected route.

*(Add Swagger screenshot here)*

---

## Security Notes
- `.env` is gitignored — your Supabase keys are never committed to GitHub.
- Token verification is handled by Supabase via `supabase.auth.get_user(token)`.
- Auth check is extracted into a reusable FastAPI **Dependency** (`get_current_user`) applied to all protected routes.
