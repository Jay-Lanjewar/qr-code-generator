import sys
import os
from streamlit.web import cli as stcli

def resolve_path(path):
    """
    Resolves the path to a resource, supporting both dev (script) and frozen (exe) modes.
    """
    if getattr(sys, 'frozen', False):
        # Portable mode: PyInstaller extracts files to sys._MEIPASS
        basedir = sys._MEIPASS
    else:
        # Dev mode: Use the directory of this script
        basedir = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(basedir, path)

if __name__ == "__main__":
    # We point to app.py which is expected to be in the same folder 
    # (or bundled root) as this launcher.
    app_path = resolve_path("app.py")

    # Set command line arguments for streamlit
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
    ]
    
    # Run streamlit
    sys.exit(stcli.main())
