# 🚀 Universal API

A clean, modular, and DX-first FastAPI backend powered by:

-   🧠 FastAPI + SQLAlchemy 2.0 (async) + Pydantic v2
-   🔐 OIDC Auth (Keycloak-ready) with typed request user
-   🗃️ Alembic migrations + PostgreSQL
-   🧪 Pytest + httpx + full DI test scaffolding
-   🛠️ Taskfile-based automation + Poetry + ASDF toolchain
-   📦 Modular architecture with DDD-inspired layering

---

## ⚙️ Tooling Setup

This project uses **ASDF** + **Taskfile** for reproducible environments and DX automation.

### ✅ 1. Install Required Tools

```bash
brew install asdf
brew install go-task/tap/go-task
```

Add plugins declared in `.tool-versions`:

```bash
asdf plugin add python
asdf plugin add poetry
asdf plugin add golang
asdf plugin add rust
```

Install them:

```bash
asdf install
```

---

## 🛠️ Project Setup

Install Python dependencies:

```bash
task install
```

Initialize the DB (via Alembic):

```bash
task migrate
```

---

## 🧪 Local Development

Run the API with live reload:

```bash
task run:dev
```

Or production mode:

```bash
task run:api
```

---

## 📁 Folder Structure

```shell
.
├── src/app/
│   ├── api/             # FastAPI routers
│   ├── auth/            # Keycloak OIDC + user mapping
│   ├── core/            # Logging, config, startup logic
│   ├── db/              # SQLAlchemy entities, session config
│   ├── domain/          # Domain models + repo interfaces
│   ├── infrastructure/  # Repositories, DAOs
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Service layer
│   └── main.py          # FastAPI entrypoint
├── migrations/          # Alembic migrations
├── Taskfile.yml         # DX automation
├── .tool-versions       # ASDF toolchain declaration
├── pyproject.toml       # Poetry + config
```

---

## 🧪 Testing

Use Pytest + anyio + httpx:

```bash
task test              # All tests
task test:messages:api # Scoped to messages API
```

---

## 🧼 Code Quality

```bash
task lint        # ruff, mypy, black
task format      # Auto-format with black + isort
task typecheck   # Static type check
task test        # Full test suite
```

---

## 🔐 Authentication

-   Uses `OIDCUser` injected via `Depends(map_oidc_user)`
-   Keycloak-ready with optional mocked test user override
-   Fine-grained role checks per route (e.g., `admin` guard for list endpoints)

---

## 📌 License

MIT ©
