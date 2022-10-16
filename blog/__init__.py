from flask import Flask

app = Flask(__name__)
app.secret_key = "6414"


from blog import routes
