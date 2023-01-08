import uvicorn
from app.main import app
import argparse

parser = argparse.ArgumentParser(description='Web Serve Arguments')

parser.add_argument('--host',type=str,default='localhost')
parser.add_argument('--port',type=int,default=5003)

args = parser.parse_args()

uvicorn.run(app, host=args.host, port=args.port)
