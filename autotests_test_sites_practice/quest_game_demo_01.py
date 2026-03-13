def start_game():
    print("Добро пожаловать в квест!")
    print("Вы стоите перед тремя дверями.")
    print("1. Дверь слева (красная)")
    print("2. Дверь по центру (синяя)")
    print("3. Дверь справа (чёрная)")

    choice = input("Какую дверь выберете? (1/2/3): ")

    if choice == "1":
        red_door()
    elif choice == "2":
        blue_door()
    elif choice == "3":
        black_door()
    else:
        print("Неверный выбор!")
        start_game()


def red_door():
    print("Вы вошли в красную дверь.")
    print("Перед вами сундук с сокровищами!")
    print("1. Открыть сундук")
    print("2. Уйти")

    choice = input("Что сделаете? (1/2): ")

    if choice == "1":
        print("🎉 Вы нашли золото! Победа!")
    else:
        print("Вы ушли ни с чем...")
        start_game()


def blue_door():
    print("Вы вошли в синюю дверь.")
    print("Перед вами мост через пропасть.")
    print("1. Перейти мост")
    print("2. Вернуться")

    choice = input("Что сделаете? (1/2): ")

    if choice == "1":
        print("🌉 Мост обрушился! Вы погибли...")
    else:
        start_game()


def black_door():
    print("Вы вошли в чёрную дверь.")
    print("Там темно и страшно...")
    print("Вы слышите шорох...")
    print("1. Пойти на звук")
    print("2. Побежать обратно")

    choice = input("Что сделаете? (1/2): ")

    if choice == "1":
        print("👻 Это был призрак! Вы погибли...")
    else:
        start_game()


# Запуск игры
start_game()