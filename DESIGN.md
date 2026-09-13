# DESIGN.md — umbrastories.studio

The Four Decisions for this site, written down so no session re-derives the
median. Brand rules in `styles.css` and the workflows in `README.md` still
govern; this file records why the page looks the way it does. Tell IDs (T5,
M2, O2 and so on) refer to Rico's design reference, `ai-slop-tells.md`.

Drafted in Phase 1 of the September 2026 home-page brief. Items marked
**[open]** wait on Rico.

## 1. Reference

An eclipse. The umbra is the darkest part of a shadow, and the page sits
inside it: near-black ground, one light source (the teal moon-glow already
behind the mark), and nothing else that glows.

Secondary references, and what to take from each:

- thisiscriminal.com: respectful true crime. Symbolic imagery instead of
  crime-scene photos, a measured tone. Leave the episode-card grid.
- vault.fbi.gov: the record as texture. Dates, places, plain lists. Leave the
  seals and anything that looks official.
- A default Linktree page is the anti-reference: a stack of identical buttons.

## 2. Color

Origin: the UMBRA brand spec, the same palette as the channel art.

| Token | Hex | Meaning |
|---|---|---|
| `--ink` | `#0A0A0B` | Ground |
| `--bone` | `#E8E4DF` | Primary text |
| `--grey` | `#7C838C` | Secondary text and metadata |
| `--teal` | `#3F8F87` | It happened: True Crime, Real Stories |
| `--amber` | `#C2803A` | It's fiction: Horror Fiction |
| `--card-bg` | `#121216` | Surfaces (neutral only) |
| `--card-bg-hover` | `#18181F` | Surface hover |
| `--card-border` | `#202026` | Hairlines |
| `--card-border-hover` | `#2E2E38` | Hairline hover |

Rules:

- Teal and amber never appear inside one element. Amber never sits near true
  crime or real stories. The color is the page's central idea: it tells you
  whether a story happened.
- Pillar color appears as a thin rule, the platform icon, and the language
  pill. Surfaces stay neutral. No colored card fills.
- Measured contrast (WCAG, computed): bone/ink 15.6, grey/ink 5.2,
  grey/card-bg 4.9, teal/ink 5.2, amber/ink 6.1, ink/teal 5.2. Bone/teal is 3.0
  and bone/amber is 2.6, both fail, so a teal or amber fill always carries ink
  text, and teal or amber type only sits on ink or `--card-bg`.
- Dark-only, on purpose (`color-scheme: dark`). The site is the inside of a
  shadow; there is no light theme to build.
- **[open]** The brand comment in `styles.css` assigns bone to text and ink to
  the ground. One proposed home-page direction inverts that in exactly one
  place (a bone surface carrying ink text at the Submit section). That is a
  brand-rule change, not a styling choice, and it needs Rico's yes before it
  is built. If approved, bone as a ground is allowed in that one section and
  nowhere else, and it carries ink text only.
- The `.card` background hardcodes `#131316`; it becomes `var(--card-bg)`.

## 3. Type

Keep Poppins (400, 600, 700). The one-sentence reason: it is the face of the
end-cards, watermarks, and OG image (`tools/make_assets.py` renders them in
Poppins Bold, SemiBold, and Regular), so a tap from a video lands on the same
letterforms. **[open: confirm]** that the video thumbnails use Poppins too;
if they do not, the reason weakens and the decision is revisited. No
replacement has a sentence that strong; swapping to a fashionable face would
reset the clock rather than fix anything.

Poppins has no variable version and its 400 weight runs thin on ink, so the
type gets its range from setting, not from a second family (T3):

- Body at 0.95–1rem, line-height 1.55–1.6. Secondary text never below 0.85rem
  on ink.
- Display at 700, line-height 1.1, tracking slightly negative. A real size
  cliff between the wordmark and everything under it.
- Poppins figures are proportional. Where figures must align in columns, use
  `font-variant-numeric: tabular-nums` first.

