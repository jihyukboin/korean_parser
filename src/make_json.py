#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 원문 입력받고 , json 형태로 변환 --> /asset/~.json
import json
import os
import argparse
from typing import Any

ASSET_DIR = "asset"


def sanitize_filename(name: str) -> str:
    """경로 구분자/금지문자 대체. 비어 있으면 그대로 빈 문자열 반환."""
    prohibited = set('/\\?%*:|"<>')
    return "".join("_" if ch in prohibited else ch for ch in name).strip()


def ensure_json_ext(name: str) -> str:
    return name if name.lower().endswith(".json") else name + ".json"


def load_existing_json(path: str) -> dict[str, Any]:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # 손상되었거나 구조가 다르면 새로 시작
        return {}


def prompt_nonempty_filename(prompt: str) -> tuple[str, str]:
    """빈 값 불가. 사용자가 입력할 때까지 재요청."""
    while True:
        name_raw = input(prompt).strip()
        name_clean = sanitize_filename(name_raw)
        if name_raw and name_clean:
            return ensure_json_ext(name_clean), name_raw
        print("⚠️ 파일 이름은 비워둘 수 없습니다. 다시 입력하세요.\n")


def read_one_item(idx: int) -> tuple[bool, str | None]:
    """
    한 문항(여러 줄 가능) 입력을 받는다.
    - 첫 줄에서 빈 입력이면 전체 종료 신호 → (False, None)
    - 한 줄에 'END'(대소문자 무관) 또는 첫 줄 이후의 '빈 줄'을 입력하면 해당 문항 입력 종료
    - 입력 중 '\\n' 시퀀스는 실제 개행으로 변환하여 같은 문항 내 줄바꿈으로 처리
    - 미리보기 후 저장 여부 확인(Y/yes 저장)
    """
    while True:
        print(
            f"\n[{idx}번 문항 입력]\n"
            "- 여러 줄 입력 가능. 문항 종료: 'END' 입력(대소문자 무관) 또는 빈 줄.\n"
            "- 전체 종료: 첫 줄에서 그냥 Enter.\n"
            "- 붙여넣은 텍스트에 '\\n'이 포함되어도 실제 줄바꿈으로 처리됩니다."
        )
        lines: list[str] = []
        first_prompt = True
        while True:
            try:
                line = input(f"{idx}번 > ")
            except EOFError:
                if not lines:
                    return False, None
                break

            # 전체 종료 조건(첫 줄에서 빈 줄)
            if first_prompt and line == "":
                return False, None

            # 문항 종료 조건: 'END' 또는 첫 줄 이후의 빈 줄
            if line.strip().upper() == "END" or (not first_prompt and line == ""):
                break

            # 리터럴 "\n" → 실제 개행
            line = line.replace("\\n", "\n")
            lines.append(line)
            first_prompt = False

        text = "\n".join(lines)

        # 확인(미리보기)
        print("\n----- 입력 미리보기 -----")
        print(text)
        print("-------------------------")
        confirm = input("이 문항을 저장하시겠습니까? [y/N]: ").strip().lower()
        if confirm in ("y", "yes"):
            return True, text

        retry = input("다시 입력하시겠습니까? [y/N]: ").strip().lower()
        if retry in ("y", "yes"):
            # 같은 idx로 재입력
            continue
        else:
            # 저장하지 않고 이 번호를 건너뜀
            return True, ""  # 호출부에서 빈 값은 스킵


def main() -> None:
    # 선택: CLI 인자 지원 (예: python make_questions_json.py --name 각론_수학)
    parser = argparse.ArgumentParser(description="문장 수집 후 JSON 저장")
    parser.add_argument(
        "-n",
        "--name",
        dest="name",
        help="생성할 JSON 파일 이름(확장자 생략 가능)"
    )
    args = parser.parse_args()

    if args.name:
        name_clean = sanitize_filename(args.name)
        if not name_clean:
            print("⚠️ 제공된 파일명이 유효하지 않습니다. 인터랙티브 입력으로 전환합니다.\n")
            filename, filename_display = prompt_nonempty_filename(
                '생성할 JSON 파일 이름(EX.각론_수학)을 입력하세요: '
            )
        else:
            filename = ensure_json_ext(name_clean)
            filename_display = args.name
    else:
        filename, filename_display = prompt_nonempty_filename(
            '생성할 JSON 파일 이름(EX.각론_수학)을 입력하세요: '
        )

    os.makedirs(ASSET_DIR, exist_ok=True)
    path = os.path.join(ASSET_DIR, filename)

    # 기존 파일 로드(있으면 이어쓰기)
    data = load_existing_json(path)
    if not data:
        data = {"파일 이름": filename_display, "문항": []}
    else:
        data.setdefault("파일 이름", filename_display)
        data.setdefault("문항", [])

    idx = len(data["문항"]) + 1

    print("\n여러 문항을 순서대로 입력합니다.")
    print("첫 줄에서 빈 입력이면 전체 입력을 종료합니다.\n")

    while True:
        proceed, text = read_one_item(idx)
        if not proceed:
            # 전체 종료
            break

        # 저장 거부 & 건너뛰기 선택 시 빈 문자열이 올 수 있음 → 저장 스킵
        if not text:
            idx += 1
            continue

        data["문항"].append({
            "문제 번호": idx,
            "입력받은 문장": text
        })
        idx += 1

    if not data["문항"]:
        print("입력된 문장이 없어 파일을 생성하지 않았습니다.")
        return

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 저장 완료: {path}")
    print(f"총 {len(data['문항'])}개 문항이 포함되었습니다.")


if __name__ == "__main__":
    main()
