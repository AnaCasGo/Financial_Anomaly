# Financial Anomaly Detection Platform

An end-to-end data analytics project that combines statistics, SQL, machine learning, business intelligence and explainable AI to detect anomalous financial transactions.

---

# Introduction

This project simulates how a data analytics team could design and build a financial anomaly detection platform from scratch.

Rather than focusing only on machine learning, the project follows the complete analytics lifecycle: understanding the business problem, generating realistic data, engineering features, applying statistical methods, training anomaly detection models, building dashboards, and generating human-readable reports.

The objective is to showcase not only technical skills but also the ability to design a complete analytical solution similar to those used in real-world financial institutions.

---

# Business Problem

Financial institutions process millions of transactions every day. Detecting unusual activity quickly is essential to reduce fraud, operational risks, financial losses, and improve customer trust.

Traditional rule-based systems often fail to identify new or previously unseen fraud patterns. This project explores how statistical analysis and unsupervised machine learning can help identify anomalous transactions while providing clear, human-readable explanations for fraud analysts.

The goal is not to build a production-ready fraud detection engine, but to simulate how a real analytics team could design an end-to-end anomaly detection platform. The platform includes a customer verification workflow where high-risk transactions trigger a real-time email requesting customer confirmation before the transaction is completed.

---

# Objectives

- Design a realistic financial transactions database.
- Generate synthetic customer and transaction data.
- Simulate different types of anomalous financial behaviour.
- Explore statistical techniques for anomaly detection before applying machine learning.
- Engineer meaningful features using SQL.
- Compare multiple anomaly detection algorithms.
- Explain model predictions using interpretable metrics and LLM-generated reports.
- Compare accuracy rate of rule-base systems vs machine learning based system 
- Build an interactive Power BI dashboard for fraud monitoring.
- Create an automated analytical pipeline from raw data to business insights.
- Follow software engineering best practices using Git, GitHub Projects, Issues, Pull Requests and documentation.
- Create a customer verification request for high risk alerts

---

# Tech Stack

Languages

- SQL
- Python

Data

- Pandas
- NumPy

Machine Learning

- Scikit-learn

Business Intelligence

- Power BI

Version Control

- Git
- GitHub

AI

- OpenAI API
- GitHub Copilot
- Gemini

Future

- Docker
- dbt

---

# Architecture

Synthetic Data Generator
        │
        ▼
SQL Database
        │
        ▼
Feature Engineering
        │
        ▼
Statistical Detection
        │
        ▼
ML Detection Engine
        │
        ▼
Risk Scoring
        │
        ├── Fraud Alerts
        ├── Power BI Dashboard
        ├── Customer Email
        └── LLM Explanation

# Why Synthetic Data?

Real banking datasets containing fraudulent transactions are rarely public due to privacy regulations and security concerns.

To overcome this limitation, this project generates realistic synthetic data that simulates customer behaviour, transaction patterns and different fraud scenarios while maintaining full control over the data generation process.

This also allows the evaluation of anomaly detection methods under controlled conditions.

---

# System Workflow

The platform simulates how a modern financial institution could process transactions in real time.

```text
Customer initiates a transaction
        │
        ▼
Transaction enters the platform
        │
        ▼
Feature Engineering
        │
        ▼
Anomaly Detection Engine
        │
        ▼
Risk Score Calculation
        │
        ├── 🟢 Low Risk
        │      └── Transaction approved automatically
        │
        ├── 🟡 Medium Risk
        │      ├── Transaction approved
        │      └── Fraud alert generated for analyst review
        │
        └── 🔴 High Risk
               ├── Transaction temporarily held
               ├── Customer verification requested
               └── Fraud team notified
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
     Customer confirms            Customer reports fraud
              │                           │
              ▼                           ▼
     Transaction completed      Transaction blocked
```

---

# Planned Customer Verification

One of the final stages of the project is to simulate how a financial institution interacts with customers when a high-risk transaction is detected.

When the anomaly detection engine assigns a high risk score, the platform will simulate sending an email requesting transaction verification.

The customer will be able to:

- ✔️ Confirm the transaction, allowing it to be completed.
- ❌ Report the transaction as fraudulent, resulting in it being blocked and flagged for investigation.

The objective is to reproduce a realistic fraud prevention workflow rather than focusing only on anomaly detection.

- HTML email generation
- One-click confirmation links
- Fraud case management
- Customer response tracking
- Alert history
- Analyst investigation dashboard

# Features

- ⌛ Synthetic financial transaction generator
- ⌛ Realistic customer behaviour simulation
- ⌛ Statistical anomaly detection
- ⌛ Machine learning anomaly detection
- ⌛ SQL feature engineering
- ⌛ Explainable AI reports
- ⌛ Fraud analyst dashboard
- ⌛ Customer verification workflow
- ⌛ Real-time transaction simulation
- ⌛ Email notification system
- ⌛ Docker deployment
- ⌛ CI/CD pipeline
  
---

# Project Roadmap

- [ ] Business Understanding
- [ ] Database Design
- [ ] Synthetic Data Generation
- [ ] Exploratory Data Analysis
- [ ] SQL Feature Engineering
- [ ] Statistical Anomaly Detection
- [ ] Machine Learning Models
- [ ] Explainable AI
- [ ] Dashboard Development
- [ ] Automation Pipeline
- [ ] Testing
- [ ] HTML email generation
- [ ] Documentation

---

# Learning Goals

This project was created as a long-term learning initiative.

The objective is to deepen my understanding of:

- Statistical modelling
- Machine learning for anomaly detection
- SQL feature engineering
- Data pipeline design
- Explainable AI
- Software engineering best practices
