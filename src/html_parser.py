import json, re
from bs4 import BeautifulSoup
from pathlib import Path

JSON_PATH = "asset/after_parsing/새 문서_request_20250909_113405.json"  # 입력 JSON
OUT_PATH = Path(JSON_PATH).with_suffix(".html")  # 같은 이름 .html

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

def walk(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "html" and isinstance(v, str):
                yield v
            else:
                yield from walk(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk(item)

# id -> outerHTML(1줄). 같은 id는 처음 것만 사용(원하면 리스트로 바꿔 모두 저장)
id_to_outer = {}

for html_str in walk(data):
    soup = BeautifulSoup(html_str, "html.parser")
    for el in soup.find_all(attrs={"id": True}):  # id 있는 모든 요소
        _id = str(el.get("id"))
        if _id not in id_to_outer:
            # 1줄로 정리(렌더링엔 영향 없음, 파일 가독성만 위해)
            one_line = re.sub(r"\s+", " ", str(el)).strip()
            id_to_outer[_id] = one_line

# id가 숫자면 숫자 정렬, 아니면 사전식
def sort_key(k):
    return (0, int(k)) if k.isdigit() else (1, k)

lines = [id_to_outer[k] for k in sorted(id_to_outer.keys(), key=sort_key)]

# 실제 렌더링되도록 raw HTML을 그대로 씁니다(escape 안 함!)
doc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{OUT_PATH.stem}</title>
<style>
  body {{ margin: 16px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans", "Apple SD Gothic Neo", "Malgun Gothic", Arial, sans-serif; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #ddd; padding: 6px; }}
</style>
</head>
<body>
{chr(10).join(lines)}
</body>
</html>
"""

OUT_PATH.write_text(doc, encoding="utf-8")
print(f"Saved: {OUT_PATH}  ({len(lines)} lines)")
