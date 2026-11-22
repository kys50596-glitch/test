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
import shutil; shutil.copy('office.jpg', out / 'office.jpg')
print('docs/index.html 생성 완료')

# /admin 주소: 관리자 화면이 있는 미리보기 페이지로 이동(관리 권한이 있는 로그인 계정만 열림)
ADMIN_URL = 'https://claude.ai/artifact/UftvmsuheLYPmhB2TecqBp#admin'
admin = out / 'admin'; admin.mkdir(exist_ok=True)
(admin / 'index.html').write_text(f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta http-equiv="refresh" content="0;url={ADMIN_URL}">
<title>관리자 페이지 이동</title>
<style>body{{font-family:system-ui,"Malgun Gothic",sans-serif;margin:0;min-height:100vh;display:grid;place-items:center;background:#fbf6ec;color:#1c2623;text-align:center;padding:16px}}
a{{display:inline-block;margin-top:12px;background:#046a38;color:#f9ebd7;padding:14px 24px;border-radius:6px;text-decoration:none;font-weight:700}}</style></head>
<body><div><h1 style="font-size:1.3rem">관리자 페이지로 이동합니다</h1>
<p>자동으로 이동하지 않으면 아래 버튼을 눌러 주세요.<br>관리 권한이 있는 계정으로 로그인해야 열립니다.</p>
<a href="{ADMIN_URL}">관리자 페이지 열기</a></div>
<script>location.replace("{ADMIN_URL}");</script></body></html>
''', encoding='utf8')
print('docs/admin/index.html 생성 완료')
