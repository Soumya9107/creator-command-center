# 🏴‍☠️ Creator Command Center

> Query your YouTube & Twitter data as SQL — powered by [Coral](https://withcoral.com)

🔗 **[Live Dashboard](https://creator-command-center-seven.vercel.app/)**

---

## 🤔 The Problem

As a content creator, you're constantly switching between YouTube and Twitter
just to answer one question — *what's actually working?*

Creator Command Center solves this with a single SQL query across all your platforms.

---

## ✨ What It Does

| Query | Sources |
|---|---|
| What's my most viewed video? | YouTube |
| What tweets get the most engagement? | Twitter |
| Cross-platform engagement summary | YouTube + Twitter |

---

## 🛠️ Tech Stack

- **[Coral](https://withcoral.com)** — SQL interface over APIs
- **Python** — Agent & dashboard generator
- **Docker** — Isolated environment
- **YouTube Data API v3** — Video data
- **Twitter API v2** — Tweet data

---

## 📁 Project Structure

creator-command-center/
├── sources/
│   ├── youtube.yaml       ← Custom Coral source spec
│   ├── twitter.yaml       ← Custom Coral source spec
├── queries/
│   ├── weekly_summary.sql
│   └── audience_questions.sql
├── agent/
│   └── main.py            ← Runs queries & generates dashboard
├── Dockerfile
├── docker-compose.yml
└── index.html             ← Live dashboard
