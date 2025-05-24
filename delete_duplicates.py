import os
import json
import shutil


def remove_duplicates_from_report(target_dir, checked_hashes):
    """Удаляет дубликаты и чистит кеш для _trash."""
    report_path = os.path.join(target_dir, "_duplicates_report.json")
    trash_dir = os.path.join(target_dir, "_trash")

    if not os.path.exists(report_path):
        print("Файл отчёта не найден!")
        return

    with open(report_path, 'r', encoding='utf-8') as f:
        duplicates = json.load(f)

    if not duplicates:
        print("Дубликатов не найдено.")
        return

    os.makedirs(trash_dir, exist_ok=True)

    for dup in duplicates:
        original = dup["original"]
        duplicate = dup["duplicate"]

        print(f"\nОригинал: {original}")
        print(f"Дубликат: {duplicate}")

        action = input("Удалить дубликат? (y/n/move/q): ").strip().lower()
        if action == 'y':
            os.remove(duplicate)
            checked_hashes.pop(duplicate, None)  # Удаляем из кеша
            print(f"Удалён: {duplicate}")
        elif action == 'move':
            new_path = os.path.join(trash_dir, os.path.basename(duplicate))
            shutil.move(duplicate, new_path)
            checked_hashes.pop(duplicate, None)  # Удаляем из кеша
            print(f"Перемещён в _trash: {duplicate}")
        elif action == 'q':
            print("Прервано пользователем.")
            break

    # Удаляем отчёт
    os.remove(report_path)
    print("\nОбработка завершена. Отчёт удалён.")