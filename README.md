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
```

Generate map data (only needed if map files are missing or maps change):

```powershell
python map_generation.py
```

Start the backend:

```powershell
medieval-backend
```

## Frontend

From `frontend`, install dependencies (first time only):

```powershell
npm install
```

Then serve locally at `http://localhost:8080/`:

```powershell
npm run serve
```
