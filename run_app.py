import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl_config")

from streamlit.runtime import credentials
credentials.check_credentials = lambda: None

import streamlit.web.cli as stcli
import sys

if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        "app.py",
        "--server.headless=true",
        "--server.port=8501",
        "--server.address=0.0.0.0",
    ]
    sys.exit(stcli.main())
