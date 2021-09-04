from modules.logger.logger_helper import \
    CSS_PATH_LIST, JS_PATH_LIST, ACCORDION_START, ACCORDION_COMMON_START, BODY_START, HEAD_START, HTML_START, \
    ROW_START, TABLE_START, ACCORDION_COMMON_END, HEAD_END, HTML_END, BODY_END, TABLE_END, ACCORDION_END, ROW_END, \
    META, STRIKE_STR, BOLD_STR, UNDER_STR, ITALIC_STR, STYLES, STYLES_PATH, SCRIPTS_PATH, SCRIPTS, DOCTYPE, \
    COLUMN_TIME, COLUMN_TEXT, COLUMN_MODULE, CARD_BLOCK


def _group_logs_by_modules(log_list, is_module_priority):
    """
    Группирует список логов по названиям модулей. Результат - сгруппированные списки в списке

    :param log_list: список логов типа LoggerItem
    :return: list
    """
    if is_module_priority:
        log_list = sorted(log_list, key=lambda x: x.module)

    current_module = None
    result_list = list()
    group_list = list()

    for log_item in log_list:
        if current_module != log_item.module:
            current_module = log_item.module
            if group_list:
                result_list.append(group_list)
                group_list = list()

        group_list.append(log_item)
    else:
        result_list.append(group_list)

    if is_module_priority:
        result_list = sorted(result_list, key=lambda x: x[0].datetime)

    return result_list


def _generate_row(log_item, datetime_format, is_split_modules):
    """
    Генерация одной строчки таблицы

    :param log_item: список логов типа LoggerItem
    :return: str
    """
    log_module = log_item.module
    log_style = log_item.style or ''
    log_date = str(log_item.datetime.date())
    log_time = str(log_item.datetime.time())
    log_text = log_item.text

    row = ROW_START.format(level=log_item.level)

    if datetime_format:
        row += COLUMN_TIME.format(title=log_date, text=log_time)

    if not is_split_modules:
        row += COLUMN_MODULE.format(text=log_module)

    if 'b' in log_style:
        log_text = BOLD_STR.format(log_text)
    if 'i' in log_style:
        log_text = ITALIC_STR.format(log_text)
    if 'u' in log_style:
        log_text = STRIKE_STR.format(log_text)
    if 's' in log_style:
        log_text = UNDER_STR.format(log_text)

    row += COLUMN_TEXT.format(text=log_text)
    row += ROW_END
    return row


def _generate_table(log_list, datetime_format, is_split_modules):
    """
    Генерация таблицы

    :param log_list: список логов типа LoggerItem
    :return: str
    """
    table = TABLE_START

    for log_item in log_list:
        table += _generate_row(log_item, datetime_format, is_split_modules)

    table += TABLE_END
    return table


def _generate_styles(is_code_inside):
    """
    Генерация стилей (CSS) в зависимости от параметра: или ссылка на стили или стили внутрь документа
    :return: str
    """
    css = ''
    if is_code_inside:
        for link in CSS_PATH_LIST:
            with open(link, 'r', encoding='utf-8') as f:
                code = f.read()
                css += STYLES.format(code=code)
    else:
        for link in CSS_PATH_LIST:
            css += STYLES_PATH.format(path=link)

    return css


def _generate_scripts(is_code_inside):
    """
    Генерация скриптов (JS) в зависимости от параметра: или ссылка на стили или стили внутрь документа
    :return: str
    """
    js = ''
    if is_code_inside:
        for link in JS_PATH_LIST:
            with open(link, 'r', encoding='utf-8') as f:
                code = f.read()
                js += SCRIPTS.format(code=code)
    else:
        for link in JS_PATH_LIST:
            js += SCRIPTS_PATH.format(path=link)

    return js


def generate_html(logger):
    """
    Генерация html документа с логами

    :param logger: датакласс BaseConfig с буфером логов и настройками
    :return: str
    """
    html = DOCTYPE
    html += HTML_START
    html += HEAD_START
    html += META
    html += _generate_styles(logger.is_code_inside)
    html += HEAD_END
    html += BODY_START
    html += CARD_BLOCK.format(info=logger.count_info,
                              success=logger.count_success,
                              debug=logger.count_debug,
                              warning=logger.count_warning,
                              error=logger.count_error,
                              critical=logger.count_critical)

    if logger.is_split_modules:
        module_list = _group_logs_by_modules(logger.log_list, logger.is_module_priority)
        html += ACCORDION_COMMON_START

        for module_item in module_list:
            html += ACCORDION_START.format(title=module_item[0].module)
            html += _generate_table(module_item, logger.datetime_format, logger.is_split_modules)
            html += ACCORDION_END

        html += ACCORDION_COMMON_END
    else:
        html += _generate_table(logger.log_list, logger.datetime_format, logger.is_split_modules)

    html += _generate_scripts(logger.is_code_inside)
    html += BODY_END
    html += HTML_END

    return html
