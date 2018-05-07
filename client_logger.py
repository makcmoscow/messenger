import logging
import logging.handlers
import os

# путь до папки где лежит этот модуль
LOG_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
# путь до файла с логом
CLIENT_LOG_FILE_PATH = os.path.join(LOG_FOLDER_PATH, 'client.log')

# создаем логгер и именем client
client_logger = logging.getLogger('client')
# настраиваем формат вывода
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
# обработчик будет логгер, который пишет в файл
client_handler = logging.FileHandler(CLIENT_LOG_FILE_PATH, encoding='utf-8')
# задаем уровень обработчика
client_handler.setLevel(logging.INFO)
# связываем с форматером
client_handler.setFormatter(formatter)
# связываем с обработчиком
client_logger.addHandler(client_handler)
# устанавливаем уровень логгера
client_logger.setLevel(logging.INFO)