import pathlib
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi import FastAPI, Request
from utils.log_wrapper import LogWrapper


def mount_resources_for_testing_page(app: FastAPI, logger: LogWrapper):
    root_dir = pathlib.Path(__file__).parent.parent.resolve()

    try:
        static_route = str(root_dir / "static")
        app.mount("/static", StaticFiles(directory=static_route), name="static")
        logger.info("Mounted static file directory.")
    except RuntimeError as e:
        logger.warning(f"Could not mount static directory 'static'. Ensure it exists: {e}")

    # --- Setup Jinja2 Templates ---
    try:
        templates_route = str(root_dir / "templates")
        templates = Jinja2Templates(directory=templates_route)
        logger.info("Initialized Jinja2Templates.")
    except Exception as e:  # Jinja2 might raise different errors
        logger.error(f"Could not initialize Jinja2Templates. Ensure 'templates' directory exists: {e}")

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)  # Exclude from OpenAPI docs
    async def read_root(request: Request):
        """Serves the main HTML index page."""
        logger.info("Serving root HTML page.")
        try:
            return templates.TemplateResponse("index.html", {"request": request})
        except Exception as e:
            logger.error(f"Error rendering index.html template: {e}")
            # Return a simple error response if template fails
            return HTMLResponse(
                "<html><body><h1>Internal Server Error</h1><p>Could not load template.</p></body></html>",
                status_code=500)