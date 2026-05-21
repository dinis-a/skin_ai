# Skin AI — AI-Powered Skin Tumor Diagnosis Telegram Bot

[![CI](https://github.com/dinis-a/skin_ai/actions/workflows/ci.yml/badge.svg)](https://github.com/dinis-a/skin_ai/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://docs.docker.com/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A Telegram bot that sends user-uploaded skin photographs to a cloud prediction API for diagnosis. The bot classifies images into several diagnostic categories including melanoma, basal cell carcinoma, and benign tumors.

> **Disclaimer:** This is a demo AI model. Diagnoses are not final and do not replace professional medical consultation.

---

## Features

- Accepts skin photographs via Telegram, returns a diagnosis with confidence score in seconds
- Connects to a cloud prediction API for inference (no local GPU/ML dependencies)
- Reply keyboard for quick navigation (FAQ, support, contact)
- Telegram Payments integration for donations
- Newsletter broadcasting to all users (admin-only)
- SQLite persistence for user interaction history
- Dockerized for one-command deployment

---

## Architecture

```
skin_ai/
├── main.py                  # Bot entrypoint (aiogram dispatcher)
├── core/
│   ├── settings.py          # Configuration via env vars (environs)
│   ├── handlers/
│   │   ├── basic.py         # Message handlers + API inference
│   │   └── pay.py           # Telegram Payments handlers
│   ├── keyboards/
│   │   ├── reply.py         # Reply keyboard builder
│   │   └── inline.py        # Inline keyboard builder
│   └── utils/
│       └── commands.py      # Bot command registration
├── assets/                  # Static images
├── tests/                   # Pytest test suite
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── pyproject.toml           # Project metadata + tool config
```

**Pipeline:** User photo → Telegram download → POST to prediction API → diagnosis + confidence → result returned to user.

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- API credentials for the prediction endpoint

### Quick Start

```bash
git clone https://github.com/dinis-a/skin_ai.git
cd skin_ai
cp .env.example .env   # then edit .env with your credentials

# Start with Docker Compose
docker compose up -d
```

### Local Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e ".[dev]"       # installs pytest, ruff
python main.py
```

---

## Running Tests

```bash
pytest tests/ -v
```

## Linting & Formatting

```bash
ruff check .          # lint
ruff format .         # auto-format
```

Pre-commit hooks are configured to run on `git commit`:

```bash
pre-commit install
```

---

## Environment Variables

| Variable     | Description                          |
|-------------|--------------------------------------|
| `BOT_TOKEN` | Telegram bot token                   |
| `ADMIN_ID`  | Telegram user ID for admin           |
| `API_URL`   | Prediction API endpoint              |
| `API_TOKEN` | Bearer token for prediction API      |
| `PAYMENT_PROVIDER_TOKEN` | (optional) Telegram payments provider token |
| `tg_token`  | (optional) Secondary bot token for notifications |
| `tg_chat_id`| (optional) Chat ID for notifications |

---

## Prediction API

The skin diagnosis model is available as a public API — anyone can integrate it into their own projects.

Response example:

```json
{"filename":"medium.png","prediction":"Eczema","recommendations":"The image shows erythematous, scaly patches on the dorsal aspect of both hands. Treatment options may include topical corticosteroids, emollients, and potentially oral medications depending on severity and chronicity. Skin care recommendations include avoiding irritants and allergens, using gentle soaps, and moisturizing regularly.\nDisclaimer: AI info only – not medical advice. Consult a doctor.","is_skin":true,"is_pathology":true}
```

To request an API token, contact [@dinis_n](https://t.me/dinis_n) on Telegram.

---

## CI/CD

GitHub Actions runs linting (ruff) and tests (pytest) on every push and pull request. See [ci.yml](.github/workflows/ci.yml).

---

## License

MIT — see [LICENSE](LICENSE).
