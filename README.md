
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

2. Sanal ortam oluşturun ve etkinleştirin:

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

3. Bağımlılıkları yükleyin.

Seçenek A — Standart pip yöntemi:

```bash
pip install -e .
```

Seçenek B — `uv` kullanarak (önerilir, daha hızlı ve proje yönetimi içerir):

1. `uv` yükleyin (eğer yüklü değilse):

```bash
pip install uv
```

2. Proje sanal ortamını oluşturun:

```bash
uv venv
```

3. Kilitli bağımlılık dosyanız varsa senkronize edin veya doğrudan proje bağımlılıklarını yükleyin:

```bash
uv pip sync
# veya
uv pip install -e .
```

## Çalıştırma

Projeyi lokal olarak başlatmanın birkaç yolu vardır.

Standart yöntem:

```bash
python main.py
```

`uv` ile çalıştırma (izole, hızlı ve tavsiye edilen yöntem):

```bash
# Doğrudan script olarak
uv run python main.py

# veya tek dosya script için (uygunsa)
uv run main.py
```

Ardından tarayıcıda `http://127.0.0.1:5000` adresini açın.

## Kullanım

- Sol alandaki textarea'ya Markdown yazın veya yapıştırın.
- Sağ üstteki `Theme` seçicisinden bir tema seçin (ör. `light`, `dark`, `ocean`, `forest`...).
- `Convert` butonuna basın.
- Sağ panelde `Preview` veya `HTML Code` görünümleri arasında geçiş yapabilirsiniz.
- Header içindeki ayar butonuyla (güneş/ay ikonu) sayfa seviyesinde dark/class tabanlı tema geçişi yapılır; tercih `localStorage`'da saklanır.

### Tema eklemek

Yeni bir tema eklemek için `app/static` içine `blog-<tema>.css` adında bir CSS dosyası ekleyin ve `base.html` içindeki `<select id="theme-selector">` bölümüne bir `<option value="<tema>">` ekleyin.

## Teknik Notlar

- Markdown dönüşümü `app/routes/home.py` içindeki `/convert` endpoint'i ile sağlanır. Endpoint, gelen markdown'u HTML'e çevirir ve seçilen temaya ait CSS dosyasını okuyup `<style>` içinde sararak JSON ile döner.
- CSS dosyaları `app/static` klasöründedir.
- Tailwind CDN kullanılırken `dark:` sınıflarının class tabanlı çalışması için `base.html` içinde `@custom-variant dark (&:where(.dark, .dark *));` tanımlaması eklendi. Bu sayede header'daki toggle ile `html` elementine eklenen `dark` sınıfı, `dark:` prefiksli stilleri tetikler.
- Güvenlik: HTML üretiminde ek güvenlik gerekiyorsa (kullanıcı girdisi), `bleach` veya benzeri bir kütüphane ile sanitizasyon eklemeniz önerilir. `pyproject.toml` içinde `bleach` bağımlılığı listelenmiştir fakat şu anki kodda otomatik sanitizasyon yapılmamaktadır.

## Geliştirme

- Kod yapısı:
	- `main.py` — uygulamayı çalıştırır
	- `app/__init__.py` — Flask uygulaması ve blueprint kayıtları
	- `app/routes/home.py` — ana route'lar ve `/convert` endpoint
	- `app/templates/` — Jinja2 şablonları (`base.html`, `partials/_header.html`)
	- `app/static/` — temalar (CSS)

## Hata Ayıklama & Sık Karşılaşılan Sorunlar

- Tema değişiklikleri çalışmıyorsa tarayıcı konsolunu kontrol edin; `localStorage`'a `theme` değeri yazılıyor mu bakın.
- Eğer `dark:` stilleri tetiklenmiyorsa `base.html` içinde `@custom-variant` tanımının korunup korunmadığını ve Tailwind CDN sürümünü kontrol edin.

---

Dosya: [app/templates/base.html](app/templates/base.html)

`, güncelleme yapmak isterseniz yardımcı olabilirim.`
