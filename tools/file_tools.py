import os

BASE_DIR = "files"


def write_file(filename, content):

    os.makedirs(BASE_DIR, exist_ok=True)

    path = os.path.join(BASE_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"ファイル {filename} を作成しました"


def read_file(filename):

    path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(path):
        return "ファイルが存在しません"

    with open(path, "r", encoding="utf-8") as f:
        return f.read()
