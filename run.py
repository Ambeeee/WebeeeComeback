from blog import app, db
from blog.models import User, Post


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Post": Post}
    #Così non serve che importi sempre Post e User in flask shell
