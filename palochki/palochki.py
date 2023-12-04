import tkinter as tk
import random
import tempfile, base64, zlib # нужна, чтобы совсем убирать иконку слева 
import pygame
 
# иконки в левом верхнем углу программы вообще не будет (совсем ничего нет, пусто) 
# раскомментировать строки 9 - 13, 91.
# закомментировать строки  90.
# ICON = zlib.decompress(base64.b64decode("eJxjYGAEQgEBBiDJwZDBysAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc="))
 
# _, ICON_PATH = tempfile.mkstemp()
# with open(ICON_PATH, "wb") as icon_file:
#     icon_file.write(ICON)

total_sticks = 20  # Изначально всего палочек 20

muted = False # Флаг для отслеживания состояния звука

def user_took_sticks(user_took):  # Функция для взятия палочек пользователем
    global total_sticks
    total_sticks -= user_took
    if not muted: # Проверка состояния звука
        pygame.mixer.init()
        pygame.mixer.music.load("wav/korotkiy-schelchok-kompyuternoy-myishi.wav")
        pygame.mixer.music.play()
    label_pile.config(text=f"Палочек осталось  {total_sticks}")
    sticks.config(text=total_sticks * "| ")
    if total_sticks == 1:  # Если осталась последняя палочка
        user_won()  # Выиграл игрок
    else:
        comp_choice = (total_sticks - 1) % 4 if (total_sticks - 1) % 4 != 0 else random.choice([1, 2, 3])
        total_sticks -= comp_choice
        label_computer_progress.config(text=f"Компьютер взял  {comp_choice}")
        label_pile.config(text=f"Палочек осталось  {total_sticks}")
        sticks.config(text=total_sticks * "| ")
        if total_sticks == 1:  # Если осталась последняя палочка
            computer_won()  # Выйграл компьютер

def computer_won():  # Выиграл компьютер
    label_computer_progress.config(text="Победил компьютер! Попробуй ещё раз.", fg='red', font=('Arial', 20, 'bold'))
    if not muted: # Проверка состояния звука
        pygame.mixer.init()
        pygame.mixer.music.load("wav/opoveschenie-o-proigryishe.wav")
        pygame.mixer.music.play()
    disable_buttons()

def user_won():  # Выиграл пользователь
    label_computer_progress.config(text="Молодец!  Вы выиграли!", fg='green', font=('Arial', 25, 'bold'))
    if not muted: # Проверка состояния звука
        pygame.mixer.init()
        pygame.mixer.music.load("wav/game-won.wav")
        pygame.mixer.music.play()
        disable_buttons()

def disable_buttons():  # Отключение кнопок после окончания игры
    button1.config(state=tk.DISABLED)
    button2.config(state=tk.DISABLED)
    button3.config(state=tk.DISABLED)
    button_play_again.config(state=tk.NORMAL, bg='aqua')

def play_again():  # Начать новую игру
    global total_sticks
    total_sticks = 20
    label_pile.config(text=f"Всего  {total_sticks}  палочек", font=("Arial", 12), fg='black')
    sticks.config(text=total_sticks * "| ")
    label_computer_progress.config(text="", font=("Arial", 12), fg='black')
    button1.config(state=tk.NORMAL)
    button2.config(state=tk.NORMAL)
    button3.config(state=tk.NORMAL)
    button_play_again.config(state=tk.DISABLED, bg='gray90', font=("Arial", 12, 'bold'), fg='green')
    if not muted: # Проверка состояния звука
        pygame.mixer.init()
        pygame.mixer.music.load("wav/zvuk-pobedyi-vyiigryisha.wav")
        pygame.mixer.music.play()

def mute_music():
    global muted
    if muted:
        pygame.mixer.init()
        volumeButton.configure(image=volumePhoto)
        muted = False
    else:
        pygame.mixer.init()
        volumeButton.configure(image=mutePhoto)
        muted = True

root = tk.Tk()
root.title('Игра "Палочки"')
root.geometry('600x300')
root.iconbitmap(default="png/iconka.ico") # зададим иконку в левом углу окна программы
# root.iconbitmap(default=ICON_PATH) # иконки в левом верхнем углу программы вообще не будет (совсем ничего нет, пусто)
root.resizable(False, False) # запретим растягивать окно программы

