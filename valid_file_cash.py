import os
import json
import hashlib
from collections import defaultdict
from datetime import datetime

# Пути
target_dir = "C:\Отсортированный семейный архив"
hash_cache_path = os.path.join(target_dir, "_checked_hashes.json")


def get_file_hash(file_path):
    """Вычисляет MD5-хеш файла с обработкой ошибок."""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        print(f"⚠️ Ошибка чтения файла {file_path}: {str(e)}")
        return None


def check_new_files(target_dir, hashes):
    """Проверяет только новые/изменённые файлы с обработкой длинных путей."""
    duplicates = []
    trash_dir = os.path.join(target_dir, "_trash")

    for root, _, files in os.walk(target_dir):
        # Пропускаем папку _trash
        if "_trash" in root.split(os.sep):
            continue

        for file in files:
            try:
                file_path = os.path.join(root, file)

                # Обработка длинных путей для Windows
                if len(file_path) > 200:
                    file_path = "\\\\?\\" + os.path.abspath(file_path)

                # Пропускаем служебные файлы
                if file in ("_checked_hashes.json", "_duplicates_report.json"):
                    continue

                # Получаем дату изменения
                mod_time = os.path.getmtime(file_path)

                # Проверяем кеш
                if file_path in hashes:
                    cached_data = hashes[file_path]
                    if isinstance(cached_data, list):
                        cached_time, cached_hash = cached_data
                    else:
                        cached_time, cached_hash = mod_time, cached_data

                    if mod_time <= cached_time:
                        continue

                # Вычисляем хеш
                file_hash = get_file_hash(file_path)
                if not file_hash:
                    continue

                # Поиск дубликатов
                is_duplicate = False
                for cached_file, cached_data in hashes.items():
                    if isinstance(cached_data, list):
                        _, cached_hash = cached_data
                    else:
                        cached_hash = cached_data

                    if cached_hash == file_hash and cached_file != file_path:
                        duplicates.append({
                            "original": cached_file,
                            "duplicate": file_path
                        })
                        is_duplicate = True
                        break

                # Обновляем кеш
                hashes[file_path] = [mod_time, file_hash]

                if not is_duplicate:
                    print(f"🟢 Уникальный: {file_path[:100]}...")
                else:
                    print(f"🔴 Дубль: {file_path[:100]}...")

            except Exception as e:
                print(f"⚠️ Ошибка обработки файла {file[:50]}...: {str(e)}")
                continue

    return duplicates


def find_duplicates_from_cache(target_dir):
    """
    Находит дубликаты на основе данных из _checked_hashes.json.
    Формирует отчёт _duplicates_report.json в формате:
    [{"original": "path1", "duplicate": "path2"}, ...]
    """
    cache_path = os.path.join(target_dir, "_checked_hashes.json")
    report_path = os.path.join(target_dir, "_duplicates_report.json")

    if not os.path.exists(cache_path):
        print("Ошибка: файл _checked_hashes.json не найден. Сначала выполните быструю проверку (команда 1).")
        return []

    # Загружаем кеш
    with open(cache_path, 'r', encoding='utf-8') as f:
        checked_hashes = json.load(f)

    # Группируем файлы по хешам
    hash_groups = defaultdict(list)
    for file_path, (_, file_hash) in checked_hashes.items():
        hash_groups[file_hash].append(file_path)

    # Формируем список дублей (файлы с одинаковыми хешами)
    duplicates = []
    for files in hash_groups.values():
        if len(files) > 1:
            # Первый файл в группе считаем "оригиналом"
            original = files[0]
            for duplicate in files[1:]:
                duplicates.append({"original": original, "duplicate": duplicate})

    # Сохраняем отчёт
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(duplicates, f, indent=4, ensure_ascii=False)

    print(f"Найдено дубликатов: {len(duplicates)}. Отчёт сохранён в {report_path}")
    return duplicates


def find_duplicates(target_dir):
    """Полная проверка всех файлов на дубликаты"""
    hashes = defaultdict(list)

    for root, _, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)
            if file_hash:
                hashes[file_hash].append(file_path)

    # Фильтруем только дубликаты
    duplicates = []
    for hash_val, files in hashes.items():
        if len(files) > 1:
            for i in range(1, len(files)):
                duplicates.append({
                    "original": files[0],
                    "duplicate": files[i]
                })

    # Сохраняем отчет
    with open("_duplicates_report.json", 'w') as f:
        json.dump(duplicates, f, indent=4)

    print(f"Найдено {len(duplicates)} дубликатов")
    return duplicates

def load_checked_hashes():
    """Загружает кеш хешей из файла или создаёт новый."""
    if os.path.exists(hash_cache_path):
        with open(hash_cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_checked_hashes(hashes):
    """Сохраняет кеш хешей в файл."""
    with open(hash_cache_path, 'w', encoding='utf-8') as f:
        json.dump(hashes, f, indent=4, ensure_ascii=False)


# Сохраняем отчёт о дублях
def save_report_of_doblicates(duplicates):
    if duplicates:
        report_path = os.path.join(target_dir, "_duplicates_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(duplicates, f, indent=4, ensure_ascii=False)
        print(f"\nНайдено дублей: {len(duplicates)}. Отчёт сохранён в {report_path}")
    else:
        print("\nДубликатов не найдено.")