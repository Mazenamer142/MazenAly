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

## Case studies
Three data analysis + business analysis projects live in `projects/` (`maven-toys`, `coffee-shop`, `video-games`). Each has SQL, a Python check, summary data, and a documents package. The coffee shop and video game pages are built in the browser from the JSON blocks `#proj-coffee` and `#proj-games` in `index.html`.

## Adding a Power BI dashboard
1. Publish the report (Power BI: File, Embed report, Publish to web) or a Tableau Public view.
2. Paste the link into `window.PB_EMBEDS` near the bottom of `index.html` (`maven`, `coffee` or `games`).
3. Only `app.powerbi.com` and `public.tableau.com` links are used, and `vercel.json` already allows them in `frame-src`.
4. Also set the "Live dashboard" link on the business analysis card (search `EDIT POWER BI LINK HERE`).
