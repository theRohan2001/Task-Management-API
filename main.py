from fastapi import FastAPI


from routes import auth
from routes import category
from routes import task

from database.db_setup import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API", version="1.0.0")



app.include_router(auth.router)
app.include_router(category.router)
app.include_router(task.router)


