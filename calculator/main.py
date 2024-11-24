import tkinter as tk
import math


# Проверяем введенное выражение на корректность и считаем его. Добавлена проверка деления на 0, а также опечатки
def check_expression(expression):
    try:
        result = eval(expression)
        return result
    except ZeroDivisionError:
        return "На ноль делить нельзя"
    except Exception:
        return "Ошибка в выражении"


# Функция обработки нажатия на кнопку. Получаем уже введенное выражение или цифры, удаляем старый текст или записываем
# новый.Пример - мы ввели число 9, захотели добавить /, тогда программа выцепит 9 из инпут бокса, удалит 9 и запишет 9/
def button_click(value):
    current_text = input_box.get()
    input_box.delete(0, tk.END)
    input_box.insert(0, current_text + value)


# Функция для отчистки окна ввода
def clear_input():
    input_box.delete(0, tk.END)


# Функция подсчета результата. Получаем введенное выражение и считаем ее через первую функцию,
# результат выводим в окно ввода
def calculate_result():
    expression = input_box.get()
    result = check_expression(expression)
    input_box.delete(0, tk.END)
    input_box.insert(0, str(result))


# Рисуем кнопки. Их, конечно, можно было сделать через Tkinter, но хотелось добавить стилей, поэтому было принято
# решение их отрисовать. Сначала рисуем прямоугольник определенного размера, заполняем его цветом, а внутри квадрата
# добавлем лейбл в виде текста (цифры / функции и тп). Далее добавляем обработку клика на эти кнопки. "<Button-1>"
# отвечает за нажатие левой кнопкой мыши. Таким образом, не важно нажмем мы на область прямоугольника или текста, будет
# реализовано нажатие
def create_button(x, y, width, height, text, color, action):
    button = canvas.create_rectangle(x, y, x + width, y + height, fill=color, outline="white", width=2)
    label = canvas.create_text(
        x + width / 2, y + height / 2, text=text, font=button_font, fill="white"
    )
    canvas.tag_bind(button, "<Button-1>", lambda n: action())
    canvas.tag_bind(label, "<Button-1>", lambda n: action())


# Доп функционал. Решила добавить интересных функций: синус, косинус, натуральный логарифм и возведение в квадрат.
# Если текст введен, то мы получаем название математичской функции, которую ввел пользователь, проверяем на корректность
# (например, у логарифма число не отрицательное) и встроенными функциями из библиотеки math получаем результат. Есть
# проверки, если пользователь введ неизвестную операцию, некорректное число или забыл ввести висло. Результат
# записывается в окно ввода
def extra_functions(func):
    current_text = input_box.get()
    if current_text:
        try:
            num = float(current_text)
            if func == "sin":
                result = math.sin(num)
            elif func == "cos":
                result = math.cos(num)
            elif func == "ln":
                if num > 0:
                    result = math.log(num)
                else:
                    input_box.delete(0, tk.END)
                    input_box.insert(0, "Логарифм отрицательного числа")
                    return
            elif func == "^2":
                result = num ** 2
            else:
                input_box.delete(0, tk.END)
                input_box.insert(0, "Неизвестная операция")
                return
            input_box.delete(0, tk.END)
            input_box.insert(0, str(result))
        except ValueError:
            input_box.delete(0, tk.END)
            input_box.insert(0, "Введите корректное число")
    else:
        input_box.delete(0, tk.END)
        input_box.insert(0, "Введите число для операции")


# Рисуем модальное окно, задаем параметры и размеры для объектов, расчитываем размеры окна, задаем дизайн
window = tk.Tk()
window.title("Калькулятор Ульяны Смирновой!")
button_width = 80
button_height = 50
gap = 10
columns = 5
rows = 5
screen_height = 80

window_width = button_width * columns + gap * (columns + 1)
window_height = screen_height + (button_height + gap) * (rows + 1) + gap
window.geometry(f"{window_width}x{window_height}")
window.resizable(False, False)

digit_color = "black"
operator_color = "#8000FF"
button_font = ("Arial", 18, "bold")

canvas = tk.Canvas(window, bg="#FF0080", width=window_width, height=window_height)
canvas.pack(fill="both", expand=True)

input_box = tk.Entry(window, font=("Arial", 24), justify="right", bd=0)
canvas.create_window(window_width // 2, screen_height // 2, window=input_box, width=window_width - 2 * gap)

# Расположение кнопок
buttons = [
    "1", "2", "3", "/", "sin",
    "4", "5", "6", "*", "cos",
    "7", "8", "9", "-", "ln",
    "0", ".", "C", "+", "^2"
]
# Координаты для кнопок
x_start = gap
y_start = screen_height + gap
current_x = x_start
current_y = y_start

# Рисуем кнопки. Циклом проходим по всем кнопкам, задаем цвета и отрисовываем на эране. Каждый раз смещаем координаты,
# чтобы кнопки не склеились и не наложились друг на друга
for index, button in enumerate(buttons):
    if button.isdigit() or button == ".":
        color = digit_color
    else:
        color = operator_color

    if button in ["sin", "cos", "ln", "^2"]:
        action = lambda f=button: extra_functions(f)
    elif button == "C":
        action = clear_input
    else:
        action = lambda x=button: button_click(x)

    create_button(current_x, current_y, button_width, button_height, button, color, action)
    current_x += button_width + gap
    if (index + 1) % columns == 0:
        current_x = x_start
        current_y += button_height + gap

# Напоследок не забудем нарисовать кнопку равенства, которая выводит итоговый результат
equal_width = button_width * columns + gap * (columns - 1)
create_button(x_start, current_y, equal_width, button_height, "=", "#64183F", calculate_result)

# Отображаем наше окно с лучшим и самым красивым калькулятором!
window.mainloop()