label_pravilo = tk.Label(root, text="Проигрывает тот, кому достанется последяя палочка.", font=("Arial", 12, 'bold'), fg='violet')
label_pravilo.pack()

label_pile = tk.Label(root, text=f"Всего  {total_sticks}  палочек", font=("Arial", 12, 'bold'), fg='black')
label_pile.pack()

sticks = tk.Label(root, text=total_sticks * "| ")  # Выводим палочки на экран
sticks.config(font=("Arial", 35, 'bold'))  # Устанавливаем шрифт Arial, размер текста 30 и делаем его жирным
sticks.pack()

label_propusk = tk.Label(root, text="")
label_propusk.pack()

label_computer_progress = tk.Label(root, text="", font=("Arial", 12), fg='black', anchor=tk.CENTER)
label_computer_progress.pack()

text1 = tk.Label(root, text="Сколько палочек будем брать?", font=("Arial", 12), fg='black')
text1.pack()

button1 = tk.Button(root, text="1 палочку", font=("Arial", 12, 'bold'),command=lambda: user_took_sticks(1))
button1.place(x=100, y=200)

button2 = tk.Button(root, text="2 палочки", font=("Arial", 12, 'bold'),command=lambda: user_took_sticks(2))
button2.place(x=270, y=200)

button3 = tk.Button(root, text="3 палочки", font=("Arial", 12, 'bold'),command=lambda: user_took_sticks(3))
button3.place(x=420, y=200)

button_play_again = tk.Button(root, fg='green', bg='gray90', text="Играть ещё раз", font=("Arial", 12, 'bold'), command=play_again, state=tk.DISABLED)
button_play_again.place( x=245, y=250 )

mutePhoto = tk.PhotoImage(file="png/free-icon-mute-2698118.png")
volumePhoto = tk.PhotoImage(file="png/free-icon-volume-up-3643435.png")
volumeButton = tk.Button(root, image=volumePhoto, command=mute_music)
volumeButton.place(x=545, y=248)

root.mainloop()

# Код разработал "Yurdos".

# Этот код создает игру "Палочки", где вы играете против компьютера.
# Код использует библиотеку tkinter для создания графического интерфейса игры,
# библиотеку random для выборки случайного числа хода компьютера при определённой логической ситуации.
# Библиотеки tempfile, base64, zlib используются для удаления логотипа слева вверху (можно не комментить).
# Бибилиотека pygame применяется для музыкального сопровождения.

# Играют двое: Игрок и Компьютер.
# На столе лежат 20 палочек.
# Ходы делаются по очереди.
# За один ход можно взять одну, две или три палочки.
# Игрок, который возьмёт последнюю палочку - проиграл.

# Алгоритм:
# Расчёт произведёт от концовки игры, где для выигрыша (после хода осталась 1 палочка)
# нужно не более 4-х палочек, а предыдущий ход минимум 1 палочка у другого игрока.
# Таким образом проигрышная позиция считается как 1 + 4 = 5 палочек перед вашим ходом.
# И всё это повторяется через 4 палочки. 
# Проигрышные позиции: 1 , 5 , 9 , 13 , 17 палочек.
# Компьютер будет стараться загнать вас в эти позиции с самого своего первого хода.
# У игрока есть преимущество - именно игрок начинает игру.
#                                           У Д А Ч И !

# Кнопки для mute заимствованы с сайта flaticon.com

#  Билдинг в exe самораспаковывающуюся папку:
#  pyinstaller -w -i "D:\Developing\Python\palochki\iconka.ico" palochki.py
# добавляем папки wav и png
# запаковываем в exe файл.
# распаковка: Создаем каталог в месте игр, копируес exe файл, запускаем, 
# можно создать ярлык на рабочий стол из файла palochki.exe.
# Пользуйтесь...


#  Билдинг в exe файл только для 1 файла py:
# pyinstaller palochki.py --clean -F -i "iconка.ico" -w