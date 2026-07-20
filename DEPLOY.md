# Deployment Guide

## Overview

This repo is connected to Vercel for automatic deployments.

## Workflow

### 1. Push to staging → Vercel preview deploy

```bash
git checkout staging
# make your changes
git add .
git commit -m "Your message"
git push origin staging
```

Vercel automatically creates a preview deployment for the `staging` branch. Check the Vercel dashboard or the GitHub PR for the preview URL.

### 2. Test the preview URL

Open the preview URL in your browser and verify:
- The page loads correctly
- All forms and interactive elements work
- The apply page (`apply.html`) functions as expected

### 3. Open PR to main → syntax check runs

```bash
gh pr create --base main --head staging --title "Your PR title" --body "Description of changes"
```

Opening a pull request from `staging` to `main` triggers the **Syntax Check** GitHub Action (`.github/workflows/syntax-check.yml`), which:
- Validates `index.html` syntax via Node.js
- Validates `apply.html` syntax via Node.js

Fix any failures before merging.

### 4. Merge to main → Vercel deploys production

Once the PR is approved and the syntax check passes, merge to `main`. Vercel automatically deploys the production site.

## CI/CD Pipeline

```
Push to staging → Vercel preview deploy
       ↓
Open PR to main → GitHub Action: syntax check
       ↓
Merge to main → Vercel production deploy
```
