# PixelCrypt

PixelCrypt is a Flask-based secure message-hiding application that combines
Fernet encryption with LSB image steganography.

It encrypts a secret message first and then hides the encrypted data inside
a PNG image. This provides two layers of protection:

- Encryption protects the message content.
- Steganography hides the existence of the message.

## Features

- User registration and login
- Bcrypt password hashing
- Session-based authentication
- Fernet message encryption/decryption
- LSB image steganography
- PNG encoded-image generation
- Encode/decode history using SQLite
- Encoded image download
- Responsive web interface

## How It Works

### Encoding

1. User selects a PNG/image.
2. User enters a secret message and encryption password.
3. PixelCrypt generates a Fernet key from the password.
4. The message is encrypted using Fernet.
5. The encrypted message is hidden inside the image using LSB steganography.
6. A new encoded PNG is generated.
7. The user downloads the encoded image.

### Decoding

1. User uploads the encoded PNG.
2. PixelCrypt extracts the hidden encrypted message using LSB.
3. The user enters the encryption password.
4. Fernet attempts to decrypt the extracted data.
5. If the password is correct and the image has not been damaged,
   the original message is recovered.

## Project Structure

PixelCrypt/
├── app.py
├── crypto_engine.py
├── stego_engine.py
├── database.py
├── requirements.txt
├── Procfile
├── templates/
├── static/
├── uploads/
└── outputs/

## Local Setup

### 1. Clone the repository

git clone https://github.com/malaika-syed-0/PixelCrypt.git

### 2. Open the project

cd PixelCrypt

### 3. Create a virtual environment

python -m venv venv

### 4. Activate the environment

Windows PowerShell:

venv\Scripts\Activate.ps1

### 5. Install dependencies

pip install -r requirements.txt

### 6. Run the application

python app.py

### 7. Open the local application

Open the URL displayed by Flask, usually:

http://127.0.0.1:5000

## Database

PixelCrypt uses SQLite.

The users database is created automatically when the application
starts for the first time.

Each installation creates its own local database.

## Security

- User passwords are stored using Bcrypt hashing.
- Secret messages are encrypted using Fernet.
- Flask sessions are protected using a SECRET_KEY.
- The encryption password is not stored in the database.

## Image Compatibility

The current steganography implementation is designed primarily for PNG
images.

Image transformations such as:

- JPEG conversion
- resizing
- recompression
- editing
- some social-media processing

can modify pixel data and may destroy the hidden message.

For reliable recovery, use the original encoded PNG without modifying it.

## Deployment

The included Procfile uses Gunicorn:

gunicorn app:app

When deploying, configure a strong SECRET_KEY as an environment variable.

Do not commit:

- .env
- users.db
- passwords
- real secret keys
- personal uploaded images

## Technologies

- Python
- Flask
- SQLite
- Flask-Bcrypt
- Cryptography / Fernet
- Stegano / LSB
- HTML
- CSS
- JavaScript

## Project Purpose

PixelCrypt demonstrates how cryptography and steganography can be combined
to provide both confidentiality and information hiding in a web application.