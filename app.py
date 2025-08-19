from utils.server import Router, AppServer
from utils.securedb import SecureDB
import json

app = AppServer()
router = Router()
db_manager = SecureDB(db_path="users.db", hash_alg="sha512")

def login_user(body: str) -> dict[str, str]:
    data: dict = json.loads(body)
    print("Data given to login_user is", data)

    if not {"username", "password"}.issubset(data.keys()):
        return {"status": "error", "errorMsg": "Error: missing required information"}
    username = data["username"]
    password = data["password"]

    res = db_manager.check_credentials(username, password)
    if not res:
        return {"status": "error", "errorMsg": "Error: invalid username or password"}

    return {"status": "ok"}

def register_user(body: str) -> dict[str, str]:
    data: dict = json.loads(body)
    print("Data given to register_user is", data)

    if not {"email", "username", "password", "confirmPassword"}.issubset(data.keys()):
        return {"status": "error", "errorMsg": "Error: missing required information"}
    email = data["email"]
    username = data["username"]
    password = data["password"]
    confirm_password = data["confirmPassword"]

    # check passwords
    if confirm_password != password:
        return {"status": "error", "errorMsg": "Error: passwords do not match"}
    
    # add user to database
    res = db_manager.add_user(email, username, password)
    if res is not None:
        return {"status": "error", "errorMsg": res}
    
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
    router.add_post_route("/login-user", login_user)
    app.start_server()