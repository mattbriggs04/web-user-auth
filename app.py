from utils.server import Router, AppServer
from utils.securedb import SecureDB
from utils.sha512 import SHA512
import json

app = AppServer()
router = Router()

def register_user(body: str) -> dict[str, str]:
    data: dict = json.loads(body)
    print("Data given to register_user is", data)
    confirm_password = data.get("confirmPassword")
    password = data.get("password")

    # check passwords
    if data.get("confirmPassword") != data.get("password"):
        return {"status": "error", "errorMsg": "Error: passwords do not match"}
    
    # ensure username not already in database

    # ensure email not already in database

    # add user to database
    return {"status": "ok"}

def index():
    with open("./index.html", 'r') as page:
        page_content = page.read()
    return page_content

def styles():
    with open("./static/styles.css", 'r') as page:
        page_content = page.read()
    return page_content

def script():
    with open("./static/script.js", 'r') as page:
        page_content = page.read()
    return page_content

if __name__ == "__main__":
    # add get routes
    router.add_get_route("/", index)
    router.add_get_route("/index.html", index)
    router.add_get_route("/static/styles.css", styles)
    router.add_get_route("/static/script.js", script)

    # add post routes
    router.add_post_route("/register-user", register_user)

    app.start_server()