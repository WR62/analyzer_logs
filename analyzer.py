import re
import tkinter as tk
from tkinter import filedialog as fd
import os
from pathlib import Path
import json

if __name__ == '__main__':
    # Выбор директории с логами
    root = tk.Tk()
    root.withdraw()
    folder_selected = fd.askdirectory(master=root, mustexist=True)
    root.destroy()
    # при отмене выбора используем текущую директорию
    if len(folder_selected) == 0:
        folder_selected = os.getcwd()
    # получаем список лог-файлов
    files = Path(folder_selected).glob('*.log')
    files = list(map(str, files))
    # Обрабатываем каждый файл и присваиваем ему уникальное имя
    for file in files:
        name_file = 'result_' + Path(file).stem + '.json'
        with open(file, 'r') as fl:
            total_requests = 0                  # Общее количество запросов
            counter_types_requests = dict()     # Словарь счетчиков по типам запросов
            counter_ip_requests = dict()        # Словарь счетчиков по ip-адресам
            # Словари с информацией по трем самым длинным запросам
            first_longest = {'duration': 0}
            second_longest = {'duration': 0}
            third_longest = {'duration': 0}
            for line in fl:
                total_requests += 1
                # Обработка типов запросов
                type_request = re.search('[A-Z]+\\b', line).group(0)
                if type_request not in counter_types_requests:
                    counter_types_requests.setdefault(type_request, 0)
                counter_types_requests[type_request] += 1
                ip_addr = re.search('\\d{1,3}.\\d{1,3}.\\d{1,3}.\\d{1,3}', line).group(0)
                # Обработка ip-адресов
                counter_ip_requests.setdefault(ip_addr, 0)
                counter_ip_requests[ip_addr] += 1
                duration = int(line.split(' ')[-1])
                date_ = re.search(r'\[.+\]', line).group()
                # Шаблон для поиска url
                pattern = r'https?://(www.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9(' \
                          r')!@:%_+.~#?&/=]*)'
                url = re.search(pattern, line)
                if url is not None:
                    url = url.group()
                    if duration >= first_longest['duration']:
                        third_longest = second_longest.copy()
                        second_longest = first_longest.copy()
                        first_longest['ip'] = ip_addr
                        first_longest['date'] = date_
                        first_longest['method'] = type_request
                        first_longest['url'] = url
                        first_longest['duration'] = duration
                    elif duration >= second_longest['duration']:
                        third_longest = second_longest.copy()
                        second_longest['ip'] = ip_addr
                        second_longest['date'] = date_
                        second_longest['method'] = type_request
                        second_longest['url'] = url
                        second_longest['duration'] = duration
                    elif duration >= third_longest['duration']:
                        third_longest['ip'] = ip_addr
                        third_longest['date'] = date_
                        third_longest['method'] = type_request
                        third_longest['url'] = url
                        third_longest['duration'] = duration

                if total_requests % 100000 == 0:            # Информация, что скрипт не завис
                    print(f'{total_requests} records processed')
    # Сортировка словаря с количеством запросов по ip для поиска трех максимальных
    sorted_counter_ip = sorted(counter_ip_requests.items(), key=lambda item: item[1], reverse=True)
    sorted_counter_ip = sorted_counter_ip[:3]

    final_result = dict()
    final_result['top_ips'] = dict(sorted_counter_ip)
    final_result['top_longest'] = [first_longest, second_longest, third_longest]
    final_result['total_stat'] = counter_types_requests
    final_result['total_requests'] = total_requests
    final_json = json.dumps(final_result, indent=4)
    with open(name_file, 'w') as outfile:
        outfile.write(final_json)
    print(final_json)
