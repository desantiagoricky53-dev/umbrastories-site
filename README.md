# umbrastories-site

Static link-in-bio site + category pages + redirects for **UMBRA** (umbrastories.studio), a
bilingual horror / true-crime story network. Plain HTML/CSS/JS, no build step,
hosted free on **GitHub Pages** with a custom domain.

- `index.html` — link-in-bio landing page (channel cards rendered from one JS array + category navigation)
- `true-crime/` — dedicated landing page for True Crime & Casos Reales (Teal accent)
- `horror-fiction/` — dedicated landing page for Horror Fiction & Ficción de Terror (Amber accent)
- `real-stories/` — dedicated landing page for Real Stories & Historias Reales (Teal accent)
- `styles.css` — shared stylesheet (index, category pages, 404, case pages)
- `404.html` — branded 404 (GitHub Pages serves this automatically)
- `submit/ yt/ tt/ casos/ nocturno/ afterdark/ firsthand/ testimonios/` — meta-refresh redirect stubs
- `cases/hinterkaifeck/` — first episode source page; doubles as the case-page template
- `assets/` — brand mark, OG image, favicons (produced by the asset pipeline)
- `docs/spacemail-aliases.md` — manual email-alias setup steps for Spaceship
- `CNAME`, `.nojekyll`, `robots.txt`, `sitemap.xml` — hosting/SEO plumbing

Brand rules live in `styles.css` (top comment). The short version: Ink `#0A0A0B`
background, Bone `#E8E4DF` text, Grey `#7C838C` secondary, Teal `#3F8F87` for
true/real pillars, Amber `#C2803A` for fiction pillars — and **never both accents
inside one card or element**.

---

## The update workflows

### 1. Add a channel (two edits: index + its category page)

Open `index.html` and find the `CHANNELS` constant at the top of the inline
`<script>`. Add **one line** — the `TODO` comments already mark where each
pending TikTok goes:

```js
{ pillar: "fiction", accent: "amber", platform: "tiktok", name: "Umbra - Nocturno", url: "https://tiktok.com/@UmbraNocturno", lang: "ES" },
```

Field cheat-sheet:

| Field | Values |
|---|---|
| `pillar` | `"truecrime"` \| `"fiction"` \| `"real"` |
| `accent` | `"teal"` (true/real) \| `"amber"` (fiction) — never mixed |
| `platform` | `"youtube"` \| `"tiktok"` |
| `lang` | `"EN"` \| `"ES"` |

Then add the matching card in the corresponding category page
(`true-crime/`, `horror-fiction/`, or `real-stories/index.html` — their card
lists are hardcoded HTML, copy an existing `<a class="card ...">` block).
Commit, push. Done. (The `<noscript>` fallback in `index.html` lists only the
flagship channels on purpose and never needs updating.)

### 2. Add a redirect (copy a stub folder)

```bash
cp -r yt newpath        # copy any existing stub folder
```

Open `newpath/index.html` and replace the target URL in **three** places:
the `<meta http-equiv="refresh">` tag, the visible `Continue →` link, and the
`location.replace(...)` call. Commit, push. The redirect is live at
`umbrastories.studio/newpath`.

### 3. Add a case page (copy the template)

```bash
cp -r cases/hinterkaifeck cases/<new-slug>
```

Open `cases/<new-slug>/index.html` — every editable slot is marked with an
`EDIT` HTML comment (title, meta line, summary paragraph, sources, watch link,
plus `<title>`/description/canonical in `<head>`). Keep the unsolved-case
disclaimer verbatim where it applies. Finally, add the new URL to
`sitemap.xml`. True-crime case pages use **teal** accents only.

---

## Deployment (GitHub Pages)

GitHub user: `desantiagoricky53-dev`.

1. Create a repo named `umbrastories-site` on GitHub, push this folder to the
   default branch (`main`).
2. Repo → **Settings → Pages** → Source: **Deploy from a branch**, branch
   `main`, folder `/ (root)`.
3. Still in Pages settings, set **Custom domain** to `umbrastories.studio`
   (the `CNAME` file in this repo keeps it pinned across deploys).
4. Wait for the TLS certificate to be issued (can take up to ~24 h after DNS
   propagates), then tick **Enforce HTTPS**.

### DNS (at Spaceship)

> **⚠️ MAIL IS LIVE ON THIS DOMAIN — DO NOT TOUCH MAIL RECORDS. ⚠️**
> Spacemail runs on umbrastories.studio with five active mailboxes.
> **Never delete, replace, or "clean up" any MX, SPF, DKIM, or TXT record.**
> The records below are **ADDED ALONGSIDE** everything that already exists.
> If a tool or wizard offers to "replace existing records" — refuse.

Add these records in the Spaceship DNS panel:

| Type | Host | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `desantiagoricky53-dev.github.io` |

### Post-deploy verification checklist

- [ ] `https://umbrastories.studio` loads over HTTPS (no cert warning)
- [ ] `https://www.umbrastories.studio` loads over HTTPS
- [ ] `https://umbrastories.studio/submit` lands on the Google Form
- [ ] Spot-check category pages (`/true-crime/`, `/horror-fiction/`, `/real-stories/`)
- [ ] Spot-check channel redirects (e.g. `/yt`, `/casos`, `/afterdark`)
- [ ] `/cases/hinterkaifeck/` renders with styling and key facts grid
- [ ] A bogus URL (e.g. `/nope`) shows the branded 404
- [ ] **Email still works**: send a message *to* and *from* a
      `@umbrastories.studio` mailbox and confirm both arrive

If email breaks after a DNS change, a mail record was deleted — restore the
MX/SPF/DKIM/TXT records in Spaceship immediately.

---

## Local preview

Absolute paths (`/styles.css`, `/assets/...`) are used throughout, so preview
with a local server from the repo root — not `file://`:

```bash
python3 -m http.server 8080
# open http://localhost:8080
```

## Deliberately out of scope

No analytics, no trackers, no cookies. Newsletter is a commented-out
placeholder in `index.html`. The only external requests on any page are the
Google Fonts loads for Poppins.
