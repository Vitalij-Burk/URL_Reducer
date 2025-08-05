# 🌐 URLReducer

**A blazing-fast, secure, and minimal URL shortener** — with folders, authentication, and Redis caching.

---

URLReducer is a pet project designed to let you securely shorten, organize, and manage your links. Built with modern web technologies and focused on performance, the service is minimal yet powerful under the hood.

> ⚠️ **Warning:** Redis cache updates every 30 seconds. This means recently created or modified links and folders might not appear instantly.

> ⚠️ **Warning:** Redis cache can not to start in docker automatically, if it is so, do it by hands.

---

## 🚀 How It Works

1. 🔐 **User Authentication**
   Sign up or log in with credentials. Passwords are hashed securely.

2. 🧾 **Token System**
   - Short-lived **access token**
   - Long-lived **refresh token**

3. 🔗 **Shorten URLs**
   Submit long URLs and get clean, compact short links.

4. 📁 **Organize into Folders**
   Group your links into folders for easy navigation and management.

---

## ✨ Key Features

- ✅ **Refresh Token Authentication**
  Secure access and refresh token system with rotation.

- 🔐 **Secure Password Storage**
  Passwords are hashed using modern algorithms like `bcrypt` or `argon2`.

- ⚡ **High-Performance Caching with Redis**
  Frequently accessed data is cached in Redis for ultra-fast response times.

- 🗂️ **Folder System for URLs**
  Keep your links organized with folder-based categorization.

- 📦 **Clean & Minimal REST API**
  Easy to use with Postman, scripts, or future frontend applications.

---

## 🛠️ Tech Stack

- **FastAPI** – Modern, high-performance Python web framework
- **PostgreSQL** – Relational database for persistent storage
- **Redis** – In-memory store used for caching
- **SQLAlchemy + Alembic** – ORM with schema migration support
- **JWT** – Token-based user authentication
- **Docker** *(planned)* – Optional containerized deployment

---

## 🧰 Getting Started

Run the following commands to get the app running:

### 1. Start Docker services
- **make docker_up**

### 2. Upgrade alembic
- **make alembic_upgrade**

### 1. Start project
- **make start**

### For more commands and options, see the Makefile ###
