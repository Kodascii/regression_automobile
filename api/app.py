from fastapi import FastAPI

app = FastAPI()

# Define a simple endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Define an endpoint with path parameters
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# Define an endpoint that accepts POST requests
@app.post("/items/")
def create_item(item: dict):
    return item