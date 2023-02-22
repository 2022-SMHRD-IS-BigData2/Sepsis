from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles   #<-- Add this
import mariadb
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

#static files & load
app.mount("/", StaticFiles(directory="static", html = True), name="static") #<-- Add this