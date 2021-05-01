# DEFINE ENVIRONMENT VARIABLES
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

# STL-IMPORTS
import sys

# LOCAL-IMPORT
from app import App

# PYTHON-MAIN
if __name__ == "__main__":
  App.main(sys.argv)
