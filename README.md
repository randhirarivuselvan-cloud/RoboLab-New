# RoboLab 2.0 Release Candidate

**RoboLab | SynapseX Robotics & Technologies**  
**Innovation Beyond Imagination.**

This package is the complete deployable application source. It includes the web UI, FastAPI backend, SQLite project storage, component catalog, project planner, calculator, optional Google OAuth, optional OpenAI-powered planning, optional Stripe subscriptions, region preferences, tests, and Render configuration.

## What works without paid/external credentials
- Responsive RoboLab dashboard
- Project planner with deterministic starter engineering plans
- Component catalog and recommendations
- Cost calculator
- Project save/list/get/update/delete
- Optional coarse country/region setting
- Health/status and API docs
- Local SQLite database

## Optional integrations
### Google Sign-In
Set `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and the exact `GOOGLE_REDIRECT_URI`. The OAuth secret stays server-side.

### AI planner
Set `OPENAI_API_KEY`. If it is missing or the AI request fails, RoboLab automatically falls back to the deterministic starter planner instead of pretending AI is active.

### Premium billing
Set `STRIPE_SECRET_KEY`, `STRIPE_MONTHLY_PRICE_ID`, and `STRIPE_ANNUAL_PRICE_ID`. The UI keeps billing disabled until all required Stripe settings exist.

The included prices are ₹99/month and ₹799/year as requested. Stripe price objects must be created in your own Stripe account; no secret or payment credentials are included.

## Local Windows setup
```bat
py -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` and `/docs` for API documentation.

## Google OAuth redirect
For local development:
`http://127.0.0.1:8000/api/auth/google/callback`

For Render, replace `YOUR-RENDER-DOMAIN` in the Render environment settings with the real service hostname and use that exact callback in Google Cloud Console.

## Render
The included `render.yaml` is ready for a Render Python web service. Add real values for OAuth, AI and Stripe only if you want those features.

**Database note:** SQLite is fine for local development and demos, but Render's normal web filesystem is not a durable database. For a production multi-user launch, move project/user storage to a managed PostgreSQL database and keep secrets in Render environment variables.

## Security
- Never commit `.env`.
- Never commit OAuth client secrets, AI keys or Stripe secret keys.
- Never upload generated local HTTPS private keys.
- Replace the development secret if running outside local development.
- The app does not require precise device location.
- Component prices are example estimates, not live marketplace prices.
- Engineering plans are planning aids, not hardware validation or safety certification.
