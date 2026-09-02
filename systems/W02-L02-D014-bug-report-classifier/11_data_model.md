# Data Model: Bug Report Classifier

## Core Entities

### Input

| Field | Type | Description |
|---|---|---|
| id | string | Unique identifier |
| content | string | Raw input content |
| metadata | dict | Source, timestamp, tags |

### Output

| Field | Type | Description |
|---|---|---|
| id | string | Unique identifier |
| input_id | string | Reference to input |
| result | string | Generated result |
| confidence | float | Model confidence (0.0–1.0) |








## Storage

- JSON or markdown files for simple persistence
- Obsidian vault for human-readable artifacts

## Notes

This data model is intentionally minimal at Level 2. It grows as you add users, APIs, and evaluation.
