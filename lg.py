import xml.etree.ElementTree as ET
import os

class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.root = ET.Element("session")

    def log_action(self, action):
        action_element = ET.SubElement(self.root, "action")
        action_element.text = action

    def save(self):
        tree = ET.ElementTree(self.root)
        tree.write(self.log_file, encoding='utf-8', xml_declaration=True)

# Пример использования
logger = Logger("log.xml")

# Логируем действия
logger.log_action("Запущен эмулятор")
logger.log_action("Выполнена команда: ls")
logger.log_action("Выполнена команда: cd /home")
logger.log_action("Выполнена команда: exit")

# Сохраняем лог в файл
logger.save()