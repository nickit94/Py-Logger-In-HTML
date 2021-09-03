# Py-Logger-In-HTML
Логирование для Python, генерирующее красивые и понятные HTML файлы с логами

## Описание

## Использование
Вызывается 1 раз конфиг и переопределяются стандартные поля (см. датакласс BaseConfig):        

`base_config(filename=LOGS_PATH, is_split_modules=True, is_module_priority=True)`

Если переопределять ничего не требуется, то вызов этого метода становится необязательным.

Далее в каждом модуле, где требуется логгирование, вызывается функция `get_logger`, в который передается желаемое имя, 
обозначающее текущий модуль и который возвращает экземпляр класса логгирования (Logger):

`logger = get_logger('name_module')`

Для написания логов разных уровней используются методы класса Logger-а, такие как:
* `info(text, style=None)` - информационное сообщение с серым фоном
* `debug(text, style=None)` - дебажное сообщение с синим фоном
* `warning(text, style=None)` - сообщение с предупреждением с желтым фоном
* `error(text, style=None)` - сообщение с ошибкой с красным фоном
* `critical(text, style='b')` - сообщение с критичной ошибкой с бордовым фоном и жирным текстом по-умолчанию

Можно изменить стандартное форматирование текста, заполнив параметр style строкой из символов, где символы:
* b: жирный
* i: курсив
* s: зачеркнутый
* u: подчеркнутый 

#### Например:

`logger.debug(text, style='bi')` - дебажное сообщение с желтым фоном с жирным и курсивным текстом

`logger.info(text, style='s')` - информационное сообщение с зачеркнутым текстом 

Допускаются любые комбинации уровней и стилей форматирования.
