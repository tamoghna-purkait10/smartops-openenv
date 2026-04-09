---
title: SmartOps OpenEnv
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---

# SmartOps OpenEnv

AI-powered customer support triage simulation environment built using OpenEnv specification.

## Overview
This environment simulates enterprise-grade customer support workflows where an AI agent must:
- Classify ticket priority
- Route to correct department
- Generate appropriate responses

## Features
- Real-world task simulation
- Multi-level difficulty (easy, medium, hard)
- Semantic reward using embeddings
- LLM-driven agent inference

## Run Locally

```bash
docker build -t smartops .
docker run smartops