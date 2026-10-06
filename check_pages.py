from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.ids = [], set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag in ('a', 'link') and 'href' in attrs:
            self.links.append(attrs['href'])


root = Path(__file__).parent / 'dist'
pages = {p.name: Page(p.read_text()) for p in root.glob('*.html')}
for name, page in pages.items():
    for href in page.links:
        url = urlsplit(href)
        if url.scheme or url.netloc:
            continue
        target = url.path or name
        assert (root / target).is_file(), (name, href)
        if url.fragment:
            assert url.fragment in pages[target].ids, (name, href)
print(f'PASS: links and section anchors across {len(pages)} pages.')
