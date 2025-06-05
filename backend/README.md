# Uni-One Backend

This backend uses FastAPI for the Uni-One social networking app. It provides
basic user registration, JWT authentication, post management, group creation,
and WebSocket chat.

## Development

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the API (set the `SECRET_KEY` environment variable first):

```bash
uvicorn main:app --reload
```
