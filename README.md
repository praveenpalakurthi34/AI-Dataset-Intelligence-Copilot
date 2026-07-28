# AI-Dataset-Intelligence-Copilot
Vision - AI for Builders

Problem Statement - AI Dataset Intelligence Copilot is an AI-powered platform that analyzes uploaded datasets, detects quality issues, explains their impact, recommends fixes, generates preprocessing code, and guides users through dataset preparation using conversational AI. 

Architecture -                               
Complete High level architecture
AI Dataset Intelligence Copilot

┌───────────────────────────────────────────────────────────────────────────────┐
│                               React + TypeScript                             │
│                                                                               │
│ Landing │ Upload │ Dashboard │ AI Insights │ Reports │ History               │
└───────────────────────────────┬───────────────────────────────────────────────┘
                                │
                         HTTPS REST API
                                │
┌───────────────────────────────▼───────────────────────────────────────────────┐
│                              FastAPI Backend                                 │
└───────────────────────────────┬───────────────────────────────────────────────┘
                                │
      ┌─────────────────────────┼─────────────────────────┐
      │                         │                         │
      ▼                         ▼                         ▼
 Dataset Analysis        AI Reasoning Engine       Report Engine
      Engine                                              │
      │                                                   │
      └──────────────────────┬────────────────────────────┘
                             ▼
                      SQLite Database


                    MODULE 1 - DATASET ANALYSIS ENGINE

                           Uploaded CSV
                                │
                                ▼
                         CSV Parser (Pandas)
                                │
                                ▼
                       Metadata Extraction
                                │
        ┌───────────────────────┼────────────────────────┐
        │                       │                        │
        ▼                       ▼                        ▼
 Missing Value           Duplicate Row            Data Type
    Detector               Detector               Validator

        ▼                       ▼                        ▼
 Outlier Detector      Dataset Statistics      Dataset Summary

        └───────────────────────┼────────────────────────┘
                                ▼
                  Dataset Readiness Calculator
                                │
                                ▼
                  Structured Audit Report (JSON)

                    MODULE 2 - AI REASONING ENGINE

                 Structured Audit Report
                          │
                          ▼
                    Prompt Builder
                          │
                          ▼
                  Context Generator
                          │
                          ▼
                     Gemini API
                          │
                          ▼
                 Response Formatter
                          │
          ┌───────────────┼────────────────┐
          ▼               ▼                ▼
   AI Explanation   Recommendations   Python Code
                                         Generator

            MODULE 3 - REPORT ENGINE

               Dataset Summary
                      │
                      ▼
             Dataset Statistics
                      │
                      ▼
            AI Recommendations
                      │
                      ▼
          Generated Python Code
                      │
                      ▼
        Readiness Score + Charts
                      │
                      ▼
                Export PDF Report

User

↓

Upload CSV

↓

React Frontend

↓

FastAPI

↓

CSV Parser

↓

Dataset Analysis Engine

↓

Structured Audit Report

↓

Dataset Readiness Score

↓

AI Reasoning Engine

↓

AI Explanation
Recommendations
Generated Cleaning Code

↓

Dashboard

↓

Download Report (Phase 2)

Folder structure:
AI-Dataset-Intelligence-Copilot/

frontend/
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── hooks/
│   ├── layouts/
│   ├── assets/
│   └── App.tsx
│
backend/
│
├── api/
├── engines/
│     ├── parser.py
│     ├── metadata.py
│     ├── auditor.py
│     ├── readiness.py
│     ├── ai_engine.py
│     ├── prompts.py
│     └── report.py
│
├── models/
├── schemas/
├── database/
├── utils/
└── main.py

shared/

reports/

datasets/

TEch Stack:
Frontend - 
| Technology   | Purpose            | Required |
| ------------ | ------------------ | -------- |
| React        | Frontend Framework | ✅        |
| TypeScript   | Type Safety        | ✅        |
| Tailwind CSS | Styling            | ✅        |
| Axios        | API Calls          | ✅        |
| React Router | Page Navigation    | ✅        |
| Recharts     | Dashboard Charts   | ✅        |

Backend - 
| Technology       | Purpose     | Required |
| ---------------- | ----------- | -------- |
| FastAPI          | REST API    | ✅        |
| Uvicorn          | Server      | ✅        |
| Python           | Backend     | ✅        |
| Pydantic         | Validation  | ✅        |
| python-multipart | File Upload | ✅        |

Data analysis - 
| Library      | Purpose                        | Required |
| ------------ | ------------------------------ | -------- |
| Pandas       | Read CSV                       | ✅        |
| NumPy        | Numerical Operations           | ✅        |
| Scikit-Learn | Outlier & Statistics Utilities | ✅        |

AI engine - 
| Technology | Purpose      | Required |
| ---------- | ------------ | -------- |
| Gemini API | AI Reasoning | ✅        |

Database - 
| Technology | Purpose                | Required               |
| ---------- | ---------------------- | ---------------------- |
| SQLite     | Store Analysis History | 🟡 Optional in Phase 1 |

Workflow:
              AI Dataset Intelligence Copilot

                     Upload CSV
                          │
                          ▼
                 Dataset Analysis Engine
                          │
      ┌───────────────────┼────────────────────┐
      │                   │                    │
      ▼                   ▼                    ▼
 Missing Values      Duplicates         Outliers
      │                   │                    │
      └───────────────┬────────────────────────┘
                      ▼
              Dataset Summary
                      │
                      ▼
          Dataset Readiness Score
                      │
                      ▼
             AI Reasoning Engine
                      │
          ┌───────────┼────────────┐
          ▼           ▼            ▼
     Explanation  Recommendation  Code
                      │
                      ▼
                 React Dashboard
