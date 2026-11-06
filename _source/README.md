# Syarif Lazuardi Photographs: source

The site is one static page (`index.html`) plus `assets/img/`. Open `index.html` in a browser to view it, or upload the folder to any static host (Netlify, GitHub Pages, Vercel, cPanel).

## Your details
In `build.py`, `SITE` holds your name, the names that cycle under the portrait, email, Instagram and LinkedIn.

## Changing the photographs or the sequence
1. Put your original JPEGs (and portrait.png) in a folder.
2. Edit `MAP` in `images.py` (plate id to filename), then run
   `python3 images.py <originals folder> ../assets/img meta.json`
3. Edit `PHOTOS` (set and title), `EXIF`, `HOME` and `GALLERY` in `build.py`.
   Each spread is a list of placements on a 12-column grid, for example
   `("img", "s04", "1 / 8", "start", "0", "full")` or `("pair", ["s13","s14"], "1 / 13", "start", "0")`.
4. Run `python3 build.py meta.json ../index.html template.html`

Requires Python 3 with Pillow (`pip install pillow`).
