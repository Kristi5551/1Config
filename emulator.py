import io
import os
import tarfile
import sys
import xml.etree.ElementTree as ET
from datetime import datetime


class FakeFile:
    def __init__(self, name, is_dir):
        self.name = name
        self.is_dir = is_dir


class ShellEmulator:
    def __init__(self, hostname, tar_path, log_path):
        self.hostname = hostname
        self.current_dir = '/'  # Текущий каталог
        self.log_path = log_path
        self.file_system = self.load_file_system(tar_path)  # Загрузка файловой системы
        self.log_actions = []

    def load_file_system(self, tar_path):
        # Читаем архив в памяти
        with open(tar_path, 'rb') as f:
            tar_byte_data = io.BytesIO(f.read())

        tar = tarfile.open(fileobj=tar_byte_data, mode='r')
        file_system = {}

        for member in tar.getmembers():
            # Заполняем словарь с именами файлов и каталогов
            file_system[member.name] = FakeFile(member.name, member.isdir())

        return file_system

    def log(self, action):
        self.log_actions.append(action)

    def save_log(self):
        root = ET.Element("log")
        for action in self.log_actions:
            entry = ET.SubElement(root, "entry")
            entry.text = action
        tree = ET.ElementTree(root)
        tree.write(self.log_path)

    def ls(self):
        # Печатаем имена файлов и каталогов
        print(" ".join(
            name for name in self.file_system if self.file_system[name].is_dir or name.startswith(self.current_dir)))
        self.log(f"Executed ls in {self.current_dir}")

    def cd(self, path):
        new_dir = os.path.join(self.current_dir, path)
        if new_dir in self.file_system and self.file_system[new_dir].is_dir:
            self.current_dir = new_dir
            self.log(f"Changed directory to {self.current_dir}")
        else:
            print(f"cd: no such file or directory: {path}")

    def mv(self, src, dest):
        # Переименовываем файл, если он существует
        if src in self.file_system:
            self.file_system[dest] = self.file_system.pop(src)
            self.log(f"Moved {src} to {dest}")
        else:
            print(f"mv: cannot stat '{src}': No such file or directory")

    def cal(self):
        print(datetime.now().strftime("%B %Y"))
        self.log("Executed cal")

    def run(self):
        while True:
            command = input(f"{self.hostname}:{self.current_dir} $ ")
            if command == "exit":
                self.save_log()
                break
            elif command.startswith("cd "):
                self.cd(command.split(" ")[1])
            elif command == "ls":
                self.ls()
            elif command.startswith("mv "):
                src, dest = command.split(" ")[1:3]
                self.mv(src, dest)
            elif command == "cal":
                self.cal()
            else:
                print(f"{command}: command not found")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python emulator.py <hostname> <tar_path> <log_path>")
        sys.exit(1)
    hostname = sys.argv[1]
    tar_path = sys.argv[2]
    log_path = sys.argv[3]
    emulator = ShellEmulator(hostname, tar_path, log_path)
    emulator.run()