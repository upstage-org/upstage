from werkzeug.middleware.dispatcher import DispatcherMiddleware
from ui import app as frontend
from asset import app as asset 

application = DispatcherMiddleware(frontend, {
    "/asset": asset
})