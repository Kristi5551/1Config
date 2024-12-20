import unittest
import os
from emulator.py import Emulator

class TestEmulatorCommands(unittest.TestCase):

    def setUp(self):
        # Создание экземпляра эмулятора перед каждым тестом
        self.emulator = Emulator("my_computer", "path/to/vfs.tar", "path/to/log.xml")
        self.emulator.start()  # Запуск эмулятора

    def tearDown(self):
        # Завершение работы эмулятора после каждого теста
        self.emulator.exit()

    def test_ls(self):
        # Тестирование команды ls
        output = self.emulator.execute_command("ls")
        self.assertIn("expected_file.txt", output)  # Проверьте, что файл присутствует

    def test_mv(self):
        # Тестирование команды mv
        self.emulator.execute_command("mv old_file.txt new_file.txt")
        self.assertTrue(os.path.exists("new_file.txt"))  # Проверьте, что новый файл существует
        self.assertFalse(os.path.exists("old_file.txt"))  # Проверьте, что старый файл не существует

    def test_cd(self):
        # Тестирование команды cd
        self.emulator.execute_command("cd new_directory")
        self.assertEqual(self.emulator.current_directory, "new_directory")  # Проверьте, что текущая директория изменилась

    def test_cal(self):
        # Тестирование команды cal
        output = self.emulator.execute_command("cal")
        self.assertIn("January", output)  # Проверьте, что вывод содержит название месяца

    def test_exit(self):
        # Тестирование команды exit
        self.emulator.execute_command("exit")
        self.assertFalse(self.emulator.is_running)  # Проверьте, что эмулятор завершил работу

if __name__ == "__main__":
    unittest.main()
