import re
import os


PATH_TO_FOLDER = "C:/Users/Piskunova/Desktop/OCR-errors" # указываем путь к папке с файлами


def parse_folder(PATH_TO_FOLDER): # используя путь к папке, находим путь к файлам
    for path, dirs, filenames in os.walk(PATH_TO_FOLDER):
        for filename in filenames:
            if '.txt' in filename:
                path_to_file = os.path.join(path, filename)
                return path_to_file


def parse_file(): # открываем файлы
    path_to_file = parse_folder(PATH_TO_FOLDER)
    with open(path_to_file, 'r', encoding='utf-8') as openfile:
        text = openfile.read()
        return text


def parse_text(): # парсим файлы
    text = parse_file()
    abonents = re.findall(r"[А-ЯЁ][а-яё\s]+[\t\s\n][А-ЯЁ]+.*?(?:-{1,2}[\s\d:'ОЗбИЮ]{1,3})+", text, flags=re.DOTALL)
    abonents = [re.sub(r"[\t\s\n]+", " ", abonent) for abonent in abonents] # делаем так, чтобы одна строчка == один абонент
    parsed_abonents = []
    for abonent in abonents:
        surnames_names_patronyms = re.findall(r"^([А-ЯЁ\s][а-яё\s]+)\s?([А-ЯЁ\d\w])\s?([А-ЯЁ\d\w])", abonent) # ищем ФИО
        for surname_name_patronym in surnames_names_patronyms:
            surname = surname_name_patronym[0] # отделяем фамилию
            name = surname_name_patronym[1] # имя
            patronym = surname_name_patronym[2] # и отчество

        wrong_phone_numbers = re.findall(r"[А-ЯЁ]{1,2}\s?\d?-.*", abonent) # ищем телефонные номера
        for wrong_phone_number in wrong_phone_numbers:
            phone_number = re.sub(r"O|О", r"0", wrong_phone_number) # исправляем возможные ошибки при распознавании телефонных номеров
            phone_number = re.sub(r"З", r"3", phone_number) # исправляем
            phone_number = re.sub(r"б", r"6", phone_number) # продолжаем исправлять
            phone_number = re.sub(r"[:'^\.,\s]", r"", phone_number) # все еще исправляем
            phone_number = re.sub(r"--", r"-", phone_number) # почти закончили, но еще исправляем

        addresses = re.findall(r"(?<=\s)([А-ЯЁ\w\d]\s?[А-ЯЁ\w\d]\s)([А-ЯЁа-яё\d\w]+.*)(?=\s[А-ЯЁ]+\d?-)", abonent) # ищем адреса
        for address in addresses:
            address = address[1]

        abonents_dict = {"Surname": surname, "Name": name, "Patronym": patronym, "Phone Number": phone_number, "Address": address} # складываем все в словари
        parsed_abonents.append(abonents_dict) # словари складываем в список
    return parsed_abonents # получаем список словарей, где один словарь == один абонент


def write_file(): # создаем новые файлы
    path_to_file = parse_folder(PATH_TO_FOLDER)
    with open(path_to_file, 'r', encoding='utf-8') as openfile:
        path_to_new_file = re.sub('.txt', '_with_parsed_abonents.txt', path_to_file) # называем новые файлы
    with open(path_to_new_file, 'w', encoding='utf-8') as writefile: # записываем в новые файлы словари, т.е. абонентов
        parsed_abonents = parse_text() # получаем список словарей, т.е. абонентов
        for abonent in parsed_abonents: # проходимся по каждому словарю, т.е. абоненту, и записываем их ФИО, телефонный номер и адрес (см. ниже)
            abonent = ("{} {} {}, {}, {}\n".format(abonent["Surname"], abonent["Name"], abonent["Patronym"], abonent["Address"], abonent["Phone Number"]))
            writefile.write(abonent)


def main():
    write_file() # создаем функцию, которая вызовет другую функцию, которая вызовет все остальные и в конечном итоге сделает файл с абонентами


if __name__ == "__main__":
    main() # вызываем эту функцию (см. выше)
# вуа-ля! получаем файл с абонентами
