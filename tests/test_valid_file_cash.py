import unittest
import os
import shutil
from valid_file_cash import get_file_hash, find_duplicates, remove_duplicates_from_report
import tempfile
from pathlib import Path


class TestValidFileCash(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Безопасное создание тестовой среды"""
        cls.test_dir = Path(tempfile.mkdtemp(prefix="test_photos_"))

        # Создаем поддиректорию для тестов
        cls.test_data_dir = cls.test_dir / "test_data"
        cls.test_data_dir.mkdir()

        #Создаем тестовые файлы
        cls.file1 = cls.test_data_dir / "file1.jpg"  # Оригинал
        cls.file2 = cls.test_data_dir / "file2.jpg"  # Дубль
        cls.file3 = cls.test_data_dir / "file3.jpg"  # Файл с другим содержанием

        try:
            # Записываем бинарные данные (одинаковые для file1 и file2)
            identical_data = b"test_image_data" * 100
            cls.file1.write_bytes(identical_data)
            cls.file2.write_bytes(identical_data)
            cls.file3.write_bytes(b"different_image_data" * 100)
        except Exception as e:
            cls.tearDownClass()
            raise RuntimeError(f'Ошибка создания тестовых файлов: {e}')

    @classmethod
    def tearDownClass(cls):
        """Удаляем тестовую среду"""
        shutil.rmtree(cls.test_dir, ignore_errors=True)

    def test_get_file_hash(self):
        """Тестируем хеширование фалов"""
        # Проверяем что одинаковые файлы дают одинаковый хеш
        hash1 = get_file_hash(str(self.file1))
        hash2 = get_file_hash(str(self.file2))
        self.assertEqual(hash1, hash2,
                       "Ошибка: одинаковые файлы имеют разные хеши")
        hash3 = get_file_hash(str(self.file3))
        self.assertNotEqual(hash1, hash3,
                          "Ошибка: разные файлы имеют одинаковые хеши")


        # #Проверка обработки несуществующего файла
        # with self.assertRaises(FileNotFoundError):
        #     get_file_hash(str(self.test_dir / "non_existent.file"))

    def test_find_duplicates(self):
        """Тестирует поиск дубликатов"""
        duplicates = find_duplicates(self.test_data_dir)

        # Проверяем что найдена 1 пара дубликатов
        self.assertEqual(len(duplicates), 1,
                       f"Ожидалась 1 пара дубликатов, найдено {len(duplicates)}")

        # # Проверяем что это именно те файлы, которые мы ожидаем
        # found_files = {os.path.normpath(duplicates['original']).lower(),
        #                os.path.normpath(duplicates['duplicate']).lower()}
        #
        # expected_files = {str(self.file1).lower(), str(self.file2).lower()}
        # self.assertEqual(found_files, expected_files,
        #                  "Найдены не те дубликаты, которые ожидались")

if __name__ == '__main__':
    unittest.main()
