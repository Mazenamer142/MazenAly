# Portfolio: Mazen Ali Abdallah Abdelazeem

Single-file static site (`index.html`): no build step, no dependencies.

## Edit
Search `index.html` for `EDIT` to find every editable spot (email, project cards, links, image paths).
Project images go in `assets/images/`. Point each card's `<img src="">` at them, e.g. `assets/images/flagship-project.png`.

## Preview locally
Open `index.html` in a browser, or run `npx serve .`

## Deploy on Vercel
1. Push this repo to GitHub.
2. Vercel dashboard: Add New, Project, import the repo.
3. Leave Framework Preset as **Other**. No build command, no output directory needed (`vercel.json` already sets them).
4. Deploy. Every push to the production branch redeploys automatically.

Or from the CLI: `npx vercel --prod`.
