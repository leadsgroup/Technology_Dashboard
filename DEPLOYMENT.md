# Render Deployment Guide — LEADS Technology Dashboard

## Prerequisites

- A [Render](https://render.com) account connected to the GitHub repository
- Push access to the repository

---

## First-Time Deployment

1. Log in to [dashboard.render.com](https://dashboard.render.com)
2. Click **New > Blueprint**
3. Connect the GitHub repository (`technology_dashboard` or equivalent)
4. Render will detect `render.yaml` automatically and configure the service
5. Click **Apply** — Render will install dependencies and start the app

The service is configured in `render.yaml`:

| Setting | Value |
|---|---|
| Service type | Web service |
| Runtime | Python 3.10 |
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn --chdir src app:server` |
| Plan | Free |

> **Note:** The free plan spins down after 15 minutes of inactivity. The first request after a spin-down takes ~30 seconds to respond.

---

## Re-Deploying After Changes

### Option A — Automatic (recommended)

Render re-deploys automatically whenever commits are pushed to the branch it tracks (by default `main`).

1. Make changes on a feature branch (e.g. `feature_dashboard_redesign`)
2. Open a pull request into `main`
3. Merge the PR — Render detects the push to `main` and deploys automatically
4. Monitor progress in the Render dashboard under **Events**

### Option B — Manual trigger

1. Go to [dashboard.render.com](https://dashboard.render.com) and open the `leads_dashboard` service
2. Click **Manual Deploy > Deploy latest commit**

---

## Project Structure

```
technology_dashboard/
├── render.yaml           # Render service configuration
├── requirements.txt      # Python dependencies
├── Data/                 # Excel/CSV data files (not served publicly)
└── src/
    ├── app.py            # Entry point — exports `server = app.server`
    ├── Electrification/
    ├── SAF/
    ├── Hydrogen/
    └── Energy_X/
```

> Gunicorn is launched with `--chdir src` so it treats `src/` as the working directory. All relative paths inside the app use `os.path.dirname(os.path.abspath(__file__))` as the base.

---

## Environment Variables

Set in `render.yaml` (no secrets required — Mapbox has been removed):

| Key | Value | Purpose |
|---|---|---|
| `PYTHON_VERSION` | `3.10.0` | Pins the Python runtime |

---

## Updating Dependencies

Edit `requirements.txt` and commit. The next deploy will pick up the changes.

Key constraints:
- `plotly>=5.18` — required for `px.scatter_map` (open-source map tiles, no API key)
- `dash` — unpinned so Render uses the latest stable version

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Build fails with `ModuleNotFoundError` | Missing package in `requirements.txt` | Add the package and redeploy |
| Maps show blank tiles | Plotly version below 5.18 | Ensure `plotly>=5.18` is in `requirements.txt` |
| App crashes on startup | Data file not found | Check that all paths in `app.py` use `os.path.join(os.path.dirname(__file__), ...)` |
| `500` error on a tab | Callback exception | Check Render logs under **Events > Logs** |
| Slow first load | Free plan spin-down | Expected — upgrade to a paid plan to keep the service live |
