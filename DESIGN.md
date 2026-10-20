# DESIGN.md — umbrastories.studio

The Four Decisions for this site, written down so no session re-derives the
median. Brand rules in `styles.css` and the workflows in `README.md` still
govern; this file records why the page looks the way it does. Tell IDs (T5,
M2, O2 and so on) refer to Rico's design reference, `ai-slop-tells.md`.

Drafted in Phase 1 of the September 2026 home-page brief. Updated 19 Oct
2026 after Rico's decisions: **Direction B, "The Ledger"**, bone ground in
the Submit section only, Metamorphous headings, and every remaining
[confirm] item as recommended in `umbra-phase1-plan.md`.

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
- **Resolved (Rico, 19 Oct):** bone may be a ground in exactly one place,
  the home page's Submit section ("the lit room"), and there it carries ink
  text only. Teal appears there only as a hairline, because teal type on bone
  fails contrast. Bone stays text everywhere else.
- The `.card` background hardcodes `#131316`; it becomes `var(--card-bg)`.

## 3. Type

Three faces, each with one job (Rico, 19 Oct):

- **Metamorphous** for headings: the wordmark, ledger and section headings,
  case titles. It is the face of every Short thumbnail on all four channels,
  so a tap from a video lands on the same letterforms. It ships one weight
  (400); headings set it at 400 and never fake a bold.
- **Poppins** (400, 600, 700) for body text, rows, buttons and metadata. Its
  400 runs thin on ink, so body sits at 0.95–1rem, line-height 1.55–1.6, and
  secondary text never goes below 0.85rem on ink. End-cards, watermarks and
  the OG image (`tools/make_assets.py`) still use Poppins.
- **Chivo Mono** 400 only where figures align: the Case Files record (year
  column) on the home page, and later the case-page facts grid and sources.
  Latin subset, same Google Fonts request.

All three are loaded in one Google Fonts request. Spanish glyphs (á é í ó ú
ñ ¿ ¡) are in the Latin block of each; Spanish strings carry `lang="es"`.

Labels (T5): on the home page, no tracked uppercase labels except the
logotype "UMBRA". Ledger, pillar and section headings are sentence case.
Case pages keep their one eyebrow ("Case File · True Crime"). The other
tracked styles in the shared stylesheet (`.fact-label`, `.section-h`,
`.feat-label`) get their own pass.

Excluded: Inter, Geist, Roboto, Open Sans, Instrument Serif, Playfair
Display (reference defaults); Fraunces, Newsreader, IBM Plex (Rico's other
brands).

## 4. Layout intent: The Ledger

A link-in-bio page first. The visitor tapped a bio link on a phone, often at
night, and wants the right UMBRA channel in their language. The page's
second job is Submit.

- **The color rule is the layout.** Channels sit in two ledgers that answer
  one question, did it happen: **It happened · Sucedió** (teal: True Crime,
  Real Stories) and **It's fiction · Es ficción** (amber: After Dark,
  Nocturno). A small pillar heading inside the teal ledger keeps True Crime
  and Real Stories distinct. The render groups `CHANNELS` by `accent`, so a
  one-line add still works.
- **Real Stories is shown as starting.** Its channels carry `live: false`
  until the first upload; the pillar shows its bios and "Starts with your
  stories · Empieza con tus historias", linking to Submit. Flip `live` in one
  line when a channel goes live.
- The first channel link is visible without scrolling at 390×844. The
  category pill row moved to the footer; the language filter sits on one
  row at 390px.
- One thumb-width column on mobile, which is why it stays centered (L1). At
  900px and up the two ledgers sit side by side with a hairline between
  them, the one place the page stops being a phone scaled up.
- Rows, not buttons. Hairline separators; platform, language, and the latest
  upload as metadata; the whole row is one tap target of at least 56px.
- Case Files is a record: year in Chivo Mono, title, place. Teal only.
- Sections exist only where there is real content: header, ledgers, Case
  Files, Submit, footer. No stats, no testimonials, no embeds.
- Spacing on a 4px base, ranked: tight inside a ledger, open between
  sections.
- Display names follow each platform: YouTube channels keep "Umbra - …";
  TikTok shows "Umbra Casos", "Umbra After Dark"; Cold Case TikTok keeps
  "Umbra - True Crime".

## Shape

Two radius levels (O2): 999px for language pills and the toast, 12px for
containers and buttons. Everything else is a hairline or square. The
one-sided radius on `.disclaimer` and the 8px on small cells collapse into
these two. Those are shared tokens, so the collapse touches category and
case pages; they get checked after the change, like every shared edit.

## Motion

One scroll-linked moment: **the lit room.** As the Submit section crosses
the viewport, its ground comes up from ink to bone like a dimmer and its
text turns from bone to ink, finishing before the section is fully in view.
It is driven by `animation-timeline: view()`, with a small
IntersectionObserver fallback that does the same with a transition. With
`prefers-reduced-motion: reduce`, without JavaScript, or without either
mechanism, the section is simply bone with ink text. No pinning.

No parallax, no scroll-reveal, no animation libraries. Hover changes border
and background only: no lift, no scale, no hover glow. The only glow is the
moon-glow.

## Copy

Calm, exact, a little cold. English then Spanish, joined with " · ". Each
pillar keeps its register: True Crime is records, dates, places, no
speculation; Horror Fiction is stories for the dark, never presented as real;
Real Stories are told by the people who lived them.

Em dashes under one per 150 words. When a literal phrase is available, use
it. No invented numbers. The Submit section states only what the form says:
we may narrate it, you keep the copyright, you choose how you're credited.
It does not claim long-form episode features (sources block, read-aloud
disclaimer, "what doesn't hold") until those are confirmed in the
published videos; "Real cases come with their sources" points at Case
Files. No hotlinked thumbnails or embeds.

## Deliberate exceptions (slop-ok registry)

- `O5/C5` the moon-glow (`body::before` and the mark's drop-shadow): the page's
  single light source and its one oddity.
- `C4` dark-only: the reference is a shadow.
- `T5` one tracked eyebrow on case pages; the logotype.

## Refuse list

See the brief, section 6. In short: no identical-button stacks, no gore or
victim imagery, no teal-with-amber, no invented numbers, no meshes, particles,
grain, parallax, lifts, scales, splash screens, embeds, or trackers.
