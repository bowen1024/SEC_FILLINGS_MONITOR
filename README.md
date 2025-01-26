# SEC Filings Monitor

A Python script that automatically monitors SEC filings for specified companies and sends email notifications when new filings are detected. Built to run on GitHub Actions with AWS S3 integration for state management and logging.

## Features

- 🕒 Scheduled checks (configurable via cron)
- 📧 Email notifications for new filings
- ☁️ AWS S3 integration for data persistence
- 📝 Comprehensive logging
- 🔍 Minimal dependencies
- ⚙️ Fully configurable via environment variables
- 🛠️ Error handling and retries

## Prerequisites

- GitHub account
- AWS account (for S3)
- Email service provider (Gmail, Outlook, etc.)
- Python 3.10+

## Setup

### 1. Clone Repository
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
