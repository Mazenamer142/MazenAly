# Toyota Al-Ghuraiz – landing page prototype

Static, no server needed: open `index.html` (works from `file://`).
`?nointro` skips the intro, `?lang=en` starts in English.

- `index.html` – markup · `style.css` – light theme (palette from the shop photo) · `app.js` – i18n (AR/EN), intro, scroll effects
- `car3d.js` – bundled three.js + procedural 3D Land Cruiser (generated, don't edit)
- `src/car3d.js` – source for the 3D car/stage

Rebuild the bundle after editing `src/car3d.js`:

    npm i three esbuild
    npx esbuild src/car3d.js --bundle --minify --format=iife --outfile=car3d.js
