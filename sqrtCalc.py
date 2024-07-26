import flet as ft
from flag import flag
import re
from cmath import pi, e, sqrt  # Константы пи, е и фи используются функцией eval, что не отображается при импорте
from scipy.constants import golden as phi
from numpy import around


def sqrt_calc(page: ft.Page):
    page.title = "Sqrt Calculator"
    page.window.min_width = 520
    page.window.min_height = 600
    page.window.width = 520
    page.window.height = 600
    page.window.max_width = 520
    page.window.max_height = 600

    # region Языковые пакеты приложения
    documentation_rus = str(
        "Программная документация Sqrt Calculator\n"
        "Выполнил студент 2 курса НИУ ВШЭ: Банников Владислав.\n\n"
        "Техническое задание: необходимо реализовать программу, которая будет извлекать корни из действительных и "
        "комплексных чисел. Необходим графический интерфейс с наличием полиязычности и кроссплатформенности. "
        "Программа должна иметь документацию и службу поддержки (форум или телефонную горячую линию) "
        "и должна быть сдана в срок до 20:00 10 сентября 2023 года.\n\n"
        "Описание программного продукта: Данный программный продукт разработан на языке Python, графический "
        "интерфейс создан с помощью Flet. Программа используется для извлечения корней из различных чисел.\n\n"
        "Список поддерживаемых платформ: Windows (95-11) \n\nСписок поддерживаемых функций: "
        "\n- извлечение корней из действительных и комплексных чисел, \n- выбор заданной точности для нецелых "
        "корней, \n- выбор языка, \n- выбор темы приложения.\n\n"
        "Список поддерживаемых языков: Русский, Английский.\n\n"
        "Для пользовательской поддержки используется горячая линия (8 *** *** ** **)."
    )
    documentation_en = str(
        "Sqrt Calculator Software Documentation\n"
        "Prepared by: Vladislav Bannikov, 2nd-year student at HSE University.\n\n"
        "Technical Assignment: The task is to develop a program that extracts roots from real and complex numbers. "
        "A graphical interface with multilingual and cross-platform support is required. The program must have "
        "documentation and a support service (forum or hotline) and must be submitted by 8:00 PM on September 10, 2023."
        "\n\nDescription of the Software Product: This software product is developed in Python, and the graphical "
        "interface is created using Flet. The program is used to extract roots from various numbers.\n\n"
        "List of Supported Platforms: Windows (95-11).\n\n"
        "List of Supported Functions: \n- extracting roots from real and complex numbers,\n- selecting the desired "
        "precision for non-integer roots,\n- language selection,\n- application theme selection.\n\n"
        "List of Supported Languages: Russian, English.\n\n"
        "For user support, a hotline is used (8 *** *** ** )."
    )

    language_packs = {
        "ru": {
            # Локализация для меню настроек
            "settings_title": "Настройки",
            "settings_tooltip": "Документация, язык и тема приложения",
            "help_button_title": "Помощь",
            "help_button_tooltip": "Информация о программе",
            "language_button_tooltip": "Выбор языка",
            "theme_button_title": "Тема",
            "theme_button_tooltip": "Выбор светлой или тёмной темы",

            # Локализация для полей ввода-вывода
            "decimal_places_title": "Количество знаков после запятой",
            "decimal_places_message": "Количество знаков после запятой может быть от 0 до 5",
            "input_label": "Введите число",
            "input_error_text": "Некорректный ввод",
            "output_hint": "(Здесь будет результат)",

            # Документация
            "documentation": documentation_rus
        },
        "en": {
            # Локализация для меню настроек
            "settings_title": "Settings",
            "settings_tooltip": "Documentation, language and theme",
            "help_button_title": "Help",
            "help_button_tooltip": "Info about program",
            "language_button_tooltip": "Language: russian, english",
            "theme_button_title": "Theme",
            "theme_button_tooltip": "Choosing light or dark theme",

            # Локализация для полей ввода-вывода
            "decimal_places_title": "Number of decimal places",
            "decimal_places_message": "Number of decimal places can be from 0 to 5",
            "input_label": "Enter a number",
            "input_error_text": "Invalid input",
            "output_hint": "(Here will be the result)",

            # Документация
            "documentation": documentation_en
        }
    }
    # endregion

    # region Создание кнопки открытия/закрытия меню настроек
    def open_settings(event_args):
        """
        Открывает меню настроек
        :param event_args: Информация о событии типа ControlEvent
        :return:
        """
        help_button.visible = not help_button.visible
        language_button.visible = not language_button.visible
        change_page_theme_button.visible = not change_page_theme_button.visible
        page.update()

    settings_button_title = ft.Ref[ft.Text]()
    settings_button = ft.MenuItemButton(
        style=ft.ButtonStyle(
            bgcolor={ft.ControlState.HOVERED: ft.colors.PINK_ACCENT_100,
                     ft.ControlState.PRESSED: ft.colors.BLACK54}
        ),
        leading=ft.Icon(ft.icons.SETTINGS),
        content=ft.Text(
            ref=settings_button_title,
            value=language_packs["ru"]["settings_title"]
        ),
        on_click=open_settings,
        tooltip=language_packs["ru"]["settings_title"]
    )
    # endregion

    # region Создание кнопки открытия документации к приложению
    def open_documentation(event_args):
        """
        Открывает документацию к приложению
        :param event_args: Информация о событии типа ControlEvent
        :return:
        """
        page.open(documentation_dialog)

    documentation = ft.Ref[ft.Text]()
    documentation_dialog = ft.AlertDialog(
        title=ft.Text(
            value=language_packs["ru"]["documentation"],
            ref=documentation,
            size=13
        ),
    )

    help_button_title = ft.Ref[ft.Text]()
    help_button = ft.MenuItemButton(
        style=ft.ButtonStyle(
            bgcolor={ft.ControlState.HOVERED: ft.colors.PINK_ACCENT_100}
        ),
        leading=ft.Icon(ft.icons.INFO),
        visible=False,
        content=ft.Text(
            ref=help_button_title,
            value=language_packs["ru"]["help_button_title"]
        ),
        tooltip=language_packs["ru"]["help_button_tooltip"],
        on_click=open_documentation
    )
    # endregion

    # region Создание кнопки выбора языка
    def choose_language_option(event_args, language):
        """
        Изменяет язык приложения на выбранный в выплывающем меню смены языка
        :param event_args: Информация о событии типа ControlEvent
        :param language: Выбранный язык
        :return:
        """
        settings_button_title.current.value = language_packs[language]["settings_title"]
        settings_button.tooltip = language_packs[language]["settings_tooltip"]
        help_button_title.current.value = language_packs[language]["help_button_title"]
        help_button.tooltip = language_packs[language]["help_button_tooltip"]
        language_button.tooltip = language_packs[language]["language_button_tooltip"]
        theme_mode_title.current.value = language_packs[language]["theme_button_title"]
        change_page_theme_button.tooltip = language_packs[language]["theme_button_tooltip"]

        num_of_decimal_places_title.current.value = language_packs[language]["decimal_places_title"]
        limit_message.current.value = language_packs[language]["decimal_places_message"]
        input_field_value.current.label = language_packs[language]["input_label"]
        if input_field_value.current.error_text:
            input_field_value.current.error_text = language_packs[language]["input_error_text"]
        output_field_value.current.hint_text = language_packs[language]["output_hint"]

        documentation.current.value = language_packs[language]["documentation"]
        page.update()

    chosen_language = ft.Ref[ft.Text]()
    russian_language_option = ft.dropdown.Option(
        text="Русский " + flag("RU"),
        text_style=ft.TextStyle(
            height=0.2
        ),
        disabled=False,
        on_click=lambda event_args: choose_language_option(event_args, "ru")
    )
    english_language_option = ft.dropdown.Option(
        text="English " + flag("US"),
        text_style=ft.TextStyle(
            height=0.2
        ),
        on_click=lambda event_args: choose_language_option(event_args, "en")
    )

    def switch_language_on_click(event_args):
        """
        Изменяет язык приложения на следующий по нажатию кнопки выбора языка
        :param event_args: Информация о событии типа ControlEvent
        :return:
        """
        if chosen_language.current.value == russian_language_option.text:
            choose_language_option(event_args, "en")
            chosen_language.current.value = english_language_option.text
        else:
            choose_language_option(event_args, "ru")
            chosen_language.current.value = russian_language_option.text
        page.update()

    language_button = ft.MenuItemButton(
        style=ft.ButtonStyle(
            bgcolor={ft.ControlState.HOVERED: ft.colors.PINK_ACCENT_100}
        ),
        visible=False,
        leading=ft.Icon(name=ft.icons.LANGUAGE),
        content=ft.Dropdown(
            ref=chosen_language,
            value="Русский " + flag("RU"),
            width=130,
            border_width=0,
            options=[
                russian_language_option,
                english_language_option
            ],
            dense=True
        ),
        width=160,
        on_click=switch_language_on_click,
        tooltip=language_packs["ru"]["language_button_tooltip"],
    )
    # endregion

    # region Создание кнопки смены темы приложения
    def change_page_theme(event_args):
        """
        Изменяет цвет темы приложения. (По умолчанию соответствует заданной системой теме)
        :param event_args: Информация о событии типа ControlEvent
        :return:
        """
        if page.theme_mode == page.theme_mode.DARK:
            page.theme_mode = page.theme_mode.LIGHT
            change_page_theme_button.leading = ft.Icon(ft.icons.LIGHT_MODE)
        else:
            page.theme_mode = page.theme_mode.DARK
            change_page_theme_button.leading = ft.Icon(ft.icons.DARK_MODE)
        page.update()

    if page.theme_mode.SYSTEM == page.theme_mode.SYSTEM.LIGHT:
        page.theme_mode = page.theme_mode.LIGHT
    else:
        page.theme_mode = page.theme_mode.DARK

    theme_mode_title = ft.Ref[ft.Text]()
    change_page_theme_button = ft.MenuItemButton(
        leading=ft.Icon(ft.icons.LIGHT_MODE) if page.theme_mode == page.theme_mode.LIGHT
        else ft.Icon(ft.icons.DARK_MODE),
        style=ft.ButtonStyle(
            bgcolor={ft.ControlState.HOVERED: ft.colors.PINK_ACCENT_100}
        ),
        visible=False,
        content=ft.Text(
            ref=theme_mode_title,
            value=language_packs["ru"]["theme_button_title"]
        ),
        on_click=change_page_theme,
        tooltip=language_packs["ru"]["theme_button_tooltip"]
    )
    # endregion

    # region Создание меню настроек
    settings = ft.MenuBar(
        style=ft.MenuStyle(
            bgcolor=ft.colors.PINK_ACCENT_200,
            mouse_cursor={
                ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
                ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
            },
            alignment=ft.alignment.top_left
        ),
        controls=[
            settings_button,
            help_button,
            language_button,
            change_page_theme_button
        ]
    )
    # endregion

    # region Создание кнопок выбора количества знаков после запятой для вычисленного значения корня
    num_of_decimal_places_title = ft.Ref[ft.Text]()
    num_of_decimal_places = ft.Ref[ft.TextField]()
    limit_message = ft.Ref[ft.Text]()
    num_reached_limit_message = ft.SnackBar(
        content=ft.Text(
            ref=limit_message,
            value=language_packs["ru"]["decimal_places_message"],
        ),
        duration=2500,
        show_close_icon=True
    )

    original_result = ""  # Неокруглённое значение корня заданного числа

    def update_output_field(result):
        """
        Обновляет поле вывода с учетом текущей точности
        :param result: Неокруглённое значение корня заданного числа
        :return:
        """
        if num_of_decimal_places.current.value == '':
            num_of_decimal_places.current.value = '0'
            result_precision.update()

        output_field_value.current.value = (str(around(
            a=result,
            decimals=int(num_of_decimal_places.current.value))).replace('j', 'i')
                                            .replace('(', '').replace(')', ''))
        output_field.update()

    def minus_click(event_args):
        """
        Уменьшает количество знаков после запятой на 1. (Минимум 0)
        :param event_args: Информация о событии типа ControlEvent
        :return:
        """
        if num_of_decimal_places.current.value == 0:
            page.open(num_reached_limit_message)
        else:
            num_of_decimal_places.current.value = int(num_of_decimal_places.current.value) - 1
            if original_result != "":
                update_output_field(original_result)
            result_precision.update()

    def plus_click(event_args):
        """
        Увеличивает количество знаков после запятой на 1. (Максимум 5)
        :param event_args: Информация о событии типа ControlEvent
        :return:
        """
        if num_of_decimal_places.current.value == 5:
            page.open(num_reached_limit_message)
        else:
            num_of_decimal_places.current.value = int(num_of_decimal_places.current.value) + 1
            if original_result != "":
                update_output_field(original_result)
            result_precision.update()

    def change_result_precision(event_args):
        """
        Изменяет точность вычисленного значения
        :param event_args: Информация о событии типа ControlEvent
        :return:
        """
        if len(event_args.control.value) > 1:
            event_args.control.value = event_args.control.value[:1]
        elif '0' <= event_args.control.value <= '5':
            num_of_decimal_places.current.value = event_args.control.value
            if original_result != "":
                update_output_field(original_result)
        else:
            num_of_decimal_places.current.value = ''
            page.open(num_reached_limit_message)
        result_precision.update()

    result_precision = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Text(
                ref=num_of_decimal_places_title,
                value=language_packs["ru"]["decimal_places_title"]
            ),
            ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
            ft.TextField(
                ref=num_of_decimal_places,
                value="3",
                hint_text="0-5",
                hint_style=ft.TextStyle(italic=True),
                text_align=ft.TextAlign.CENTER,
                width=50,
                input_filter=ft.NumbersOnlyInputFilter(),
                on_change=change_result_precision
            ),
            ft.IconButton(ft.icons.ADD, on_click=plus_click),
        ],
    )
    # endregion

    # region Создание полей ввода числа и вывода результата
    summand_pattern = re.compile(r"(\d+([.,]\d+)?[ℼeφ]*|[ℼeφ]+)")
    no_start_sign_real_num_pattern = re.compile(rf"""
        ({summand_pattern.pattern}           # Одно число
        ([-+]{summand_pattern.pattern})*)    # 0 и более последующих чисел
    """, re.VERBOSE)
    real_num_pattern = re.compile(rf"([-+]?{no_start_sign_real_num_pattern.pattern})")
    complex_number_pattern = re.compile(rf"""
        ^                                                                    # Начало строки
        (?:
        (?P<real_then_imag>                                                  # Группа 1: действительная + мнимая часть
            (?P<group1_real>{real_num_pattern.pattern})                      # Действительная часть
            (?P<group1_imag>[-+](?:{summand_pattern.pattern}?|               # Мнимая часть (опционально)
            \({real_num_pattern.pattern}\))
            i)?
        )|
        (?P<imag_then_real>                                                  # Группа 2: мнимая + действительная часть
            (?P<group2_imag>[-+]?(?:({summand_pattern.pattern}?)             # Мнимая часть
            |(\({real_num_pattern.pattern}\)))
            i)
            (?P<group2_real>[-+]{no_start_sign_real_num_pattern.pattern})?   # Действительная часть (опционально)
        ))
        $                                                                    # Конец строки
    """, re.VERBOSE)

    def validate_input(event_args):
        """
        Проверяет корректность введённого числа
        :param event_args: Информация о событии типа ControlEvent (введённое значение)
        :return: Введённое пользователем число, если оно соответствует заданному правилу, иначе None
        """
        match = complex_number_pattern.match(event_args.control.value)
        if match:
            event_args.control.error_text = None
            event_args.control.update()
            return match
        else:
            if input_field_value.current.value == "":
                event_args.control.error_text = None
            elif chosen_language.current.value == "Русский " + flag("RU"):
                event_args.control.error_text = language_packs["ru"]["input_error_text"]
            else:
                event_args.control.error_text = language_packs["en"]["input_error_text"]
            event_args.control.update()
            return None

    def evaluate_expression(expression):
        """
        Вычисляет выражение, переданное строкой
        :param expression: Выражение типа str
        :return: Приведённое к нужному виду и вычисленное выражение
        :exception ValueError: Если переданное выражение не соответствует заданным функцией eval правилам
        """
        if expression != '':
            expression = expression.replace('ℼ', 'pi').replace('φ', 'phi')
            expression = re.sub(r'(?<=\d)(?=[a-z])', '*', expression)  # Добавление умножения между цифрой и буквой
            expression = re.sub(r'(?<=[a-z])(?=\d)', '*', expression)  # Добавление умножения между буквой и цифрой
            expression = re.sub(r'(?<=[ie])(?=[ep])', '*', expression)  # Добавление умножения между буквами
        else:  # Если выражение пустое (действительная или мнимая часть отсутствуют)
            expression = "0"
        try:
            return eval(expression)
        except Exception:
            raise ValueError(f"Invalid expression: {expression}")

    def get_real_and_imag_parts(num):
        """
        Разбивает строку с комплексным числом на действительную и мнимую части
        :param num: Комплексное число в формате str
        :return: Пару значений типа float (или если отсутствует - None) действительной и мнимой части числа
        """
        real_part = None
        imaginary_part = None
        if num.group("real_then_imag"):  # Первый вариант (действительная + мнимая часть)
            real_part_expr = num.group("group1_real").replace(",", ".")
            real_part = evaluate_expression(real_part_expr)
            if num.group("group1_imag"):
                imag_part_expr = num.group("group1_imag").replace(",", ".")
                if imag_part_expr == '+i':
                    imaginary_part = 1
                elif imag_part_expr == '-i':
                    imaginary_part = -1
                else:
                    imaginary_part = evaluate_expression(imag_part_expr.replace('i', ''))
        else:  # Второй вариант (мнимая + действительная часть)
            imag_part_expr = num.group("group2_imag").replace(",", ".")
            if imag_part_expr == 'i':
                imaginary_part = 1
            elif imag_part_expr == '-i':
                imaginary_part = -1
            elif num.group("group2_imag"):
                imaginary_part = evaluate_expression(imag_part_expr.replace('i', ''))
            if num.group("group2_real"):
                real_part_expr = num.group("group2_real").replace(",", ".")
                real_part = evaluate_expression(real_part_expr)

        real_part = real_part if real_part is not None else 0.0
        imaginary_part = imaginary_part if imaginary_part is not None else 0.0
        return real_part, imaginary_part

    def complex_sqrt(event_args):
        """
        Вычисляет квадратный корень из введённого комплексного числа
        :param event_args: Информация о событии типа ControlEvent (введённое значение)
        :return:
        """
        nonlocal original_result
        if len(event_args.control.value) > 29:  # Ограничение на количество вводимых символов
            event_args.control.value = event_args.control.value[:29]
            event_args.control.update()
            return

        num = validate_input(event_args)
        if num is not None:
            real_part, imag_part = get_real_and_imag_parts(num)
            sqrt_num = sqrt(complex(real_part, imag_part))

            if sqrt_num.imag:
                original_result = sqrt_num
            else:
                original_result = sqrt_num.real
            update_output_field(original_result)
        else:
            output_field_value.current.value = None
            output_field.update()

    input_field_value = ft.Ref[ft.TextField]()
    input_field = ft.Row(
        width=300,
        controls=[
            ft.TextField(
                autofocus=True,
                label=language_packs["ru"]["input_label"],
                prefix_text='√',
                prefix_style=ft.TextStyle(weight=ft.FontWeight.W_600),
                on_change=complex_sqrt,
                ref=input_field_value
            )
        ]
    )

    output_field_value = ft.Ref[ft.TextField]()
    output_field = ft.Row(
        width=300,
        controls=[
            ft.TextField(
                prefix_text='=',
                prefix_style=ft.TextStyle(
                    weight=ft.FontWeight.W_600
                ),
                hint_text=language_packs["ru"]["output_hint"],
                read_only=True,
                ref=output_field_value
            )
        ]
    )

    input_output_field = ft.Column(
        controls=[
            input_field,
            output_field
        ],
    )
    # endregion

    # region Создание клавиатуры
    def write_symbol(event_args):
        """
        Добавляет символ с клавиатуры в поле ввода числа
        :param event_args: Информация о событии типа ControlEvent
        :return:
        """
        input_field_value.current.value += event_args.control.text
        fake_event = ft.ControlEvent(
            target="",
            name="",
            data="",
            page=None,
            control=input_field_value.current)
        complex_sqrt(fake_event)
        input_field.update()

    def delete_input(event_args):
        """
        Очищает поле ввода числа
        :param event_args: Информация о событии типа ControlEvent
        :return:
        """
        nonlocal original_result
        input_field_value.current.value = ""
        input_field.update()
        output_field_value.current.value = ""
        output_field.update()
        original_result = ""

    def delete_symbol(event_args):
        """
        Удаляет последний символ в поле ввода числа
        :param event_args: Информация о событии типа ControlEvent
        :return:
        """
        nonlocal original_result
        input_field_value.current.value = input_field_value.current.value[:-1]
        input_field.update()
        if input_field_value.current.value == '':
            original_result = ''
        fake_event = ft.ControlEvent(
            target="",
            name="",
            data="",
            page=None,
            control=input_field_value.current)
        complex_sqrt(fake_event)
        output_field.update()

    keyboard = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.ElevatedButton(text="CE", on_click=delete_input),
                    ft.ElevatedButton(text="⌫", on_click=delete_symbol),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton(text="ℼ", on_click=write_symbol),
                    ft.ElevatedButton(text="i", on_click=write_symbol),
                    ft.ElevatedButton(text="e", on_click=write_symbol),
                    ft.ElevatedButton(text="φ", on_click=write_symbol),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton(text="7", on_click=write_symbol),
                    ft.ElevatedButton(text="8", on_click=write_symbol),
                    ft.ElevatedButton(text="9", on_click=write_symbol),
                    ft.ElevatedButton(text="-", on_click=write_symbol),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton(text="4", on_click=write_symbol),
                    ft.ElevatedButton(text="5", on_click=write_symbol),
                    ft.ElevatedButton(text="6", on_click=write_symbol),
                    ft.ElevatedButton(text="+", on_click=write_symbol),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton(text="1", on_click=write_symbol),
                    ft.ElevatedButton(text="2", on_click=write_symbol),
                    ft.ElevatedButton(text="3", on_click=write_symbol),
                    ft.ElevatedButton(text=".", on_click=write_symbol),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton(text="0", on_click=write_symbol),
                    ft.ElevatedButton(text="(", on_click=write_symbol),
                    ft.ElevatedButton(text=")", on_click=write_symbol),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
    )
    # endregion

    # region Настройка расположения элементов интерфейса
    settings_container = ft.Container(
        alignment=ft.alignment.top_left,
        content=settings,
        width=page.width
    )

    main_container = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        controls=[
            input_output_field,
            keyboard
        ]
    )

    body = ft.Container(
        content=ft.Stack(
            controls=[
                result_precision,
                main_container
            ],
        ),
        expand=True,
        width=page.width,
    )

    page.add(settings_container)
    page.add(body)
    # endregion


ft.app(target=sqrt_calc)
