# herrell.us

Static homepage: plain HTML, CSS and JS, no build step.

```
wrangler.jsonc             Cloudflare config (serves ./public)
public/index.html          homepage
public/404.html            shown for any page that doesn't exist yet
public/assets/styles.css   all styles (colors and fonts are tokens at the top)
public/assets/main.js      footer year
public/favicon.svg
```

Preview locally: `python3 -m http.server 8000 -d public`, then open http://localhost:8000.

## Deploy (GitHub + Cloudflare)

The repo is connected to Cloudflare (Workers & Pages → Import a repository) with:

- Build command: empty
- Deploy command: `npx wrangler deploy`
- Preview command: `npx wrangler preview`

`wrangler.jsonc` tells Cloudflare to serve everything in `public/` as static files and to use `public/404.html` for missing pages. Every push to `main` redeploys; other branches get preview builds.

Custom domain: in the Worker's Settings → Domains & Routes, add `herrell.us` (and `www.herrell.us` if you want it).

Adding a section: create a folder such as `public/portfolio/index.html`, then edit that section's card in `public/index.html` (remove its `stamp` once the page is live).

Photo: drop a square image at `public/assets/photo.jpg` and it replaces the initials in the hero portrait.