Second face: Chivo Mono 400, and only where it has a job: aligned record
metadata (a year · place · title list, the case-page facts grid, the sources
list). It is one more Google Fonts request from the same origin, Latin
subset only, and it is loaded only on pages that set aligned figures. The
home page qualifies only if its Case Files section sets year and place in
columns.

Labels (T5), scoped to this pass: on the home page, no tracked uppercase
labels except the logotype "UMBRA", which stays tracked because it is a
logotype, not a label. Pillar and section headings on the home page are
sentence case. Case pages keep their one eyebrow ("Case File · True Crime").
The other tracked styles in the shared stylesheet (`.fact-label`,
`.section-h` on case pages, `.feat-label` on category pages) are out of scope
here and get their own pass. **[open: confirm]**

Excluded, and why: Inter, Geist, Roboto, Open Sans, Instrument Serif, Playfair
Display (reference defaults); Fraunces, Newsreader, IBM Plex (Rico's other
brands). Spanish glyphs (á é í ó ú ñ ¿ ¡) are in the Latin block of both
chosen faces; Spanish strings are marked `lang="es"`.

## 4. Layout intent

A link-in-bio page first. The visitor tapped a bio link on a phone, often at
night, and wants the right UMBRA channel in their language. The page's second
job is Submit.

- The first channel link is visible without scrolling at 390×844. Measured
  on the live site: the first channel row starts at 468px, so the floor holds
  today. The category pill row costs about 102px with its margins and the
  language filter wraps to two rows at 390px; moving the pill row to the
  footer and keeping the filter on one row buys headroom for rows that carry
  metadata, so the floor still holds after the redesign.
- One thumb-width column on mobile. That is the one-sentence reason it stays
  centered (L1). On desktop the page is not a scaled-up phone: the column
  widens into two, and the one scroll moment may pin for up to one viewport.
- Rows, not buttons. Hairline separators; platform, language, and the latest
  upload as metadata; the whole row is one tap target of at least 44px.
- Sections exist only where there is real content: header, channels, Case
  Files, Submit, footer. No stats, no testimonials, no template spine.
- Spacing on a 4px base, ranked: tight inside a pillar, open between sections.

## Shape

Two radius levels (O2): 999px for language pills and the toast, 12px for
containers and buttons. Everything else is a hairline or square. The
one-sided radius on `.disclaimer` and the 8px on small cells collapse into
these two. Those are shared tokens, so the collapse touches category and
case pages; they get checked after the change, like every shared edit.

## Motion

One scroll-linked moment per page, driven by scroll position
(`animation-timeline: view()` with a small IntersectionObserver fallback). No
parallax, no scroll-reveal, no animation libraries.

Hover changes border and background only. No lift (`translateY`), no
`scale()`, on cards, the CTA, or the mark. The only glow is the moon-glow.
`prefers-reduced-motion: reduce` shows the moment's end state, static.

## Copy

Calm, exact, a little cold. English then Spanish, joined with " · ". Each
pillar keeps its register: True Crime is records, dates, places, no
speculation; Horror Fiction is stories for the dark, never presented as real;
Real Stories are told by the people who lived them.

Em dashes under one per 150 words. When a literal phrase is available, use
it. No invented numbers. The Submit section states only what the form says:
we may narrate it, you keep the copyright, you choose how you're credited.

## Deliberate exceptions (slop-ok registry)

- `O5/C5` the moon-glow (`body::before` and the mark's drop-shadow): the page's
  single light source and its one oddity.
- `C4` dark-only: the reference is a shadow.
- `T5` one tracked eyebrow on case pages; the logotype.

## Refuse list

See the brief, section 6. In short: no identical-button stacks, no gore or
victim imagery, no teal-with-amber, no invented numbers, no meshes, particles,
grain, parallax, lifts, scales, splash screens, embeds, or trackers.
