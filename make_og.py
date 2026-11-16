#!/usr/bin/env python3
"""og.png 1200x630 — Haven Express Lounge (2x supersample).
Truck-to-storefront identity: espresso ink ground, awning stripes up top,
ember accents, cream wordmark. Shop identity only — zero builder tokens."""
from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 1200, 630
S = 2
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

INK = (23, 18, 13); INK2 = (36, 26, 18)
CREAM = (244, 234, 217); EMBER = (255, 93, 36); GOLD = (231, 176, 79)
MUTE = (168, 154, 134)

def font(paths, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in paths:
            p = b + n
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size)
                except Exception: pass
    return ImageFont.load_default()

sans  = lambda s: font(["Avenir Next Bold.ttf", "AvenirNext-Bold.ttf", "HelveticaNeue-Bold.ttf", "Arial Bold.ttf"], s*S)
sansm = lambda s: font(["Avenir Next Medium.ttf", "AvenirNext-Medium.ttf", "HelveticaNeue.ttc", "Arial.ttf"], s*S)
serif = lambda s: font(["Georgia Bold.ttf", "Times New Roman Bold.ttf"], s*S)

img = Image.new("RGB", (W*S, H*S), INK)
d = ImageDraw.Draw(img, "RGBA")

# vertical gradient ink -> deeper at bottom
for y in range(0, H*S, 8):
    t = y / (H*S)
    r = int(INK2[0] + (INK[0]-INK2[0])*t); g = int(INK2[1] + (INK[1]-INK2[1])*t); b = int(INK2[2] + (INK[2]-INK2[2])*t)
    d.rectangle([0, y, W*S, y+7], fill=(r, g, b))

def P(x, y): return (x*S, y*S)

# --- awning stripe band across the very top (the truck motif) ---
stripe_h = 46
x = 0; i = 0
while x < W:
    col = EMBER if i % 2 == 0 else CREAM
    d.rectangle([P(x, 0), P(x+38, stripe_h)], fill=col)
    x += 40; i += 1
# scalloped bottom edge: alternating arcs bumping down from the band
arc = 22
for k in range(0, W, 40):
    d.pieslice([P(k, stripe_h-arc), P(k+40, stripe_h+arc)], 0, 180, fill=(EMBER if (k//40) % 2 == 0 else CREAM))
# shadow under awning
d.rectangle([P(0, stripe_h+arc), P(W, stripe_h+arc+10)], fill=(0, 0, 0, 90))

L = 80
# kicker
d.text(P(L, 130), "F O O D - T R U C K  F A V O R I T E   ·   F I R S T   B R I C K - A N D - M O R T A R", font=sansm(17), fill=GOLD)
# wordmark
d.text(P(L, 168), "HAVEN EXPRESS", font=sans(84), fill=CREAM)
# "LOUNGE" ember, tracked
def tracked(text, x, y, fnt, fill, sp):
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + sp*S
    return x
xend = tracked("L O U N G E", L+2, 305, sans(40), EMBER, 6)
# thin rule under wordmark
d.line([P(L, 385), P(xend+30, 385)], fill=(231, 176, 79, 160), width=int(2*S))
# address + hours lines
d.text(P(L, 410), "1217 Leavenworth Street  ·  Old Market  ·  Omaha, NE 68102", font=sansm(24), fill=CREAM)
d.text(P(L, 452), "Open Tue–Thu 3–9 PM  ·  Fri–Sat 3–11:30 PM  ·  (402) 210-4610", font=sansm(21), fill=MUTE)

# --- right-side ember ring ornament (decor, behind nothing on the right field) ---
cx, cy, rr = 1010, 480, 118
d.ellipse([P(cx-rr, cy-rr), P(cx+rr, cy+rr)], outline=(255, 93, 36, 200), width=int(3*S))
d.ellipse([P(cx-rr-26, cy-rr-26), P(cx+rr+26, cy+rr+26)], outline=(231, 176, 79, 90), width=int(2*S))
# door glyph inside ring
d.pieslice([P(cx-46, cy-70), P(cx+46, cy+62)], 180, 360, fill=None, outline=CREAM, width=int(4*S))
d.rectangle([P(cx-46, cy-4), P(cx+46, cy+62)], fill=None, outline=CREAM, width=int(4*S))
d.ellipse([P(cx+24, cy+22), P(cx+34, cy+32)], fill=CREAM)
# "NOW OPEN" stamp inside ring top
d.text(P(cx - d.textlength("N O W  O P E N", font=sans(17))/2, cy-rr-40), "N O W  O P E N", font=sans(17), fill=GOLD)

img = img.resize((W, H), Image.LANCZOS)
img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")
