from app.server import app

if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False,
        host="localhost",
        port=5000
    )