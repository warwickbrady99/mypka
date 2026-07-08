# F247 AsdAIr Microsite - Next.js V1

This is the Vercel-oriented migration of the Mum-facing shopping page.

The original FastAPI MVP remains in `../2026-07-08-f247-asdair-microsite` and has not been deleted or overwritten.

## Current Scope

Included:

- Private Mum route at `/mum/<MUM_ACCESS_TOKEN>`.
- Static catalogue ported from the FastAPI starter items.
- Grouped shopping items.
- Plus and minus quantity controls.
- `Use usual shop` reset.
- `Anything else?` notes box.
- Gmail SMTP email submission.
- Friendly success and failure messages.

Not included:

- Database storage.
- Admin dashboard.
- Cloud file exports.
- Asda login, payment, API, checkout, or order placement.

## Local Setup

```powershell
npm install
Copy-Item .env.example .env.local
```

Set a private token in `.env.local`:

```text
MUM_ACCESS_TOKEN=your-long-private-shopping-token
GMAIL_SMTP_USER=your-gmail-address@gmail.com
GMAIL_SMTP_APP_PASSWORD=your-gmail-app-password
SHOPPING_EMAIL_TO=warwick@example.com
```

Run locally:

```powershell
npm run dev
```

Open:

```text
http://localhost:3000/mum/your-long-private-shopping-token
```

## Verification

- The plain `/` page should only show private-link guidance.
- `/mum/<wrong-token>` should return a not-found page.
- `/mum/<correct-token>` should show Mum's Shopping.
- Plus buttons increase quantities.
- Minus buttons decrease quantities and never go below zero.
- `Use usual shop` restores the original default quantities.
- Pressing `Send list to Warwick` sends the selected items and `Anything else?` text by email.
- The success screen states the safety boundary: this is only a shopping request.
- If email settings are missing or Gmail rejects the login, the page shows a friendly failure message.

## Vercel Deployment

Add the same environment variables in the Vercel project settings:

- `MUM_ACCESS_TOKEN`
- `GMAIL_SMTP_USER`
- `GMAIL_SMTP_APP_PASSWORD`
- `SHOPPING_EMAIL_TO`

Vercel runs the `/api/shopping-list` route server-side, so the Gmail credentials stay out of the browser bundle.
