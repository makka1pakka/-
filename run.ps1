$ErrorActionPreference = 'Stop'

if (!(Test-Path .env) -and (Test-Path .env.example)) {
    Copy-Item .env.example .env
}

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
