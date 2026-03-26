import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# --- Настройки ---
FILE_TYPES = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".heic"],
    "documents": [".doc",".pdf", ".docx", ".txt", ".xlsx"],
    "videos": [".mp4", ".mov", ".avi"],
    "archives": [".zip", ".rar", ".7z"],
    "program": [".exe", ".bin", ".app"],
    "web": [".html", ".htm"]
}

def organize_files(folder_path, selected_categories, template):
    if not os.path.exists(folder_path):
        messagebox.showerror("Ошибка", "Папка не существует!")
        return

    counters = {}

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename) #Путь к файлу с которым мы сейчас работаем

        if os.path.isfile(file_path):
            name, ext = os.path.splitext(filename) #Достаем имя файла и расширение
            ext = ext.lower()

            # Определяем категорию
            category = "other"
            for key, extensions in FILE_TYPES.items():
                if ext in extensions:
                    category = key
                    break

            # Фильтр по выбранным категориям
            category_folder = os.path.join(folder_path, category)
            os.makedirs(category_folder, exist_ok=True) #Создаем папку для категории

            counters.setdefault(category, 0)
            counters[category] += 1 #Счетчик файлов в категории

            #Получаем дату создания файла и преобразуем в удобный формат
            create_time = os.path.getctime(file_path)
            date = datetime.fromtimestamp(create_time)
            date_str = date.strftime("%Y-%m-%d")

            # --- ШАБЛОН ---
            new_name = template.format(
                name=name,
                date=date_str,
                category=category,
                num=counters[category]
            ) + ext

            new_path = os.path.join(category_folder, new_name)

            shutil.move(file_path, new_path)

    messagebox.showinfo("Готово", "Файлы отсортированы!")

# ---------------- GUI ----------------

def choose_folder():
    path = filedialog.askdirectory()  #Открываем окно выбора папки
    folder_path.set(path)

def start_sorting():
    path = folder_path.get()

    if not path:
        messagebox.showerror("Ошибка", "Выберите папку!") #Проверяем выбор папки
        return

    selected_categories = [
        key for key, var in category_vars.items() if var.get() #Собираем выбранные категории
    ]

    if not selected_categories:
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип файлов!") #Проверяем выбор
        return

    template = template_var.get()   #Получаем шаблон имени файла

    if not template:
        messagebox.showerror("Ошибка", "Введите шаблон имени!")
        return

    organize_files(path, selected_categories, template)

# --- Окно ---
root = tk.Tk()
root.title("Сортировка файлов")
root.geometry("500x500")

folder_path = tk.StringVar()
template_var = tk.StringVar(value="{name}_{date}_{category}_{num}")

# Заголовок
tk.Label(root, text="Автоматизация файлов", font=("Arial", 14)).pack(pady=10)

# Выбор папки
tk.Label(root, text="Путь к папке:").pack()
tk.Entry(root, textvariable=folder_path, width=50).pack(pady=5)
tk.Button(root, text="Выбрать папку", command=choose_folder).pack(pady=5)

# Выбор категорий
tk.Label(root, text="Типы файлов:").pack(pady=10)

category_vars = {}
for category in FILE_TYPES.keys():
    var = tk.BooleanVar(value=True)
    category_vars[category] = var
    tk.Checkbutton(root, text=category, variable=var).pack()

# Шаблон имени
tk.Label(root, text="Шаблон имени файла:").pack(pady=10)
tk.Entry(root, textvariable=template_var, width=50).pack()

tk.Label(root, text="Доступные переменные:\n{name}, {date}, {category}, {num}").pack()

# Кнопка запуска
tk.Button(root, text="Запустить", command=start_sorting, bg="green", fg="white").pack(pady=20)

root.mainloop()