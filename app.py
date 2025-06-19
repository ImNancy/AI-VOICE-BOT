from app import app  # assuming your FastAPI app is in app.py

# For gunicorn or uvicorn
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port= 5000, reload=True)
