# herrell.us

Static homepage: plain HTML, CSS and JS, no build step.

```
index.html          homepage
404.html            shown for any page that doesn't exist yet
assets/styles.css   all styles (colors and fonts are tokens at the top)
assets/main.js      footer year
favicon.svg
```

Preview locally: `python3 -m http.server 8000` in this folder, then open http://localhost:8000.

## Deploy (GitHub + Cloudflare Pages)

1. Push this folder to a GitHub repository (these files at the repo root).
2. In Cloudflare: Workers & Pages → Create → Pages → Connect to Git, then pick the repo.
3. Build settings: framework preset **None**, build command **empty**, build output directory **/**.
4. Deploy. Every push to the main branch redeploys; other branches get preview URLs.
5. In the Pages project: Custom domains → add `herrell.us` (and `www.herrell.us` if you want it). If the domain's DNS is already on Cloudflare, the records are added for you.

Cloudflare Pages serves `404.html` automatically for missing pages.

Adding a section: create a folder such as `portfolio/index.html`, then edit that section's card in `index.html` (remove its `stamp` once the page is live).

Photo: drop a square image at `assets/photo.jpg` and it replaces the initials in the hero portrait.
