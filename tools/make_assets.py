#!/usr/bin/env python3
"""
UMBRA brand asset generator — video assets (Task 3) + site images.

Re-runnable: every output is regenerated from the two canonical source marks:
  branding/umbra-avatar-truecrime-icononly.png  (teal crescent-in-circle on flat Ink, 800x800)
  branding/umbra-wordmark-lockup.png            (reference only, for tracking feel)

Outputs
  branding/umbra-watermark-domain.png        transparent watermark, Bone @70%
  branding/umbra-watermark-domain-teal.png   transparent watermark, Teal @80%
  branding/umbra-qr-domain.png               dark QR -> https://umbrastories.studio
  branding/umbra-endcard-1920x1080.png       end-card slate, landscape
  branding/umbra-endcard-1080x1920.png       end-card slate, vertical
  umbrastories-site/assets/mark-teal.png     512x512 transparent teal mark
  umbrastories-site/assets/og.png            1200x630 OpenGraph card
  umbrastories-site/assets/favicon-32.png    32x32
  umbrastories-site/assets/apple-touch-icon.png  180x180
  umbrastories-site/assets/icon-512.png      512x512
  umbrastories-site/favicon.ico              16+32 px ICO

Brand: Ink #0A0A0B bg, Bone #E8E4DF text, Grey #7C838C secondary,
Teal #3F8F87 (TRUE/REAL + submit CTA). No amber in any of these assets.
Type: Poppins (Bold wordmark w/ wide tracking, SemiBold domain/CTA, Regular body).
"""

import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import qrcode
from qrcode.constants import ERROR_CORRECT_H

# ---------------------------------------------------------------- paths / palette
UMBRA = "/Users/rico/Documents/Umbra"
BRANDING = os.path.join(UMBRA, "branding")
SITE = os.path.join(UMBRA, "umbrastories-site")
ASSETS = os.path.join(SITE, "assets")
FONTS = ("/private/tmp/claude-501/-Users-rico-Documents-Umbra/"
         "ab2c3710-00a6-42ff-8f55-522665ce212d/scratchpad/fonts")

INK = (10, 10, 11)        # #0A0A0B
BONE = (232, 228, 223)    # #E8E4DF
GREY = (124, 131, 140)    # #7C838C
TEAL = (63, 143, 135)     # #3F8F87

DOMAIN = "umbrastories.studio"
URL = "https://umbrastories.studio"
CTA_TEXT = "Submit your story"
CTA_DEST = "umbrastories.studio/submit"

os.makedirs(ASSETS, exist_ok=True)


def font(weight, size):
    return ImageFont.truetype(os.path.join(FONTS, f"Poppins-{weight}.ttf"), size)


# ---------------------------------------------------------------- mark extraction
def extract_mark():
    """Key the flat Ink background out of the icon-only avatar.

    The art is exactly two flat colors (Ink bg, Teal mark) with anti-aliased
    edges that are linear blends of the two. For each pixel we recover the
    blend factor t by projecting (pixel - INK) onto (TEAL - INK); the output
    is pure Teal with alpha = t. This "unmixes" the anti-aliasing, so there is
    no dark halo at the edges by construction.

    Returns a full-resolution RGBA image cropped square around the mark.
    """
    src = Image.open(os.path.join(BRANDING, "umbra-avatar-truecrime-icononly.png")).convert("RGB")
    w, h = src.size
    px = src.load()

    dvec = tuple(t - i for t, i in zip(TEAL, INK))
    dlen2 = sum(c * c for c in dvec)

    # RGB is pure Teal EVERYWHERE (even where alpha=0): resampling mixes RGB
    # independently of alpha, so constant RGB guarantees no dark halo after
    # any downscale/composite.
    out = Image.new("RGBA", (w, h), (*TEAL, 0))
    opx = out.load()
    minx, miny, maxx, maxy = w, h, -1, -1
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            t = ((r - INK[0]) * dvec[0] + (g - INK[1]) * dvec[1] + (b - INK[2]) * dvec[2]) / dlen2
            t = max(0.0, min(1.0, t))
            a = round(t * 255)
            if a > 0:
                opx[x, y] = (*TEAL, a)
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y

    # Crop square around content (mark is a circle, so bbox is ~square already).
    side = max(maxx - minx + 1, maxy - miny + 1)
    cx, cy = (minx + maxx) // 2, (miny + maxy) // 2
    half = side // 2 + 1
    return out.crop((cx - half, cy - half, cx + half, cy + half))


