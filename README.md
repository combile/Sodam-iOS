# SODAM Backend (Fixed, No Circular Import)

A minimal Flask backend with auth and recommendation endpoints.

## Run (macOS/Linux)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# set PYTHONPATH to project root if needed
export PYTHONPATH=$(pwd)

# initialize DB (SQLite)
flask --app backend.wsgi db init
flask --app backend.wsgi db migrate -m "init"
flask --app backend.wsgi db upgrade

# run
flask --app backend.wsgi run -p 5000 --debug
```

### Endpoints
- `GET /api/v1/health`
- `POST /api/v1/auth/register` — body: `{ "email": "...", "password": "...", "name": "..." }`
- `POST /api/v1/auth/login` — body: `{ "email": "...", "password": "..." }`
- `POST /api/v1/recs/score` — body: `{ "features": { "foot_traffic": 0.7, ... } }`
- `GET  /api/v1/recs/sample`

### Notes
- JWT/DB are wired; default DB is `sqlite:///app.db`.
- The scoring function lives in `backend/services/scoring.py`; blueprints import from there, avoiding circular imports.
