from utils import server
from utils.server import Router, AppServer

app = AppServer()
router = Router()

def index():
    with open("./templates/index.html", 'r') as page:
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
    # add routes
    router.add_get_route("/", index)
    router.add_get_route("/index.html", index)
    router.add_get_route("/static/styles.css", styles)
    router.add_get_route("/static/script.js", script)
    app.start_server()