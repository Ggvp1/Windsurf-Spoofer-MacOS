import os
import shutil
from pathlib import Path

cache_path = Path.home() / ".wdm"

print("🔄 Очистка кеша webdriver-manager")

if cache_path.exists():
    try:
        shutil.rmtree(cache_path)
        print(f"✅ Кеш удален: {cache_path}")
    except Exception as e:
        print(f"❌ Ошибка при удалении кеша: {e}")
else:
    print("ℹ️  Кеш не найден")

print("\n🔄 Теперь запусти основной скрипт - chromedriver скачается заново")
print("python3 ws-spoof.py")
