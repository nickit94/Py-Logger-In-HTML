import sys
import atexit
import traceback
from datetime import datetime

from modules.logger.html_generator import generate_html
from modules.logger.logger_helper import LoggerItem, BaseConfig, \
    CONSOLE_FORMAT, SUCCESS_FINAL_MSG, ERROR_FINAL_MSG, LOG_FILENAME


_root = BaseConfig()


def base_config(**config):
    """
    Заполнение настроек базового конфига.
    Можно указать ряд необязательных аргументов, которые могут изменить поведение по умолчанию.

    filename:           Путь к файлу, в который будет сохранен лог. Если передано None, вывод
                        будет производиться в консоль.
    is_code_inside:     Флаг, определяющий, будет ли код стилей и скрипта (css и js) включен
                        в файл лога или будет дана ссылка. Работает, если задан filename.
    is_split_modules:   Разделять ли логи на модули (аккардеоны).
    is_module_priority: Приоритет модулей или даты. True - модули. Если приоритет модулей - то
                        модули не будут повторяться, но дата может идти непоследовательно.
                        Если приоритет даты - то логи будут идти последовательно друг за другом
                        по времени, но заголовки модулей могут дублироваться. Работает только
                        с is_split_modules.
    datetime_format:    Формат даты и времени. Если None - дата и время не будут выводится
                        в логи (не будет создана первая колонка).
    """
    filename = config.pop('filename', None)
    is_code_inside = config.pop('is_code_inside', None)
    is_split_modules = config.pop('is_split_modules', None)
    is_module_priority = config.pop('is_module_priority', None)
    datetime_format = config.pop('datetime_format', None)

    if filename is not None:
        _root.filename = filename
        atexit.register(_save_logs)

    if is_code_inside is not None:
        _root.is_code_inside = is_code_inside

    if is_split_modules is not None:
        _root.is_split_modules = is_split_modules

    if is_module_priority is not None:
        _root.is_module_priority = is_module_priority

    if datetime_format is not None:
        _root.datetime_format = datetime_format


def get_logger(name):
    """
    Получить логгер с заданным именем. Имя будет использоваться как название модуля
    для сворачивания логов, если в базовом конфиге установлен флаг is_split_modules
    либо выводится в строке в отсальных случаях.

    :param name: имя модуля
    :return: class Logger
    """
    if not isinstance(name, str):
        return None

    return Logger(name)


def _save_logs():
    """
    Метод сохраняет логи в html формат при завершении работы программы (в т.ч. и из-за ошибки).
    Работает, только если задан filename в BaseConfig
    """
    if not _root.filename:
        return

    # noinspection PyBroadException
    try:
        traceback_msg = ''.join(traceback.format_exception(sys.last_type, sys.last_value, sys.last_traceback))
        traceback_msg = traceback_msg.replace('\n', '<br>').replace(' ', '\xa0')
        final_msg = ERROR_FINAL_MSG.format(error=traceback_msg)
        level = 'critical'
    except Exception:
        final_msg = SUCCESS_FINAL_MSG
        level = 'info'

    _root.add_log(LoggerItem(
        module='base',
        datetime=datetime.now(),
        level=level,
        text=final_msg,
        style=None))

    html = generate_html(logger=_root)
    start_datetime = _root.log_list[0].datetime.strftime('%d.%m.%y-%H.%M.%S')
    filename = LOG_FILENAME.format(path=_root.filename, date=start_datetime)

    with open(filename, 'w', encoding='UTF-8') as f:
        f.write(html)


class Logger:
    """
    Экземпляр класса Logger представляет из себя один канал логгирования, называемый модулем.
    Это необходимо для логического разграничения логов по разным модулям.
    Название текущего экземпляра будет тянутся в вывод, чтобы обозначить, откуда именно логгер был вызван.
    """
    def __init__(self, name):
        self.name = name

    def _send(self, level, text, style):
        """
        Добавление одной записи в очередь (для файла) или в консоль

        :param level: уровень лога [info, debug, warning, error, critical]
        :param text: текст лога
        :param style: стиль текста лога
        """
        if _root.filename:
            _root.add_log(LoggerItem(
                module=self.name,
                datetime=datetime.now(),
                level=level,
                text=text,
                style=style))
        else:
            print(CONSOLE_FORMAT.format(module=self.name,
                                        level=level.upper(),
                                        text=text))

    def info(self, text, style=None):
        """
        Уровень INFO

        :param text: текст сообщения
        :param style: опционально, стили форматирования текста [b, i, u, s]
        """
        self._send(level='info', text=text, style=style)

    def debug(self, text, style=None):
        """
        Уровень DEBUG

        :param text: текст сообщения
        :param style: опционально, стили форматирования текста [b, i, u, s]
        """
        self._send(level='debug', text=text, style=style)

    def warning(self, text, style=None):
        """
        Уровень WARNING

        :param text: текст сообщения
        :param style: опционально, стили форматирования текста [b, i, u, s]
        """
        self._send(level='warning', text=text, style=style)

    def error(self, text, style=None):
        """
        Уровень ERROR

        :param text: текст сообщения
        :param style: опционально, стили форматирования текста [b, i, u, s]
        """
        self._send(level='error', text=text, style=style)

    def critical(self, text, style='b'):
        """
        Уровень CRITICAL

        :param text: текст сообщения
        :param style: опционально, стили форматирования текста [b, i, u, s]. По-умолчанию жирный текст
        """
        self._send(level='critical', text=text, style=style)


"""
Пример использования:

    Вызывается 1 раз конфиг и переопределяются стандартные поля (см. датакласс BaseConfig):        
        base_config(filename=LOGS_PATH, is_split_modules=True, is_module_priority=True)
    Если переопределять ничего не требуется, то вызов этого метода становится необязательным.
    
    Далее в каждом модуле, где требуется логгирование, вызывается метод get_logger, в который передается желаемое имя, 
    обозначающее текущий модуль и который возвращает экземпляр класса логгирования (Logger):
        logger = get_logger('name_module')
    
    Для написания логов разных уровней используются методы класса Logger-а, такие как:
        * info(text, style=None) - информационное сообщение с серым фоном
        * debug(text, style=None) - дебажное сообщение с синим фоном
        * warning(text, style=None) - сообщение с предупреждением с желтым фоном
        * error(text, style=None) - сообщение с ошибкой с красным фоном
        * critical(text, style='b') - сообщение с критичной ошибкой с бордовым фоном и жирным текстом по-умолчанию
    
    Можно изменить стандартное форматирование текста, заполнив параметр style строкой из символов, где символы:
        * b: жирный
        * i: курсив
        * s: зачеркнутый
        * u: подчеркнутый 
    
    Например:
        logger.debug(text, style='bi') - дебажное сообщение с желтым фоном с жирным и курсивным текстом
        logger.info(text, style='s') - информационное сообщение с зачеркнутым текстом 
    
    Допускаются любые комбинации уровней и стилей форматирования.
"""

