import threading
import click


from main import app
from cli.user.commands import cmd

def run_app():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)

if __name__ == "__main__":
    uvicorn_thread = threading.Thread(target=run_app, daemon=True)
    uvicorn_thread.start()
    cmd()
