
"""
Target AI Ad Agent
Minimal prototype for website analysis and targeted advertising content.
"""

from urllib.request import Request, urlopen
from html.parser import HTMLParser
from urllib.parse import urlparse
import json
import re
import sys


class WebsiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = False
        self.in_title = False
        self.title_text = []
        self.text = []
        self.links = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self.in_title = True
        if tag.lower() == "a":
            self.links += 1

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self.in_title:
            self.title_text.append(text)
        self.text.append(text)


def analyze_website(url):
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Please provide a valid HTTP or HTTPS URL.")

    request = Request(
        url,
        headers={"User-Agent": "TargetAIAdAgent/0.1"}
    )

    with urlopen(request, timeout=15) as response:
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type.lower():
            raise ValueError("The URL does not return an HTML page.")
        html = response.read(1_000_000).decode("utf-8", errors="replace")

    parser = WebsiteParser()
    parser.feed(html)

    page_text = " ".join(parser.text)
    words = re.findall(r"\b[\w'-]+\b", page_text.lower())
    word_counts = {}

    for word in words:
        if len(word) > 3:
            word_counts[word] = word_counts.get(word, 0) + 1

    keywords = sorted(
        word_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )[:10]

    return {
        "url": url,
        "domain": parsed.hostname,
        "title": " ".join(parser.title_text) or "No page title found",
        "word_count": len(words),
        "links_found": parser.links,
        "top_keywords": [
            {"keyword": word, "count": count}
            for word, count in keywords
        ],
        "advertising_ideas": [
            f"Create content focused on {word}"
            for word, _ in keywords[:3]
        ]
    }


if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else "https://healthsportvoyageai.com"

    try:
        print(json.dumps(
            analyze_website(target_url),
            ensure_ascii=False,
            indent=2
        ))
    except Exception as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False, indent=2))
        sys.exit(1)
