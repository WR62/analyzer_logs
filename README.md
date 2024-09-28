# log_analyzer

<h3>Важно! Поскольку (пока) нет возможности работать в линукс, 
скрипт написан под Windows!</h3>

1. Выбор директории, где находятся лог-файлы. Если директория не выбрана, используется текущая.
2. Получение списка лог-файлов в данной директории
3. Построчно считывая файл, считаем общее количество запросов, количество запросов по каждому типу запроса, количество запросов по каждому ip-адресу.

Создаются три словаря для самых длинных запросов. Если текущий запрос попадает в тройку самых длинных - перезаписываем словари.

Информация из строки извлекается с помощью регулярных выражений

Каждые 100000  записей в терминал выдается сообщение о количестве записей для индикации продолжающейся работы скрипта.

После окончания чтения файла:
1. Сортируется словарь с количеством запросов по ip-адресам для получения трех максимальных
2. Создается словарь с требуемыми данными, который в формате json выдается в терминал и записывается в файл.