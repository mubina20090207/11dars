import sqlite3

def display_menu():
    print("\n--- Autosalon Boshqaruv Paneli ---")
    print("1. Barcha modellarni brand nomi va rangi bilan ko'rish")
    print("2. Xodimlar va buyurtmachilarning email'larini birlashtirish")
    print("3. Har bir davlatda nechtadan buyurtmachi borligini hisoblash")
    print("4. Har bir davlatdan nechtadan xodim borligini hisoblash")
    print("5. Har bir brandda nechtadan model borligini chiqarish")
    print("6. 5 tadan ko'p modellar mavjud bo'lgan brandlarni chiqarish")
    print("7. Orders jadvalini boshqa jadval bilan birlashtirib ko'rish")
    print("8. Avtomobillarning umumiy narxini hisoblash")
    print("9. Jami brandlar sonini chiqarish")
    print("10. Yangi ma'lumotlarni qo'shish")
    print("0. Dasturdan chiqish")

def query_and_display(cursor, query, description):
    print(f"\n--- {description} ---")
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def main():
    conn = sqlite3.connect("autosalon.db")
    cursor = conn.cursor()

    while True:
        display_menu()
        choice = input("Tanlovni kiriting: ")

        if choice == "1":
            query = """
                SELECT models.name, brands.name AS brand, models.color
                FROM models
                JOIN brands ON models.brand_id = brands.id
            """
            query_and_display(cursor, query, "Barcha modellar, brendlari va ranglari")

        elif choice == "2":
            query = """
                SELECT email FROM employees
                UNION
                SELECT email FROM customers
            """
            query_and_display(cursor, query, "Xodimlar va buyurtmachilar email'lari")

        elif choice == "3":
            query = """
                SELECT country, COUNT(*) AS count
                FROM customers
                GROUP BY country
                ORDER BY count DESC
            """
            query_and_display(cursor, query, "Har bir davlatda buyurtmachilar soni")

        elif choice == "4":
            query = """
                SELECT country, COUNT(*) AS count
                FROM employees
                GROUP BY country
                ORDER BY count DESC
            """
            query_and_display(cursor, query, "Har bir davlatdan xodimlar soni")

        elif choice == "5":
            query = """
                SELECT brands.name, COUNT(models.id) AS model_count
                FROM brands
                JOIN models ON brands.id = models.brand_id
                GROUP BY brands.name
            """
            query_and_display(cursor, query, "Har bir branddagi modellar soni")

        elif choice == "6":
            query = """
                SELECT brands.name, COUNT(models.id) AS model_count
                FROM brands
                JOIN models ON brands.id = models.brand_id
                GROUP BY brands.name
                HAVING model_count > 5
            """
            query_and_display(cursor, query, "Modellar soni 5 tadan ko'p bo'lgan brandlar")

        elif choice == "7":
            query = """
                SELECT orders.id, customers.name AS customer, employees.name AS employee, models.name AS model
                FROM orders
                JOIN customers ON orders.customer_id = customers.id
                JOIN employees ON orders.employee_id = employees.id
                JOIN models ON orders.model_id = models.id
            """
            query_and_display(cursor, query, "Orders jadvali boshqa jadval bilan birlashtirildi")

        elif choice == "8":
            query = "SELECT SUM(price) AS total_price FROM models"
            query_and_display(cursor, query, "Barcha avtomobillarning umumiy narxi")

        elif choice == "9":
            query = "SELECT COUNT(*) AS brand_count FROM brands"
            query_and_display(cursor, query, "Jami brandlar soni")

        elif choice == "10":
            table = input("Ma'lumot kiritmoqchi bo'lgan jadval nomini kiriting (e.g., customers, employees, models): ")
            columns = input(f"{table} jadvali uchun ustun nomlarini vergul bilan ajratib kiriting: ")
            values = input(f"{table} jadvali uchun ma'lumotlarni vergul bilan ajratib kiriting: ")
            query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
            try:
                cursor.execute(query)
                conn.commit()
                print("Ma'lumot muvaffaqiyatli qo'shildi!")
            except Exception as e:
                print(f"Xato: {e}")

        elif choice == "0":
            print("Dasturdan chiqilmoqda...")
            break

        else:
            print("Noto'g'ri tanlov, qayta urinib ko'ring.")

    conn.close()

if __name__ == "__main__":
    main()
