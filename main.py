import os
import valid_file_cash
from collections import defaultdict

# Пути
target_dir = r"C:\Отсортированный семейный архив"

def print_help():
    """Выводит список доступных команд."""
    print('\nСписок команд:')
    print('1 - быстрая проверка новых файлов (с кешированием)')
    print('2 - создать отчёт о дублях (полная проверка)')
    print('3 - удалить дубликаты из отчёта')
    print('h - помощь')
    print('q - выход')

def main():
    print('=== Программа для сортировки семейного архива ===')
    print_help()

    while True:
        try:
            command = input('\nВведите команду ("h" - список команд): ').strip().lower()

            if command == 'h':
                print_help()

            elif command == '1':
                print("\nЗапуск быстрой проверки (с кешированием)...")
                checked_hashes = valid_file_cash.load_checked_hashes()
                duplicates = valid_file_cash.check_new_files(target_dir, checked_hashes)
                valid_file_cash.save_checked_hashes(checked_hashes)
                valid_file_cash.save_report_of_doblicates(duplicates)

            elif command == '2':
                print("\nЗапуск полной проверки на дубликаты...")
                valid_file_cash.find_duplicates_from_cache(target_dir)

            elif command == '3':
                print("\nУдаление дубликатов из отчёта...")
                checked_hashes = valid_file_cash.load_checked_hashes()
                delete_duplicates.remove_duplicates_from_report(target_dir, checked_hashes)
                valid_file_cash.save_checked_hashes(checked_hashes)

            elif command == 'q':
                print("\nВыход из программы.")
                break

            else:
                print('\nОшибка: неизвестная команда. Введите "h" для списка команд.')

        except Exception as e:
            print(f"\n⚠️ Произошла ошибка: {str(e)}")
            print("Попробуйте еще раз или перезапустите программу.")

if __name__ == "__main__":
    main()