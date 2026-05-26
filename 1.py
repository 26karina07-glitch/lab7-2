import sys
from dataclasses import dataclass
from enum import Enum

# --- КРОК 1: Опис переліку (Enum) та сутностей автопарку ---

class FuelType(Enum):
    DIESEL = "Дизель"
    GASOLINE = "Бензин"
    ELECTRIC = "Електро"


@dataclass
class Vehicle:
    v_id: str
    brand: str
    model: str
    fuel_type: FuelType
    max_payload: float  # Максимальна вантажопідйомність в кг

    def calculate_delivery_cost(self, distance: float) -> float:
        """Поліморфний метод для розрахунку вартості доставки"""
        # Базовий тариф: 10 грн за км
        return distance * 10.0


class Truck(Vehicle):
    def calculate_delivery_cost(self, distance: float) -> float:
        # Для вантажівок додатковий коефіцієнт 1.5 та податок на вагу
        return (distance * 15.0) + (self.max_payload * 0.02)


class Van(Vehicle):
    def calculate_delivery_cost(self, distance: float) -> float:
        # Для фургонів тариф трохи нижчий, коефіцієнт 1.2
        return distance * 12.0

# --- КРОК 2: Менеджер системи (Композиція) з методами збереження ---

class FleetManager:
    def __init__(self):
        # Список для зберігання транспортних засобів
        self._vehicles = []

    def load_config(self):
        """Імітація зчитування конфігурації"""
        pass

    def load_system_state(self):
        """Імітація завантаження стану з бінарного файлу (pickle)"""
        pass

    def save_system_state(self):
        """Імітація збереження стану системи"""
        print("[System] Стан автопарку успішно збережено в бінарний файл (pickle).")

    def export_sales_report(self):
        """Імітація експорту фінансового звіту в CSV"""
        print("[System] Фінансовий звіт по доставках успішно експортовано в CSV.")

    def add_vehicle(self, vehicle: Vehicle):
        """Додавання нового транспорту до системи"""
        self._vehicles.append(vehicle)
        print(f"[Success] ТЗ {vehicle.brand} {vehicle.model} (ID: {vehicle.v_id}) додано до автопарку!")

    def display_all_vehicles(self):
        """Виведення всіх транспортних засобів"""
        if not self._vehicles:
            print("[Info] Автопарк наразі порожній.")
            return

        print("\n--- СПИСОК ТРАНСПОРТНИХ ЗАСОБІВ АВТОПАРКУ ---")
        for v in self._vehicles:
            v_type = "Вантажівка" if isinstance(v, Truck) else "Фургон"
            print(f"[{v_type}] ID: {v.v_id} | {v.brand} {v.model} | Паливо: {v.fuel_type.value} | "
                  f"Макс. вантаж: {v.max_payload} кг")
            # Демонстрація поліморфізму (тестова дистанція 100 км)
            print(f"    -> Тестова вартість доставки на 100 км: {v.calculate_delivery_cost(100):.2f} грн")


# --- КРОК 3: Реалізація інтерактивного CLI-меню ---

def show_menu():
    print("\n" + "="*40)
    print("      СИСТЕМА УПРАВЛІННЯ АВТОПАРКОМ")
    print("="*40)
    print("1. Показати всі транспортні засоби")
    print("2. Додати нову Вантажівку (Truck)")
    print("3. Додати новий Фургон (Van)")
    print("4. Розрахувати вартість доставки для ТЗ")
    print("5. Зберегти стан системи (Pickle)")
    print("6. Експортувати звіт у формат CSV")
    print("0. Безпечний вихід із програми")
    print("="*40)


