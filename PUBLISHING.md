# Publishing the cards as a website for students

`build_site.js` turns the Hebrew task cards into a self-contained static website.

```bash
node build_site.js                 # everything -> site/
node build_site.js --projects 1,2  # only the projects you have taught
```

Then drag the `site/` folder onto **Cloudflare Pages** (`pages.cloudflare.com`) or
**Netlify** (`app.netlify.com/drop`). Both are free, both give you a link like
`arduino-pbl.pages.dev` to hand to students. No account setup is needed on Netlify Drop;
Cloudflare wants a free account but gives you a stable name you can reuse on every upload.

To preview locally first:

```bash
cd site && python -m http.server 8000     # then open http://127.0.0.1:8000
```

## What ships, and what does not

Only `task_cards_he/` — the 8 projects, 130 cards, about 162 MB.

**Reference cards R1–R7 are deliberately excluded.** They are the teacher's, per the
2026-08-25 review note (*"כרטיסיות R למינהן מיועדות למורה ולא לתלמיד"*), which is also why
the R-references were taken out of the task cards. `build_output/` (the 450 MB of print
bundles) is not part of the site either.

`site/` is gitignored. It is derived output — rebuild it, don't commit it.

## Why the site vendors React

Every card is a `.dc.html` file whose runtime (`support.js`) needs React, ReactDOM and Babel.
In the repo those come from `unpkg.com`, so **a school network that blocks that CDN renders
every card blank** — not degraded, blank. The build downloads all three into `site/vendor/`
and repoints `support.js` at them, so the cards work even with no internet at all. This is
verified: `_sitecheck.js` loads all 139 pages with every non-localhost request aborted and
all of them render.

The only remaining external request is Google Fonts (Rubik). If that is blocked the cards
fall back to a system font and stay perfectly readable, so it is left as-is.

## Rebuild when cards change

The site is a copy. After editing any card, re-run `node build_site.js` and re-upload, or
the students keep seeing the old version. Two things the build handles that a plain copy
would not:

- **Card order.** Filenames sort M10 before M2, so the order comes from `card_nav.js`.
  Project 1 branches (the pick-a-pattern card's `next` is a choice object, not a filename);
  the build follows the default and lists the other branches under "נוסף".
- **Two asset conventions.** Most cards use `./assets/`, but Project 1's wiring figures use
  `../images/`, which would escape the project folder on the site. Those files are copied in
  and the paths repointed.

## Checking it before a lesson

```bash
cd site && python -m http.server 8903 &
node _sitecheck.js
```

Loads every page with the internet blocked and reports any that fail to render or 404.
Run it after a rebuild; it catches a missing figure before a student does.

## Size note

162 MB total, and 60 of the figures are over 1 MB (largest 3.4 MB). Cloudflare and Netlify
gzip automatically, which makes this fine over normal wifi. A USB stick or a plain file
share would not, and the heavy P8 cards would feel slow.
