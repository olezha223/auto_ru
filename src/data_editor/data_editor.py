import json
import pandas as pd


class DataEditor:
    """
    Класс для обработки полученных данных
    """

    def __init__(self, output_file: str, count: int, **paths):
        """
        :param output_file: Путь до выходного датафрейма
        :param count: Количество процессов, используемых при парсинге
        :param paths: вписать сюда нужные пути до файлов
        """
        self.output_file = output_file
        self.count = count
        if len(paths.keys()) == 2:
            self.path_to_tech_data = paths['path_to_tech_data']
            self.path_to_pack_data = paths['path_to_pack_data']
        else:
            self.path_to_json = paths['path_to_json']

    def join_data_json(self):
        """
        Соединяет полученные json в один датафрейм, применяется для случая,
        если нужно соединить два параллельных процесса
        """
        tech_result_list = []
        package_result_list = []
        for i in range(self.count):
            with open(f'{self.path_to_tech_data}_{i}.json', encoding='utf-8') as f:
                data = json.load(f)
                tech_dict_list = data['data']
                tech_result_list += tech_dict_list
            with open(f'{self.path_to_pack_data}_{i}.json', encoding='utf-8') as f:
                data = json.load(f)
                pack_dict_list = data['data']
                package_result_list += pack_dict_list

        result = []
        if len(tech_result_list) != len(package_result_list):
            print("разные длины массивов, невозможно соединить")
            return
        for i in range(len(tech_result_list)):
            tech_result_list[i].update(package_result_list[i])
            result.append(tech_result_list[i])
        df = pd.DataFrame(result)
        df.fillna(0, inplace=True)
        df.to_csv(self.output_file)

    def join_data_csv(self):
        """
        Соединяет json и сохраняет все в датафрейм csv. Применяется, когда каждый процесс кидает в свой файл
        в пределах одной задачи.
        """
        files = [f'{self.path_to_json}_{i}.json' for i in range(self.count)]
        result = []
        for filename in files:
            with open(filename, encoding='utf-8') as f:
                data = json.load(f)
                for row in data['data']:
                    result.append(row)
        df = pd.DataFrame(result)
        df.to_csv(self.output_file, index=False)

