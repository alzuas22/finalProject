from mycriptos import app

@app.route("/")
def index():
    return "Flask rulando"