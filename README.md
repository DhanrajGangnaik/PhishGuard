# PhishGuard

## Overview

**PhishGuard** is a lightweight, containerized cybersecurity tool that detects phishing attempts in **URLs and email content** using a hybrid approach of rule-based analysis and intelligent scoring.

The system runs entirely on a **local machine**, ensuring privacy while providing **real-time, explainable threat detection** through an interactive web dashboard.

---

## Key Features

### URL Phishing Detection
- Detects suspicious domains, IP-based URLs, shortening services, and malicious patterns

### Email Content Analysis
- Identifies phishing language such as urgency, credential requests, and deceptive tone

### Explainable Detection Engine
- Provides reasons for classification (not just output)

### Interactive Dashboard
- Visualizes scan results and trends

### Scan History Tracking
- Stores and displays previous analyses using SQLite

### Containerized Deployment
- Easily deployable using Docker and Docker Compose

---

## Architecture

User Input (URL / Email)
↓
Feature Extraction (Regex + Rules)
↓
Risk Scoring Engine
↓
Classification (Safe / Suspicious / Phishing)
↓
Results + Explanation + Dashboard

---

## Project Structure
```
PhishGuard/
│
├── app.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
│
├── templates/
├── static/
├── utils/
├── database/
├── dataset/
└── model/
```


---

## Installation & Setup

### Option 1: Run Locally

```bash
git clone https://github.com/your-username/phishguard.git
cd PhishGuard
```
```
python -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate    # Windows
```
```
pip install -r requirements.txt
python app.py
```

---

## Open:

```http://127.0.0.1:5000```

### Option 2: Run with Docker (Recommended)
```
docker compose up --build
```
- Open:
```
http://127.0.0.1:5001
```

---

## Demo Inputs

### 🔴 Phishing URL
```http://secure-login-bank-update.verify-user.ru```


### 🔴 Phishing Email
```
Dear Customer,
Your account will be suspended immediately.
Verify your password and OTP now.
```

### 🟢 Safe URL
```https://github.com```

---

## Output Example
- Result: Phishing
- Risk Score: 87%

### Reasons:

- Suspicious keyword detected
- Deceptive domain structure
- Urgent language pattern

---

## Detection Logic

PhishGuard evaluates inputs based on:

- URL Indicators
- IP address usage
- URL length
- Suspicious keywords (login, verify, secure)
- Shortened links
- Excessive subdomains
- Lack of HTTPS

### Email Indicators
- Urgent tone
- Credential requests
- Threat language
- Suspicious links
- Social engineering patterns

---

## Use Cases
- Academic cybersecurity demonstrations
- Phishing awareness training
- Local security testing tool
- Lightweight SOC-style monitoring

---

## Limitations
- Rule-based detection may produce false positives
- Does not analyze email headers or attachments
- Limited to known phishing patterns

---

## Future Improvements
- Machine learning-based classification
- Browser extension integration
- Real-time email scanning
- Domain reputation APIs
- QR phishing detection