import csv
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


FILE_NAME = "sessions.csv"

def normalize_date(date_str):
    formats = ["%Y-%m-%d", "%d-%m-%Y", "%d.%m.%Y", "%d/%m/%Y", "%Y/%m/%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return date_str

def load_sessions():
    sessions = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["цена"] = int(row["цена"])
                row["дата"] = normalize_date(row["дата"])
                sessions.append(row)
    return sessions

def save_sessions(sessions):
    with open(FILE_NAME, mode="w", encoding="utf-8", newline="") as file:
        fieldnames = ["клиент", "услуга", "цена", "дата"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for session in sessions:
            writer.writerow(session)

sessions = load_sessions()

def add_sessions():
    client = input("Имя клиента: ")
    service = input("Услуга:")
    price = int(input("Цена: "))
    date = normalize_date(input("Дата (ГГГГ-ММ-ДД): "))

    session = {
      "клиент": client,
      "услуга": service,
      "цена": price,
      "дата": date
    }
    sessions.append(session)
    save_sessions(sessions)
    print(f"Сеанс для {client} добавлен!\n")

def show_all_sessions():
    if not sessions:
        print("Нет данных.\n")
        return
    print("\nВСЕ СЕАНСЫ")
    print("-" * 60)
    print(f"{'№':<4} {'Клиент':<15} {'Услуга':<20} {'Цена':<8} {'Дата':<12}")
    print("-" * 60)

    for i, s in enumerate(sessions, start=1):
        print(f"{i:<4} {s['клиент']:<15} {s['услуга']:<20} {'цена':<8} {s['дата']:<12}")

    print("-" * 60)
    print(f"Всего записей: {len(sessions)}")
    print()

def delete_session():
    if not sessions:
        print("Нет данных для удаления.\n")
        return

    show_all_sessions()

    try:
        num = int(input("Введите номер записи для удаления (или 0 для отмены): "))
    except ValueError:
        print("Нужно ввести число.\n")
        return

    if num == 0:
        print("Отмена.\n")
        return

    removed = sessions.pop(num - 1)
    save_sessions(sessions)
    print(f"Запись для {removed['клиент']} удалена.\n")

def edit_session():
    if not sessions:
        print("Нет данных для редактирования.\n")
        return

    show_all_sessions()

    try:
        num = int(input("Введите номер записи для редактирования (или 0 для отмены): "))
    except ValueError:
        print("Нужно ввести число.\n")
        return

    if num == 0:
        print("Отмена.\n")
        return

    if num < 1 or num > len(sessions):
        print("Такого  номера нет.\n")
        return

    session = sessions[num - 1]
    print(f"\nТекущие данные:")
    print(f"Клиент: {session['клиент']}")
    print(f"Услуга: {session['услуга']}")
    print(f"Цена: {session['цена']}")
    print(f"Дата: {session['дата']}")

    print("\nЧто меняем?  (оставьте пустым, чтобы не менять)")
    new_client = input(f"Клиент [{session['клиент']}]:").strip()
    new_service = input(f"Услуга [{session['услуга']}]:").strip()
    new_price = input(f"Цена [{session['цена']}]:").strip()
    new_date = input(f"Дата [{session['дата']}]:").strip()

    if new_client:
        session['клиент'] = new_client
    if new_service:
        session['услуга'] = new_service
    if new_price:
        session['цена'] = int(new_price)
    if new_date:
        session['дата'] = normalize_date(new_date)

    save_sessions(sessions)
    print("Запись обновлена.\n")
    
def show_report():
    if not sessions:
        print ("Нет данных для отчета.\n")
        return

    total = sum(s["цена"] for s in sessions)
    average = total / len(sessions)

    service_count = {}
    for s in sessions:
        service = s["услуга"]
        service_count[service] = service_count.get(service, 0) + 1

    popular = max(service_count, key=service_count.get)

    print("\n ОТЧЕТ")
    print(f"Всего сеансов: {len(sessions)}")
    print(f"Общая выручка: {total} руб.")
    print(f"Средний чек: {round(average, 2)} руб.")
    print(f"Самая популярная услуга: {popular} ({service_count[popular]} раз)")
    print(f"Уникальных клиентов: {len(set(s['клиент'] for s in sessions))}")
    print()

def show_report_by_month():
    if not sessions:
        print("Нет данных для отчета.\n")
        return

    month_input = input("Введите месяц (ГГГГ-ММ, ММ-ГГГГ, ММ.ГГГГ): ").strip()

    month = None
    for fmt in ("%Y-%m", "%m-%Y", "%m.%Y", "%m/%Y"):
        try:
            month = datetime.strptime(month_input, fmt).strftime("%Y-%m")
            break
        except ValueError:
            continue

    if month is None:
        print("Не удалось распознать месяц. Введите, например: 2026-09 или 09.2026\n")
        return

    filtered = [s for s in sessions if s["дата"].startswith(month)]

    if not filtered:
        print(f"Нет данных за {month}.\n")
        return

    total = sum(s["цена"] for s in filtered)
    average = total / len(filtered)

    service_count = {}
    for s in filtered:
        service = s["услуга"]
        service_count[service] = service_count.get(service, 0) + 1

    popular = max(service_count, key=service_count.get)

    print(f"\nОТЧЕТ ЗА {month}")
    print(f"Всего сеансов: {len(filtered)}")
    print(f"Общая выручка: {total} руб.")
    print(f"Средний чек: {round(average, 2)} руб.")
    print(f"Самая популярная услуга: {popular} ({service_count[popular]} раз)")
    print(f"Уникальных клиентов: {len(set(s['клиент'] for s in filtered))}")
    print()

def show_charts():
    if not sessions:
        print("Нет данных для графиков.\n")(sessions)
        return

    df = pd.DataFrame(sessions)
    df['дата'] = pd.to_datetime(df['дата'])

    plt.style.use('seaborn-v0_8-darkgrid')
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    revenue_by_service = df.groupby('услуга')['цена'].sum().sort_values()
    axes[0].barh(revenue_by_service.index, revenue_by_service.values, color='skyblue')
    axes[0].set_title('Выручка по услугам')
    axes[0].set_xlabel('Сумма (руб.)')

    revenue_by_date = df.groupby('дата')['цена'].sum()
    axes[1].plot(revenue_by_date.index, revenue_by_date.values, marker='o', color='green')
    axes[1].set_title('Выручка по датам')
    axes[1].set_xlabel('Дата')
    axes[1].set_ylabel('Сумма (руб.)')
    axes[1].tick_params(axis='x', rotation=45)

    service_counts = df['услуга'].value_counts()
    axes[2].pie(service_counts.values,labels=service_counts.index, autopct='%1.1f%%', startangle=90)
    axes[2].set_title('Популярность услуг')

    plt.tight_layout()
    plt.show()    

while True:
    print("1. Добавить сеанс")
    print("2. Показать отчет")
    print("3. Показать отчет за месяц")
    print("4. Показать всех клиентов")
    print("5. Удалить запись")
    print("6. Редактировать запись")
    print("7. Показать графики")
    print("8. Выйти")
    choice = input("Выберите действие: ")

    if choice == "1":
        add_sessions()
    elif choice == "2":
        show_report()
    elif choice == "3":
        show_report_by_month()
    elif choice == "4":
        show_all_sessions()
    elif choice == "5":
        delete_session()
    elif choice == "6":
        edit_session()
    elif choice == "7":
        show_charts()
    elif choice == "8":
        print("До встречи!")
        break
    else:
        print("Неверный выбор. Попробуйте снова.\n")
