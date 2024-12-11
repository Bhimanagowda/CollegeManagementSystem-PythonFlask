import sys
import os

# Add the parent directory of `api` to sys.path to resolve relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app=create_app()

if __name__=='__main__':
  app.run(debug=True)
