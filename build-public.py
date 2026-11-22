"""index.html(관리자 포함 원본)을 GitHub Pages용 docs/index.html로 변환합니다.
사용법: python3 build-public.py"""
import re, pathlib
src = pathlib.Path('index.html').read_text(encoding='utf8')
title = re.search(r'<title>.*?</title>', src, re.S).group(0)
font = re.search(r'<link rel="stylesheet"[^>]*>', src).group(0)
style = re.search(r'<style>.*?</style>', src, re.S).group(0)
body = src
for part in (title, font, style):
    body = body.replace(part, '', 1)
body = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\n?', '', body)
body = re.sub(r'\s*<a class="adm-link"[^>]*>.*?</a>', '', body)  # 공개 사이트에서는 관리자 링크 숨김
head = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="description" content="의정부 녹양역 인근 이편한세상녹양역부동산. 매매·전세·월세·상가 상담 031-873-5454">\n'
        + title + '\n' + font + '\n' + style + '\n</head>\n<body>\n')
out = pathlib.Path('docs'); out.mkdir(exist_ok=True)
(out / 'index.html').write_text(head + body.strip() + '\n</body>\n</html>\n', encoding='utf8')
(out / '.nojekyll').write_text('')
print('docs/index.html 생성 완료')
