# Uni-One

This repository contains a minimal prototype for the Uni-One social networking
app. The goal is to promote cultural exchange, collaboration, and unity among
African youth.

## Structure

- `backend`: FastAPI application with JWT auth, posting, groups, WebSocket chat,
  and a simple AI-powered caption generator using HuggingFace transformers.
- `frontend`: Minimal React application that displays posts from the backend.
- `streamlit_app.py`: Simple Streamlit interface for interacting with the backend.

## Running Locally

1. Start the backend (see `backend/README.md`). Set `SECRET_KEY` in your
   environment to secure JWT tokens.
2. Start the frontend (see `frontend/README.md`).
3. Run the Streamlit demo from the project root:
   `streamlit run streamlit_app.py` or `python -m streamlit run streamlit_app.py`
   after installing dependencies from `streamlit_requirements.txt`.

This project is highly experimental and only demonstrates a few features of the
planned platform.
