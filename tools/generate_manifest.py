#!/usr/bin/env python3
"""Генерирует translations/manifest.json для TranslationSync.
Запуск из корня репозитория: python tools/generate_manifest.py
version увеличивается ТОЛЬКО если изменился состав/хэши файлов."""
import hashlib, json, sys
from pathlib import Path

DIR = Path("translations")
OUT = DIR / "manifest.json"
EXCLUDE = {"manifest.json", "config.json"}  # config.json мод принципиально не принимает

files = {}
for p in sorted(DIR.rglob("*.json")):
    rel = p.relative_to(DIR).as_posix()
    if rel in EXCLUDE or rel.startswith("wynncraft_translator_cache/"):
        continue
    data = p.read_bytes()
    json.loads(data.decode("utf-8"))  # битый JSON в репозиторий не пускаем
    files[rel] = {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}

old = json.loads(OUT.read_text("utf-8")) if OUT.exists() else {"version": 0, "files": {}}
version = old.get("version", 0) if old.get("files") == files else old.get("version", 0) + 1
if old.get("files") == files and OUT.exists():
    print("Без изменений, version =", version); sys.exit(0)
OUT.write_text(json.dumps({"version": version, "files": files}, ensure_ascii=False, indent=2) + "\n", "utf-8")
print(f"manifest.json: version {version}, файлов {len(files)}")
