import sys
import os

# Adds the src directory to sys.path so that tests can import modules from it
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))
