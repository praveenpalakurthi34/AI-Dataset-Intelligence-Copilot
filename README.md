# AI-Dataset-Intelligence-Copilot
Vision - AI for Builders

Problem Statement - AI Dataset Intelligence Copilot is an AI-powered platform that analyzes uploaded datasets, detects quality issues, explains their impact, recommends fixes, generates preprocessing code, and guides users through dataset preparation using conversational AI. 

Team Member - Boddu Mandeep, Manipavan Reddy Chandhireddy, Palakurthi Durga Praveen

# AI Dataset Intelligence Copilot

> **An AI-powered dataset quality auditing and automated data cleaning platform that transforms raw CSV datasets into machine-learning-ready data using intelligent decision-making and automated preprocessing.**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)
![React](https://img.shields.io/badge/React-Frontend-61DAFB.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-Frontend-3178C6.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

# Overview

AI Dataset Intelligence Copilot is an intelligent web application that automates dataset quality assessment and preprocessing using Artificial Intelligence. The platform enables users to upload CSV datasets, analyze data quality, receive AI-powered cleaning decisions, automatically repair common issues, generate executable Python preprocessing code, and export comprehensive PDF reports.

The project eliminates manual dataset inspection by combining rule-based auditing with AI-driven decision making, helping data scientists and machine learning engineers prepare high-quality datasets faster and more accurately.

---

# Features

## 📂 Dataset Upload
- Upload CSV datasets
- Automatic encoding detection
- Metadata extraction
- Dataset profiling
- Large dataset support

---

## 🔍 AI Data Quality Auditor

Automatically detects:

- Missing Values
- Duplicate Rows
- Data Type Inconsistencies
- Numerical Outliers (IQR)
- Dataset Statistics
- Column Statistics
- Readiness Metrics

---

## 🤖 AI Decision Engine

Instead of generic recommendations, the AI generates intelligent cleaning decisions.

Each decision includes:

- Decision Name
- Target Columns
- Confidence Score
- Reason
- Expected Impact
- Auto Fix Availability

Example decisions:

- Remove Duplicate Rows
- Fill Missing Values
- Cap Numerical Outliers
- Convert Data Types
- Remove Constant Columns
- Review Suspicious Features

---

## ⚡ Auto Fix Engine

Automatically executes AI-approved preprocessing steps.

Supported operations:

- Remove duplicate rows
- Fill missing values
- Correct data types
- Cap outliers
- Remove constant columns

Outputs a cleaned dataset ready for machine learning.

---

## 🧹 AI Generated Python Cleaning Code

Generates executable Pandas preprocessing scripts corresponding to the AI decisions.

---

## 📊 Dataset Readiness Score

Evaluates dataset quality using:

- Completeness
- Uniqueness
- Data Type Validity
- Outlier Analysis

Outputs:

- Overall Score
- Grade
- Dataset Status

---

## 📄 PDF Report Generation

Automatically generates professional PDF reports containing:

- Executive Summary
- Dataset Metadata
- Data Quality Audit
- Readiness Score
- AI Decisions
- Python Cleaning Code

---

# System Architecture

```
                    Upload CSV
                         │
                         ▼
            Dataset Metadata Extraction
                         │
                         ▼
         Rule-Based Data Quality Auditor
                         │
                         ▼
            Dataset Readiness Scoring
                         │
                         ▼
               AI Decision Engine
               ┌─────────┴─────────┐
               ▼                   ▼
        Auto Fix Engine     Python Cleaning Code
               │                   │
               ▼                   ▼
      Cleaned Dataset       PDF Audit Report
```

---

# Technology Stack

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Lucide React

---

## Backend

- FastAPI
- Python
- Pydantic
- SQLAlchemy
- SQLite

---

## Artificial Intelligence

- DeepSeek V3.2
- Featherless AI
- OpenAI Compatible SDK

---

## Data Processing

- Pandas
- NumPy
- Scikit-learn

---

## Report Generation

- ReportLab

---

# Project Structure

```
AI-Dataset-Intelligence-Copilot
│
├── backend
│   ├── api
│   ├── database
│   ├── engines
│   ├── models
│   ├── schemas
│   ├── uploads
│   ├── outputs
│   ├── reports
│   ├── config.py
│   └── main.py
│
├── frontend
│   ├── public
│   └── src
│       ├── assets
│       ├── components
│       ├── pages
│       ├── services
│       ├── types
│       └── App.tsx
│
├── datasets
├── README.md
└── requirements.txt
```

---

# Workflow

```
Upload Dataset
       │
       ▼
Rule-Based Audit
       │
       ▼
Dataset Readiness Score
       │
       ▼
AI Decision Engine
       │
       ▼
Auto Fix Dataset
       │
       ▼
Download Cleaned Dataset
       │
       ▼
Generate PDF Report
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/AI-Dataset-Intelligence-Copilot.git

cd AI-Dataset-Intelligence-Copilot
```

---

## Backend Setup

```bash
cd backend

python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file inside the backend folder.

```env
FEATHERLESS_API_KEY=YOUR_API_KEY

FEATHERLESS_BASE_URL=https://api.featherless.ai/v1

FEATHERLESS_MODEL=deepseek-ai/DeepSeek-V3.2
```

---

## Run Backend

```bash
uvicorn main:app --reload
```

Backend

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend

```
http://localhost:3000
```

---

# REST API

### Upload Dataset

```
POST /api/upload
```

### Analyze Dataset

```
POST /api/analyze/{dataset_id}
```

### Generate AI Decisions

```
POST /api/analyze-ai/{dataset_id}
```

### Auto Fix Dataset

```
POST /api/autofix/{dataset_id}
```

### Download Cleaned Dataset

```
GET /api/download-cleaned/{filename}
```

### Download PDF Report

```
GET /api/report/pdf/{dataset_id}
```

---

# Sample AI Decision

```json
{
  "decision": "Fill Missing Values",
  "target": "Severity, Affected_Machine",
  "confidence": 97,
  "reason": "Missing values reduce dataset completeness and affect downstream machine learning models.",
  "expected_impact": "Improves data quality, completeness, and model readiness.",
  "auto_fix": true
}
```

---

# Application Screens

- Landing Page
- Dataset Upload
- Audit Dashboard
- AI Decision Engine
- Auto Fix Dataset
- Reports
- History

---

# Future Enhancements

- Excel, JSON, and Parquet support
- Interactive visual analytics
- Explainable AI (XAI)
- ML model readiness prediction
- Dataset versioning
- Authentication & User Management
- Team collaboration
- Cloud deployment (Docker & Kubernetes)
- Real-time data quality monitoring

---

# Contributors

**Team ECHO-2026**

- Backend Development
- Frontend Development
- Artificial Intelligence Integration
- Data Processing
- UI/UX Design
- Report Generation

---



# Acknowledgements

This project is built using the following open-source technologies:

- FastAPI
- React
- Featherless AI
- DeepSeek AI
- Pandas
- NumPy
- Scikit-learn
- SQLAlchemy
- ReportLab

---
