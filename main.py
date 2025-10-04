from fastapi import FastAPI, HTTPException, Depends


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

