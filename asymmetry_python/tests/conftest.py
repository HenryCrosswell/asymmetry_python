import os
import sys

# Get the root directory of your project (where main.py is located)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the root directory to the system path
sys.path.insert(0, root_dir)