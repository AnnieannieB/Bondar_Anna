import csv
from collections import Counter


# функция для чтения данных из CSV файла и преобразования их в список словарей
def read_file(filename: str) -> list[dict]:
    """
    Читает данные из CSV файла и преобразует их в список словарей.

    :param filename: Название файла, содержащего данные.
    :return: Список словарей с данными о домах.
    """
    data = []
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["floor_count"] = int(row["floor_count"])
            row["population"] = int(row["population"])
            row["heating_value"] = float(row["heating_value"])
            row["area_residential"] = float(row["area_residential"])
            data.append(row)
    return data


# классифицирует дом на основе количества этажей
def classify_house(floor_count: int) -> str:
    """
    Классифицирует дом на основе количества этажей.

    Проверяет, является ли количество этажей целым числом и положительным значением.
    Возвращает категорию дома в зависимости от количества этажей.

    :param floor_count: Количество этажей в доме.
    :return: Категория дома в виде строки: "Малоэтажный", "Среднеэтажный" или "Многоэтажный".
    """
    if not isinstance(floor_count, int):
        te = "Количество этажей должно быть целым числом"
        raise TypeError(te)
    if floor_count <= 0:
        ve = "Количество этажей должно быть положительным числом"
        raise ValueError(ve)

    limit1 = 5
    limit2 = 16

    if floor_count <= limit1:
        return "Малоэтажный"
    elif floor_count <= limit2:
        return "Среднеэтажный"
    else:
        return "Многоэтажный"


# классифицирует дома на основе количества этажей и возвращает список категорий
def get_classify_houses(houses: list[dict]) -> list[str]:
    """
    Классифицирует дома на основе количества этажей.

    :param houses: Список словарей с данными о домах.
    :return: Список категорий домов.
    """
    classified_houses = []
    try:
        for house in houses:
            floor_count = house["floor_count"]
            category = classify_house(floor_count)
            classified_houses.append(category)
    except (ValueError, TypeError):
        classified_houses.append("Ошибка")
    return classified_houses


# функция для подсчета количества домов в каждой категории
def get_count_house_categories(categories: list[str]) -> dict[str, int]:
    """
    Подсчитывает количество домов в каждой категории.

    :param categories: Список категорий домов.
    :return: Словарь с количеством домов в каждой категории.
    """
    counter = Counter(categories)
    return dict(counter)


# функция для поиска дома с наименьшим средним количеством кв.м жилой площади на одного жильца
def min_area_residential(houses: list[dict]) -> str:
    """
    Находит адрес дома с наименьшим средним количеством квадратных метров жилой площади на одного жильца.

    :param houses: Список словарей с данными о домах.
    :return: Адрес дома с наименьшим средним количеством квадратных метров жилой площади на одного жильца.
    """
    avg_areas = [house["area_residential"] / house["population"] for house in houses]

    min_avg_area = min(avg_areas)
    min_area_index = avg_areas.index(min_avg_area)

    return houses[min_area_index]["house_address"]


if __name__ == "__main__":
    data = read_file("housing_data.csv")

    count_cat = get_count_house_categories(get_classify_houses(data))
    print(count_cat)

    min_address = min_area_residential(data)
    print(min_address)
