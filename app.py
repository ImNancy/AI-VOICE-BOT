#from app import app

#if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # <-- This allows Render to assign the right port
    app.run(host='0.0.0.0', port=port, debug=True)