if __name__ == "__main__":
    manager = FleetManager()
    
    # Ініціалізація системи перед запуском циклу
    manager.load_config()
    manager.load_system_state()
    
    print("Ласкаво просимо до Global Logistics UA ")
    
    # Головний життєвий цикл програми
    while True:
        show_menu()
        try:
            choice = input("Оберіть потрібну дію: ").strip()
            
            match choice:
                case "1":
                    manager.display_all_vehicles()
                    
                case "2" | "3":
                    # Спільне введення даних для Truck та Van
                    v_type_str = "Вантажівки" if choice == "2" else "Фургона"
                    print(f"\n--- Введення даних для нового {v_type_str} ---")
                    
                    v_id = input("Введіть унікальний ID (напр. АА1234): ").strip()
                    if not v_id:
                        raise ValueError("ID транспортного засобу не може бути порожнім!")
                        
                    brand = input("Введіть марку (brand): ").strip()
                    model = input("Введіть модель (model): ").strip()
                    if not brand or not model:
                        raise ValueError("Марка та модель мають бути заповнені!")
                    
                    print("Оберіть тип палива: 1. Дизель | 2. Бензин | 3. Електро")
                    fuel_choice = input("Ваш вибір (1-3): ").strip()
                    match fuel_choice:
                        case "1": fuel = FuelType.DIESEL
                        case "2": fuel = FuelType.GASOLINE
                        case "3": fuel = FuelType.ELECTRIC
                        case _: raise ValueError("Некоректний вибір типу палива!")
                    
                    # Небезпечна ділянка валідації числових даних
                    try:
                        max_payload = float(input("Введіть макс. вантажопідйомність (кг): "))
                    except ValueError:
                        raise ValueError("Вантажопідйомність повинна бути числовим значенням!")
                        
                    if max_payload <= 0:
                        raise ValueError("Вантажопідйомність повинна бути строго більшою за 0!")
                    
                    # Валідація вантажопідйомності відповідно до специфікації варіанта
                    if choice == "2" and max_payload < 3500:
                        raise ValueError("Вантажівка (Truck) не може мати вантажопідйомність менше 3500 кг!")
                    if choice == "3" and max_payload >= 3500:
                        raise ValueError("Фургон (Van) повинен мати вантажопідйомність менше 3500 кг!")

                    # Створення відповідного об'єкта залежно від обраного пункту
                    if choice == "2":
                        new_vehicle = Truck(v_id, brand, model, fuel, max_payload)
                    else:
                        new_vehicle = Van(v_id, brand, model, fuel, max_payload)
                        
                    manager.add_vehicle(new_vehicle)
                    
                case "4":
                    print("\n--- Розрахунок доставки під конкретну вагу ---")
                    v_id_search = input("Введіть ID потрібного ТЗ: ").strip()
                    
                    # Пошук об'єкта в списку менеджера
                    selected_v = next((v for v in manager._vehicles if v.v_id == v_id_search), None)
                    if not selected_v:
                        print("[Warning] Транспортний засіб з таким ID не знайдено.")
                        continue
                        
                    try:
                        cargo_weight = float(input(f"Введіть вагу вантажу для перевезення (макс {selected_v.max_payload} кг): "))
                        distance = float(input("Введіть відстань доставки (км): "))
                    except ValueError:
                        raise ValueError("Вага та відстань мають бути дробовими чи цілими числами!")
                        
                    # Критична бізнес-валідація варіанта: не можна завантажити більше максимуму
                    if cargo_weight > selected_v.max_payload:
                        raise ValueError(f"Помилка валідації вантажу! Перевищено максимум на {cargo_weight - selected_v.max_payload} кг!")
                    if distance <= 0 or cargo_weight <= 0:
                        raise ValueError("Відстань та вага вантажу повинні бути більшими за нуль!")
                        
                    cost = selected_v.calculate_delivery_cost(distance)
                    print(f"[Success] Розрахунок завершено. Вартість доставки на {distance} км складе: {cost:.2f} грн.")
                    
                case "5":
                    manager.save_system_state()
                    
                case "6":
                    manager.export_sales_report()
                    
                case "0":
                    print("\nЗавершення роботи. Виконується автозбереження стану системи...")
                    manager.save_system_state()
                    print("Дякуємо, що користувалися нашою системою! Бувай! 🚛💨")
                    sys.exit(0)
                    
                case _:
                    print("[Warning] Невідома команда! Будь ласка, оберіть пункт меню від 0 до 6.")
                    
        except ValueError as e:
            # Перехоплення помилок невірного введення типів та бізнес-логіки
            print(f"\n[Помилка введення даних]: {e}")
            print("Система автоматично повертає вас до головного меню. Спробуйте ще раз.")
        except Exception as e:
            # Захист від глобальних непередбачуваних помилок (Fault Tolerance)
            print(f"\n[Критична помилка інтерфейсу]: {e}")
            print("Роботу стабілізовано. Повернення до головного меню.")