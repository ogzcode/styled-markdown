
# MD to HTML

Basit bir Flask uygulaması: kullanıcıdan alınan Markdown metnini HTML'e çevirir ve seçilen tema (CSS) ile birlikte önizleme sağlar.

## Özeti

Bu proje, Markdown girdisini alıp sunucu tarafında `markdown` kütüphanesi ile HTML'e çevirir ve temaya uygun CSS'i `app/static/blog-*.css` dosyalarından okuyarak sonucu istemci tarafına gönderir. Kullanıcı arayüzü Tailwind ile oluşturulmuş olup, tema seçici ve sayfa içi dark/light toggle desteği içerir.

## Özellikler

- Markdown -> HTML dönüşümü (code highlight, tablolar, fenced code vs. destekler)
- Tema seçici (farklı `blog-*.css` dosyaları)
- Dark / Light toggle (localStorage ile tercih saklama)
- Önizleme iframe ve ham HTML görüntüleme

## Gereksinimler

- Python 3.13 veya üzeri
- Bağımlılıklar pyproject.toml içinde listelenmiştir: `flask`, `markdown`, `bleach`, `python-dotenv`.

## Kurulum

1. Depoyu klonlayın ve dizine girin:

```bash
git clone <repo-url>
cd md-to-html
```

# MD to HTML

Simple Flask app that converts user-provided Markdown into HTML and returns a preview styled with a selected theme CSS.

## Overview

This project converts Markdown on the server using the `markdown` Python package and applies a theme CSS from `app/static/blog-*.css`. The UI is built with Tailwind and includes a theme selector and a page-level dark/light toggle.

## Features

- Markdown -> HTML conversion (supports code highlighting, tables, fenced code blocks, etc.)
- Theme selector (multiple `blog-*.css` files)
- Dark / Light toggle stored in `localStorage`
- Preview iframe and raw HTML view

## Requirements

- Python 3.13 or newer
- Project dependencies are listed in `pyproject.toml` (e.g., `flask`, `markdown`, `bleach`, `python-dotenv`).

## Installation

1. Clone the repository and change directory:

```bash
git clone <repo-url>
cd md-to-html
```

2. Create and activate a virtual environment.

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux / macOS:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies.

Option A — standard pip method:

```bash
pip install -e .
```

Option B — using `uv` (recommended for faster environment management):

```bash
pip install uv
uv venv
uv pip sync
# or
uv pip install -e .
```

## Running

Start the app locally:

```bash
python main.py
```

Or with `uv`:

```bash
uv run python main.py
```

Open `http://127.0.0.1:5000` in your browser.

## Usage

- Enter or paste Markdown into the left textarea.
- Choose a theme from the `Theme` selector (e.g., `light`, `dark`, `ocean`, `forest`).
- Click `Convert`.
- Switch between `Preview` and `HTML Code` in the right panel.
- Use the header toggle to switch page-level `dark` class (preference saved in `localStorage`).

### Adding a Theme

Add a CSS file named `blog-<theme>.css` to `app/static` and add a matching `<option value="<theme>">` in `base.html`'s theme selector.

## Technical Notes

- Markdown conversion happens in the `/convert` endpoint in `app/routes/home.py`. The endpoint converts Markdown to HTML and applies the selected theme CSS inline before returning JSON.
- CSS files live under `app/static`.
- Tailwind CDN is used; `base.html` defines `@custom-variant dark (&:where(.dark, .dark *));` so class-based `dark` toggling works with `dark:` utilities.
- Security: if user-provided HTML is rendered, consider sanitizing with `bleach` or similar.

## Development

- Project structure:
	- `main.py` — application entry point
	- `app/__init__.py` — Flask app and blueprint registration
	- `app/routes/home.py` — main routes and `/convert` endpoint
	- `app/templates/` — Jinja2 templates (`base.html`, `partials/_header.html`)
	- `app/static/` — theme CSS files

## Debugging & Common Issues

- If theme changes don't appear, check the browser console and verify `localStorage` contains the `theme` key.
- If `dark:` utilities are not taking effect, ensure `@custom-variant` is present in `base.html` and the Tailwind CDN version supports it.
- **`/ai-css` endpoint:** Now accepts an optional `html` parameter. When provided, the endpoint generates CSS (via Gemini), strips markdown fences, applies the CSS inline to the supplied HTML, and returns both the raw CSS and the inline-styled HTML. If `html` is omitted, it returns only the generated CSS.
- **Notes & limitations:** Complex selectors, pseudo-elements, or some advanced CSS features may be ignored; invalid selectors are safely skipped. Existing inline styles are preserved and merged with generated styles. Consider sanitizing user HTML (e.g., with `bleach`) if exposing to untrusted input.

If you want this summary translated to Turkish or integrated into a different documentation file, tell me where to place it.
