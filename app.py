#from app import app

#if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True)
from app import app

# For gunicorn compatibility
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

