import json
from typing import Dict, List, Union, Optional


class ProductManager:
    def __init__(self, config_file: str = 'cfg.json'):
        """
        Инициализация менеджера продуктов с загрузкой конфигурационного файла.

        :param config_file: Путь к JSON-файлу конфигурации
        """
        self.config_file = config_file
        self.config = self._load_config()
        self.products = self.config.get('products', [])

    def _load_config(self) -> Dict:
        """
        Загрузка конфигурационного файла.

        :return: Словарь с конфигурацией
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file {self.config_file} not found")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in config file {self.config_file}")

    def _get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """
        Получение продукта по ID (индексу в списке).

        :param product_id: ID продукта (индекс)
        :return: Словарь с информацией о продукте или None, если не найден
        """
        try:
            return self.products[product_id]
        except IndexError:
            return None

    def _get_product_by_name(self, product_name: str) -> Optional[Dict]:
        """
        Получение продукта по имени.

        :param product_name: Название продукта
        :return: Словарь с информацией о продукте или None, если не найден
        """
        for product in self.products:
            if product['name'].lower() == product_name.lower():
                return product
        return None

    def _format_product_info(self, product: Dict, fields: List[str] = None) -> str:
        """
        Форматирование информации о продукте в красивый текст.

        :param product: Словарь с информацией о продукте
        :param fields: Список полей для вывода (если None - выводим все)
        :return: Отформатированная строка с информацией
        """
        if not product:
            return "Продукт не найден"

        if fields is None:
            fields = product.keys()

        info = []
        for field in fields:
            if field in product:
                value = product[field]
                if isinstance(value, list):
                    value = " x ".join(map(str, value))
                info.append(f"{field.replace('_', ' ').title()}: {value}")

        return "\n".join(info)

    def get_product_info_by_id(self, product_id: int, fields: List[str] = None) -> str:
        """
        Получение информации о продукте по ID.

        :param product_id: ID продукта
        :param fields: Список полей для вывода (если None - выводим все)
        :return: Отформатированная строка с информацией
        """
        product = self._get_product_by_id(product_id)
        if product is None:
            return f"Продукт с ID {product_id} не найден"

        return self._format_product_info(product, fields)

    def get_product_info_by_name(self, product_name: str, fields: List[str] = None) -> str:
        """
        Получение информации о продукте по имени.

        :param product_name: Название продукта
        :param fields: Список полей для вывода (если None - выводим все)
        :return: Отформатированная строка с информацией
        """
        product = self._get_product_by_name(product_name)
        if product is None:
            return f"Продукт с именем '{product_name}' не найден"

        return self._format_product_info(product, fields)

    def get_all_products(self) -> List[Dict]:
        """
        Получение списка всех продуктов.

        :return: Список всех продуктов
        """
        return self.products


# Пример использования
if __name__ == "__main__":
    try:
        manager = ProductManager('cfg.json')

        # Поиск по ID
        print("=== Поиск по ID ===")
        print(manager.get_product_info_by_id(0))  # Все поля
        print("\n" + manager.get_product_info_by_id(0, ['name', 'size', 'prise_yes_markup']))  # Конкретные поля
        print("\n" + manager.get_product_info_by_id(999))  # Несуществующий ID

        # Поиск по имени
        print("\n=== Поиск по имени ===")
        print(manager.get_product_info_by_name("Brelock"))  # Все поля
        print("\n" + manager.get_product_info_by_name("Figurka", ['id', 'size', 'time_to_print']))  # Конкретные поля
        print("\n" + manager.get_product_info_by_name("Unknown"))  # Несуществующее имя

    except Exception as e:
        print(f"Ошибка: {e}")