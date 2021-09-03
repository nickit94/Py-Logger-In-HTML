import sys
from collections import namedtuple
from dataclasses import dataclass, field


@dataclass
class BaseConfig:
    """
    Датакласс с общим конфигом для логов:

    * filename:             Путь к файлу, в который будет сохранен лог. Если передано None, вывод
                            будет производиться в консоль.
    * is_code_inside:       Флаг, определяющий, будет ли код стилей и скрипта (css и js) включен
                            в файл лога или будет дана ссылка. Работает, если задан filename.
    * is_split_modules:     Разделять ли логи на модули (аккардеоны).
    * is_module_priority:   Приоритет модуля или даты.
    * datetime_format:      Формат даты и времени. Если None - дата и время не будут выводится
                            в логи (не будет создана первая колонка)
    * _log_list:            Общий буфер, куда помещаются все логи во время выполнения программы.
                            По завершению рабоы программы (успешному или с ошибкой) логи будут
                            сохранены в filename. Используется, только если задан filename.
    """
    filename: str = None
    is_code_inside: bool = False
    is_split_modules: bool = True
    is_module_priority: bool = False
    datetime_format: str = "%d.%m.%y %H:%M:%S.%f"
    _log_list: list = field(default_factory=list)

    """ Счетчики уровней логов """
    count_info: int = 0
    count_debug: int = 0
    count_warning: int = 0
    count_error: int = 0
    count_critical: int = 0

    def add_log(self, log_item):
        """
        Добавить 1 запись в общий буфер
        :param log_item: запись лога типа LoggerItem
        """
        if log_item.level == 'info':
            self.count_info += 1
        elif log_item.level == 'debug':
            self.count_debug += 1
        elif log_item.level == 'warning':
            self.count_warning += 1
        elif log_item.level == 'error':
            self.count_error += 1
        elif log_item.level == 'critical':
            self.count_critical += 1

        self._log_list.append(log_item)

    @property
    def log_list(self):
        """
        Getter, возвращает буфер логов
        :return: список LoggerItem
        """
        return self._log_list

    @log_list.setter
    def log_list(self, value):
        """
        Setter, устанавливает буффер логов
        :param value: список LoggerItem
        """
        self._log_list = value


"""
LoggerItem - тип данных для хранения логов:

* module    - Модуль, к которому относится лог (имя логгера)
* datetime  - Дата и время лога (формат задается в BaseConfig)
* level     - Уровень лога [info, debug, warning, error, critical]
* text      - Текст лога
* style     - Стиль текста лога. Строка вида 'bisu', если нужен определенный стиль: добавляется буква стиля в строку
              Возможные стили:
                * b: жирный
                * i: курсив
                * s: зачеркнутый
                * u: подчеркнутый 
"""
LoggerItem = namedtuple(
    'LoggerItem',
    (
        'module',
        'datetime',
        'level',
        'text',
        'style',
    ),
)


CONSOLE_FORMAT = "{module}: {level} - {text}"
SUCCESS_FINAL_MSG = '<b>Успешное</b> завершение работы программы'
ERROR_FINAL_MSG = 'Программа завершилась сбоем:<br><br>{error}'
LOG_FILENAME = '{path}log-{date}.html'

CSS_PATH_LIST = ['Css/style.min.css', ]
JS_PATH_LIST = ['Js/jquery.min.js', 'Js/script.min.js']

ACCORDION_COMMON_START = '<div class="accordion js-accordion">'
ACCORDION_COMMON_END = '</div>'
ACCORDION_START = '<div class="accordion__item js-accordion-item active">' \
                  '<div class="accordion-header js-accordion-header">{title}</div>' \
                  '<div class="accordion-body js-accordion-body">'
ACCORDION_END = '</div></div>'
CARD_BLOCK = '<div class="container-cards wrap">' \
             '<div class="grid-card info"><div class="card-text">INFO: {info}</div></div>' \
             '<div class="grid-card debug"><div class="card-text">DEBUG: {debug}</div></div>' \
             '<div class="grid-card warning"><div class="card-text">WARNING: {warning}</div></div>' \
             '<div class="grid-card error"><div class="card-text">ERROR: {error}</div></div>' \
             '<div class="grid-card critical"><div class="card-text">CRITICAL: {critical}</div></div></div>'
TABLE_START = '<div class="container-table100"><div class="table100-body"><table>'
TABLE_END = '</table></div></div>'
ROW_START = '<tr class="{level}">'
COLUMN_TIME = '<td class="column1" title={title}>{text}</td>'
COLUMN_MODULE = '<td class="column1">{text}</td>'
COLUMN_TEXT = '<td class="column2">{text}</td>'
ROW_END = '</tr>'

DOCTYPE = '<!DOCTYPE html>'
META = '<meta charset="UTF-8">'
TITLE = '<title>{title}</title>'
TITLE_STR = 'log {date}'

STYLES = '<style type="text/css">{code}</style>'
STYLES_PATH = '<link rel="stylesheet" type="text/css" href="{path}">'
SCRIPTS = '<script>{code}</script>'
SCRIPTS_PATH = '<script src="{path}"></script>'

HTML_START = '<html>'
HTML_END = '</html>'
HEAD_START = '<head>'
HEAD_END = '</head>'
BODY_START = '<body>'
BODY_END = '</body>'

BOLD_STR = '<b>{}</b>'
ITALIC_STR = '<i>{}</i>'
STRIKE_STR = '<s>{}</s>'
UNDER_STR = '<u>{}</u>'