def mark_at(mark_full, size):
    """Resize the full-res transparent mark to a square `size` px.

    Pillow premultiplies alpha when resampling RGBA, which leaves rounding
    noise in the RGB of low-alpha edge pixels. The mark is flat-color, so we
    keep only the resampled alpha and rebuild RGB as pure Teal — flat color,
    smooth edges, zero halo."""
    resized = mark_full.resize((size, size), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), (*TEAL, 255))
    out.putalpha(resized.getchannel("A"))
    return out


# ---------------------------------------------------------------- text helpers
def render_line(text, fnt, fill, tracking=0.0):
    """Render one line on a transparent strip of height ascent+descent,
    cropped horizontally to the text width. `tracking` is extra px between
    characters (not after the last one), for the lockup's wide-tracked feel."""
    ascent, descent = fnt.getmetrics()
    widths = [fnt.getlength(c) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    img = Image.new("RGBA", (max(1, int(round(total)) + 4), ascent + descent), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = 2.0
    for c, cw in zip(text, widths):
        d.text((x, 0), c, font=fnt, fill=fill)
        x += cw + tracking
    return img


def make_arrow(height, color, thickness=None):
    """Vector right-arrow (Poppins has no U+2192 glyph). Drawn 4x supersampled."""
    S = 4
    h = height * S
    w = int(h * 1.55)
    t = (thickness or max(2, height // 7)) * S
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cy = h // 2
    head = int(h * 0.46)
    # shaft
    d.line([(t // 2, cy), (w - head // 2 - t, cy)], fill=color, width=t)
    # chevron head
    d.line([(w - head - t, cy - head), (w - t, cy)], fill=color, width=t)
    d.line([(w - head - t, cy + head), (w - t, cy)], fill=color, width=t)
    return img.resize((w // S, h // S), Image.LANCZOS)


def paste_center(canvas, img, cx, top):
    canvas.alpha_composite(img, (int(cx - img.width / 2), int(top)))
    return top + img.height


# ---------------------------------------------------------------- 1) watermarks
def make_watermark(path, color, alpha, shadow=True):
    """Transparent domain watermark ~440px wide for 1080x1920 corner placement.
    Rendered 4x supersampled, then downscaled. Optional very subtle dark
    shadow for legibility on bright footage."""
    S = 4
    pad = 10 * S
    target_text_w = (440 - 20) * S  # 420px text at 1x

    # binary-search font size to hit the target text width
    lo, hi = 10, 400
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if font("SemiBold", mid).getlength(DOMAIN) <= target_text_w:
            lo = mid
        else:
            hi = mid - 1
    fnt = font("SemiBold", lo)
    ascent, descent = fnt.getmetrics()
    tw = int(fnt.getlength(DOMAIN))
    W, H = tw + 2 * pad, ascent + descent + 2 * pad

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((pad, pad + 2 * S), DOMAIN, font=fnt, fill=(0, 0, 0, 140))
        sh = sh.filter(ImageFilter.GaussianBlur(3 * S))
        img.alpha_composite(sh)
    ImageDraw.Draw(img).text((pad, pad), DOMAIN, font=fnt, fill=(*color, alpha))

    img = img.resize((W // S, H // S), Image.LANCZOS)
    img.save(path)
    return img


# ---------------------------------------------------------------- 2) QR code
def make_qr(path, mark_full):
    """QR -> URL, ECC H, Bone modules on Ink, 4-module quiet zone, ~1080px.
    Crescent mark on an Ink circular badge centered at <=22% of width."""
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, border=4)
    qr.add_data(URL)
    qr.make(fit=True)
    n = qr.modules_count + 2 * qr.border          # total modules incl. quiet zone
    box = max(1, round(1080 / n))                  # crisp integer module size
    qr.box_size = box
    img = qr.make_image(fill_color=BONE, back_color=INK).convert("RGBA")
    W = img.width

    # Ink circular badge (supersampled mask for a clean edge)
    badge_d = int(W * 0.22)
    S = 4
    m = Image.new("L", (badge_d * S, badge_d * S), 0)
    ImageDraw.Draw(m).ellipse((0, 0, badge_d * S - 1, badge_d * S - 1), fill=255)
    m = m.resize((badge_d, badge_d), Image.LANCZOS)
    badge = Image.new("RGBA", (badge_d, badge_d), (*INK, 255))
    badge.putalpha(m)

    # crescent mark centered on the badge with an Ink margin ring
    mk = mark_at(mark_full, int(badge_d * 0.78))
    badge.alpha_composite(mk, ((badge_d - mk.width) // 2, (badge_d - mk.height) // 2))

    img.alpha_composite(badge, ((W - badge_d) // 2, (W - badge_d) // 2))
    img.save(path)
    return img


# ---------------------------------------------------------------- 3) end cards
def cta_line(size):
    """'Submit your story  ->  umbrastories.studio/submit' — arrow+dest in Teal."""
    f = font("SemiBold", size)
    a = render_line(CTA_TEXT, f, (*BONE, 255))
    b = render_line(CTA_DEST, f, (*TEAL, 255))
    arrow = make_arrow(int(size * 0.52), (*TEAL, 255))
    gap = int(size * 0.55)
    ascent, _ = f.getmetrics()
    H = a.height
    W = a.width + gap + arrow.width + gap + b.width
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = 0
    img.alpha_composite(a, (x, 0)); x += a.width + gap
    # arrow centered on the lowercase midline (~55% of ascent)
    img.alpha_composite(arrow, (x, int(ascent * 0.55 - arrow.height / 2))); x += arrow.width + gap
    img.alpha_composite(b, (x, 0))
    return img


def make_endcard(path, W, H, mark_full):
    """Centered slate: teal mark, tracked UMBRA in Bone, domain in Grey,
    teal-emphasized submit CTA. Generous negative space, no amber."""
    img = Image.new("RGBA", (W, H), (*INK, 255))
    cx = W / 2
    portrait = H > W

    mark_sz = int(H * 0.155) if not portrait else int(W * 0.21)
    word_sz = int(H * 0.135) if not portrait else int(W * 0.125)
    dom_sz = int(H * 0.040) if not portrait else int(W * 0.040)
    cta_sz = int(H * 0.037) if not portrait else int(W * 0.038)

    wf = font("Bold", word_sz)
    word = render_line("UMBRA", wf, (*BONE, 255), tracking=word_sz * 0.30)
    dom = render_line(DOMAIN, font("Regular", dom_sz), (*GREY, 255))

    if portrait:
        # CTA on two centered lines so type stays large on the narrow frame
        f = font("SemiBold", cta_sz)
        l1 = render_line(CTA_TEXT, f, (*BONE, 255))
        arrow = make_arrow(int(cta_sz * 0.52), (*TEAL, 255))
        dest = render_line(CTA_DEST, f, (*TEAL, 255))
        gap = int(cta_sz * 0.5)
        ascent, _ = f.getmetrics()
        l2 = Image.new("RGBA", (arrow.width + gap + dest.width, dest.height), (0, 0, 0, 0))
        l2.alpha_composite(arrow, (0, int(ascent * 0.55 - arrow.height / 2)))
        l2.alpha_composite(dest, (arrow.width + gap, 0))
        cta_h = l1.height + int(cta_sz * 0.25) + l2.height
    else:
        cta = cta_line(cta_sz)
        cta_h = cta.height

    g1 = int(H * (0.055 if not portrait else 0.032))   # mark -> UMBRA
    g2 = int(H * (0.012 if not portrait else 0.008))   # UMBRA -> domain
    g3 = int(H * (0.105 if not portrait else 0.085))   # domain -> CTA

    total = mark_sz + g1 + word.height + g2 + dom.height + g3 + cta_h
    top = (H - total) / 2

    top = paste_center(img, mark_at(mark_full, mark_sz), cx, top) + g1
    top = paste_center(img, word, cx, top) + g2
    top = paste_center(img, dom, cx, top) + g3
    if portrait:
        top = paste_center(img, l1, cx, top) + int(cta_sz * 0.25)
        paste_center(img, l2, cx, top)
    else:
        paste_center(img, cta, cx, top)

    img.convert("RGB").save(path)  # opaque slate; no alpha needed
    return img


# ---------------------------------------------------------------- 5) OG image
def make_og(path, mark_full):
    W, H = 1200, 630
    img = Image.new("RGBA", (W, H), (*INK, 255))
    cx = W / 2
    word = render_line("UMBRA", font("Bold", 110), (*BONE, 255), tracking=110 * 0.30)
    dom = render_line(DOMAIN, font("Regular", 40), (*GREY, 255))
    mark_sz = 168
    g1, g2 = 34, 6
    total = mark_sz + g1 + word.height + g2 + dom.height
    top = (H - total) / 2
    top = paste_center(img, mark_at(mark_full, mark_sz), cx, top) + g1
    top = paste_center(img, word, cx, top) + g2
    paste_center(img, dom, cx, top)
    img.convert("RGB").save(path)
    return img


# ---------------------------------------------------------------- 6) favicons
def icon_on_ink(size, mark_frac, mark_full):
    img = Image.new("RGBA", (size, size), (*INK, 255))
    mk = mark_at(mark_full, int(size * mark_frac))
    img.alpha_composite(mk, ((size - mk.width) // 2, (size - mk.height) // 2))
    return img


def make_icons(mark_full):
    icon_on_ink(512, 0.74, mark_full).save(os.path.join(ASSETS, "icon-512.png"))
    icon_on_ink(180, 0.64, mark_full).save(os.path.join(ASSETS, "apple-touch-icon.png"))
    icon_on_ink(32, 0.86, mark_full).save(os.path.join(ASSETS, "favicon-32.png"))
    # ICO with 16 + 32 renditions (16 rendered from full-res mark, not the 32)
    i32 = icon_on_ink(32, 0.86, mark_full)
    i16 = icon_on_ink(16, 0.88, mark_full)
    i32.save(os.path.join(SITE, "favicon.ico"), format="ICO",
             append_images=[i16], sizes=[(32, 32), (16, 16)])


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    print("extracting mark ...")
    mark_full = extract_mark()
    mark_at(mark_full, 512).save(os.path.join(ASSETS, "mark-teal.png"))

    print("watermarks ...")
    make_watermark(os.path.join(BRANDING, "umbra-watermark-domain.png"), BONE, 179)       # 70%
    make_watermark(os.path.join(BRANDING, "umbra-watermark-domain-teal.png"), TEAL, 179)  # 70%, matching the neutral version per spec

    print("qr ...")
    make_qr(os.path.join(BRANDING, "umbra-qr-domain.png"), mark_full)

    print("end cards ...")
    make_endcard(os.path.join(BRANDING, "umbra-endcard-1920x1080.png"), 1920, 1080, mark_full)
    make_endcard(os.path.join(BRANDING, "umbra-endcard-1080x1920.png"), 1080, 1920, mark_full)

    print("og + icons ...")
    make_og(os.path.join(ASSETS, "og.png"), mark_full)
    make_icons(mark_full)
    print("done")
