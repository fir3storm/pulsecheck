from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import socket
import ssl
import time
import requests
import os
from bs4 import BeautifulSoup

app = FastAPI()

# Static and template setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ✅ Main website health check logic
def check_website_health(url):
    result = {"url": url}

    if not url.startswith("http"):
        url = "http://" + url

    # DNS Resolution
    try:
        hostname = url.split("//")[-1].split("/")[0]
        ip = socket.gethostbyname(hostname)
        result["dns"] = f"Resolved to {ip}"
    except Exception as e:
        result["dns"] = f"Failed: {str(e)}"
        hostname = None

    # HTTP and metadata
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        end = time.time()

        result["http_status"] = response.status_code
        result["response_time"] = f"{round(end - start, 2)}s"
        result["headers"] = dict(response.headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        result["title"] = soup.title.string.strip() if soup.title else "N/A"
        result["redirects"] = [r.url for r in response.history] + [response.url]

    except Exception as e:
        result["http_status"] = f"Error: {str(e)}"
        result["response_time"] = "N/A"
        result["title"] = "N/A"
        result["redirects"] = []
        result["headers"] = {}

    # SSL Certificate check
    try:
        if hostname:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    result["ssl_valid"] = "Valid" if cert else "Invalid"
        else:
            result["ssl_valid"] = "N/A"
    except Exception as e:
        result["ssl_valid"] = f"SSL Error: {str(e)}"

    return result


# ✅ Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.get("/check", response_class=HTMLResponse)
async def check(request: Request, url: str):
    result = check_website_health(url)
    return templates.TemplateResponse("result.html", {"request": request, "result": result})


@app.get("/api/check")
async def api_check(url: str):
    return JSONResponse(content=check_website_health(url))
