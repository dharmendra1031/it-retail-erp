# React frontend

Shared React + TypeScript frontend for both ERP backends.

## Development

1. Run `npm install`.
2. Copy `.env.example` to `.env`.
3. Set `VITE_PROXY_TARGET` to the backend URL.
4. Run `npm run dev`.

Examples:

- ASP.NET Core: `VITE_PROXY_TARGET=http://localhost:5000`
- Django: `VITE_PROXY_TARGET=http://127.0.0.1:8000`

The frontend always calls relative `/api` URLs and does not contain backend-specific code.
