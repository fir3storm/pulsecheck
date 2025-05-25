# PulseCheck - Website Health Checker

**PulseCheck** is a lightweight, professional-grade website health check tool built using **FastAPI**. It helps you quickly diagnose the status and security of any website by analyzing key indicators like DNS resolution, HTTP response, SSL validity, and metadata.

---

## 🚀 Features

- ✅ DNS resolution and IP mapping
- ✅ HTTP status code and response time
- ✅ SSL certificate validation
- ✅ Website title and redirect chain
- ✅ HTTP response headers
- 🖥️ Clean, corporate-style UI (HTML/CSS)
- 🌐 Web interface + JSON API

---

## 🛠️ Technologies Used

- FastAPI
- Jinja2 (Templating)
- Requests (HTTP Client)
- BeautifulSoup4 (HTML parsing)
- HTML/CSS (Frontend)

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/pulsecheck.git
cd pulsecheck
pip install -r requirements.txt

## Usage

Start the server:

uvicorn main:app --reload

Open in your browser:
http://127.0.0.1:8000
