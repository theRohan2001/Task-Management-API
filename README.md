# Task-Management-API

A comprehensive REST API for managing tasks with user authentication, categories, and filtering capabilities. Built with FastAPI, SQLAlchemy, and JWT authentication.

## Tech Stack
 __FastAPI  
 SQLite  
 SQLAlchemy ORM  
 Authentication: JWT (JSON Web Tokens)  
 Password Hashing:  bcrypt via passlib  
 Validation:  Pydantic v2  
 Testing:  pytest with coverage  
 Server:  Uvicorn (ASGI server)__  

## Docker Installation

### 1. Clone the repository  
### 2. Build the Docker image  

```bash
docker build -t task-management-api .
```
### 3. Run the container  
```bash
docker run -p 8000:80 task-management-api
```
### 4. Go to this URL to interact with the API:  
[localhost](http://localhost:8000/docs) 

## Features to add in future:
__1. Add database migrations( using Alembic)  
2. Deploy the codebase to a cloud platform__


