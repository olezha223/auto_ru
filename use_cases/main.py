from use_cases.count import run_count_parsing
from use_cases.link import run_links_parser
from use_cases.equipment import Processing
import pandas as pd
import re


def main():
    run_count_parsing(count_processes=5, count_models=5)
    run_links_parser(count=5)
    Processing(first=True, count_processes=5).run()


def extract_id(link: str):
    match = re.search(r"\d+-\w{7}", link)
    return match.group() if match else "can't get id"


if __name__ == "__main__":
    main()
    cars_path = '../data/cars/result.csv'
    counting_path = '../data/counting/result.csv'
    links_path = '../data/links/result.csv'
    output_path = '../data/cars.csv'
    cars = pd.read_csv(cars_path)
    cars.fillna(0, inplace=True)
    counting = pd.read_csv(counting_path)

    def extract_id(link: str):
        match = re.search(r"\d+-\w{7}", link)
        return match.group() if match else "can't get id"

    links = pd.read_csv(links_path)
    df = links.merge(counting)
    id_column = []
    for url in list(df['Ссылка на объявление']):
        id_column.append(extract_id(url))
    df['id'] = id_column

    df.drop_duplicates(subset=['id'])
    cars.drop_duplicates(subset=['id'])
    df.merge(cars, on='id').to_csv(output_path, index=False)
