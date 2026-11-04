# Sample Model API (for testing FairNexa)

This folder provides a **local dummy “AI model API”** you can run to test FairNexa end-to-end.

## What it does

- Exposes `POST /predict`
- Accepts **any JSON** input (FairNexa synthetic records)
- Returns a simple JSON output:
  - `prediction`: numeric score (0-1)
  - `label`: `"approved"` or `"rejected"`

## Setup (Windows PowerShell)

```powershell
cd C:\Users\Yash\Desktop\FairNexa\sample_model_api
python -m venv venv
.\venv\Scripts\Activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 5000
```

## Use in FairNexa

In the FairNexa UI, paste:

`http://localhost:5000/predict`

Because FairNexa blocks private-network model URLs by default, set
`MODEL_ALLOW_PRIVATE_URLS=true` in the backend environment when running this
local sample API.

## Test quickly (optional)

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:5000/predict `
  -ContentType "application/json" `
  -Body '{"age":30,"income":60000,"credit_score":720,"gender":"male","race":"white"}'
```
