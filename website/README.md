# FlowGuard Website

A standalone Next.js landing page for the FlowGuard network intrusion detection project.

## Local development

```bash
cd website
npm install
npm run dev
```

Open `http://localhost:3000`.

## Validation

```bash
npm run typecheck
npm run build
```

## Deploy on Vercel

1. Import `puneetdixit200/flowguard` into Vercel.
2. Set **Root Directory** to `website`.
3. Keep the detected framework as **Next.js**.
4. Use the default install and build commands.
5. Deploy.

The website is intentionally isolated from the existing dashboard and backend services. Deploying this directory does not replace the FastAPI/Render runtime.

## Content sources

The benchmark cards use the checked-in real-flow evaluation results from `docs/real_only_evaluation.txt`. Architecture and feature descriptions reflect the repository's capture, ML service, persistence, dashboard, Docker, and engineering diagram structure.
