# DnD

## Setup

`.venv` is not checked into git.

From the workspace root, create and activate the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Backend

Install and run:

```powershell
python -m pip install -e backend
medieval-backend
```

## Frontend

From `frontend`:

```powershell
npx webpack
```
