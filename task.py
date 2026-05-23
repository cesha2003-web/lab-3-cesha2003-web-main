import csv

LOW_RISE_MAX_FLOORS = 5
MID_RISE_MAX_FLOORS = 16

LOW_RISE = "Малоэтажный"
MID_RISE = "Среднеэтажный"
HIGH_RISE = "Многоэтажный"

DATA_FILE = "housing_data.csv"


def read_file(filename: str) -> list[dict]:
    """Читает данные из CSV файла и преобразует их в список словарей.

    :param filename: Название файла, содержащего данные.
    :return: Список словарей с данными о домах.
    """
    with open(filename, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        houses = []
        for row in reader:
            row["floor_count"] = int(row["floor_count"])
            row["population"] = int(row["population"])
            row["heating_value"] = float(row["heating_value"])
            row["area_residential"] = float(row["area_residential"])
            houses.append(row)
    return houses


def classify_house(floor_count: int) -> str:
    """Классифицирует дом на основе количества этажей.

    Проверяет, является ли количество этажей целым числом и положительным значением.
    Возвращает категорию дома в зависимости от количества этажей.

    :param floor_count: Количество этажей в доме.
    :return: Категория дома в виде строки:
    "Малоэтажный", "Среднеэтажный" или "Многоэтажный".
    """
    if not isinstance(floor_count, int) or isinstance(floor_count, bool):
        message = "Количество этажей должно быть целым числом."
        raise TypeError(message)
    if floor_count <= 0:
        message = "Количество этажей должно быть положительным числом."
        raise ValueError(message)

    if floor_count <= LOW_RISE_MAX_FLOORS:
        return LOW_RISE
    if floor_count <= MID_RISE_MAX_FLOORS:
        return MID_RISE
    return HIGH_RISE


def get_classify_houses(houses: list[dict]) -> list[str]:
    """Классифицирует дома на основе количества этажей.

    :param houses: Список словарей с данными о домах.
    :return: Список категорий домов.
    """
    return [classify_house(house["floor_count"]) for house in houses]


def get_count_house_categories(categories: list[str]) -> dict[str, int]:
    """Подсчитывает количество домов в каждой категории.

    :param categories: Список категорий домов.
    :return: Словарь с количеством домов в каждой категории.
    """
    counts: dict[str, int] = {}
    for category in categories:
        counts[category] = counts.get(category, 0) + 1
    return counts


def min_area_residential(houses: list[dict]) -> str:
    """Находит адрес дома с минимальным средним количеством жилой площади на человека.

    Функция рассчитывает среднее количество квадратных метров жилой площади,
    приходящееся на каждого зарегистрированного жильца в доме.
    Среди всех домов функция возвращает адрес того дома, где эта величина минимальна.
    Такой подход позволяет выявлять дома с высокой плотностью заселения.

    :param houses: Список словарей с данными о домах.
    :return: Адрес дома с наименьшим средним количеством
    квадратных метров жилой площади на одного жильца.
    """
    house = min(
        houses,
        key=lambda item: item["area_residential"] / item["population"],
    )
    return house["house_address"]


def main() -> None:
    """Запускает анализ данных о домах и выводит результаты."""
    houses = read_file(DATA_FILE)
    categories = get_classify_houses(houses)
    counts = get_count_house_categories(categories)

    print("Количество домов по категориям:")
    for category, count in counts.items():
        print(f"  {category}: {count}")

    address = min_area_residential(houses)
    print(
        "Дом с наименьшим средним количеством жилой площади на одного жильца: "
        f"{address}",
    )


if __name__ == "__main__":
    main()
