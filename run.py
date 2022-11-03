from blog import app, db
from blog.models import User, PresPost, Wpost


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Pres": PresPost, "Webeee": Wpost}
    #Così non serve che importi sempre Post e User in flask shell
