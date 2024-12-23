import sqlite3


DATABASE_PATH = 'telegram.db'

def get_doctors():
    """Возвращает список врачей."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, specialty FROM doctors")
    doctors = cursor.fetchall()
    conn.close()
    return doctors

def get_services():
    """Возвращает список услуг."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, description FROM services")
    services = cursor.fetchall()
    conn.close()
    return services

def get_reviews():
    """Возвращает список отзывов."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT text, rating FROM reviews")
    reviews = cursor.fetchall()
    conn.close()
    return reviews

def book_appointment(user_id, doctor_id, service_id, date, time):
    """Записывает данные о новой записи (id пользователя, id доктора, id услуги, дату и время) в таблицу appointments
     базы данных, возвращая True в случае успеха и False в случае ошибки."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO appointments (user_id, doctor_id, service_id, date, time)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, doctor_id, service_id, date, time))
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Ошибка при записи в базу данных: {e}")
        return False
    finally:
        conn.close()

def get_dates():
    """Возвращает список дат."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT date FROM doctors")
    dates = cursor.fetchall()
    conn.close()
    return dates

def get_times():
    """Возвращает список времени."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT time FROM doctors")
    times = cursor.fetchall()
    conn.close()
    return times

def get_doctor_by_id(doctor_id):
    """Извлекает данные доктора из таблицы “doctors” по его ID и возвращает их в виде словаря."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
        doctor = cursor.fetchone()
        if doctor:
            return dict(zip([description[0] for description in cursor.description], doctor))
        else:
            return None
    except Exception as e:
        print(f"Error getting doctor by ID: {e}")
        return None
    finally:
        conn.close()

def get_service_name(service_id):
    """Извлекает название услуги из таблицы “services” по её ID и возвращает его в виде строки."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM services WHERE id = ?", (service_id,))
        service_name = cursor.fetchone()
        if service_name:
            return service_name[0]
        else:
            return None
    except Exception as e:
        print(f"Error getting service name: {e}")
        return None
    finally:
        conn.close()