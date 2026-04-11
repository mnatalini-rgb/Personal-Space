from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
    def handle_starttag(self, tag, attrs):
        if tag not in ['meta', 'link', 'br', 'hr', 'img', 'input', 'col', 'path', 'rect', 'circle', 'line', 'polygon', 'polyline', 'stop', 'svg', 'defs', 'linearGradient']:
            self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag not in ['meta', 'link', 'br', 'hr', 'img', 'input', 'col', 'path', 'rect', 'circle', 'line', 'polygon', 'polyline', 'stop', 'svg', 'defs', 'linearGradient']:
            if self.stack and self.stack[-1] == tag:
                self.stack.pop()

parser = MyHTMLParser()
with open('nsm-dashboard.html', 'r', encoding='utf-8') as f:
    parser.feed(f.read())
print("Remaining stack length:", len(parser.stack))
