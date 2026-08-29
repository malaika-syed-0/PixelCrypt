# PixelCrypt

A Flask web application that encrypts secret messages with Fernet and hides the encrypted text inside PNG images using LSB steganography.

## Features
- User registration and login
- Bcrypt password hashing
- Fernet message encryption/decryption
- LSB image steganography
- Encode/decode history in SQLite
- Encoded image download

## Local Setup (Windows)

1. Install Python.
2. Open this folder in VS Code.
3. Create a virtual environment:
   `python -m venv venv`
4. Activate it:
   `venv\\Scripts\\Activate.ps1`
5. Install dependencies:
   `pip install -r requirements.txt`
6. Run:
   `python app.py`
7. Open the local URL shown by Flask.

The SQLite database (`users.db`) is created automatically on first run.

## Deployment

Use a production WSGI server (the included Procfile uses Gunicorn):
`gunicorn app:app`

Set a strong `SECRET_KEY` environment variable on the hosting provider. Do not commit `users.db`, `.env`, passwords, or real secret keys.

The `uploads/` and `outputs/` folders are runtime directories. The repository keeps only `.gitkeep` files so the folders exist after cloning.

## Note

The current LSB implementation is intended for PNG images. Image processing such as resizing, recompression, or format conversion can affect the hidden data.
