import requests
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

def generate_number_formats(end):
    formats = set()
    for i in range(1, end + 1):
        formats.add(str(i)) 
        formats.add(str(i).zfill(2)) 
        formats.add(str(i).zfill(3))
        formats.add(str(i).zfill(4)) 
    return sorted(formats, key=lambda x: int(x))  

def check_internet_connection(proxy, base_url, output_file, timeout=5, start=1, end=99999, general_search=False):
    working_links = set()  
    failed_links = []

    try:
        with open(output_file, 'a') as f:  
            try:
                with open(output_file, 'r') as existing_file:
                    existing_links = {line.strip() for line in existing_file}
            except FileNotFoundError:
                existing_links = set()

            if general_search:
                number_formats = generate_number_formats(end)
            else:
                number_formats = [str(i).zfill(len(str(end))) for i in range(start, end + 1)]

            for formatted_number in tqdm(number_formats, desc="Проверка зеркал", unit="зеркало"):
                url = base_url.format(number=formatted_number)

                try:
                    response = requests.get(url, proxies=proxy, timeout=timeout)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        if soup.find: #Тут после find в скобках можно написать какой элемент на сайте мы ищем для проверки
                            if url not in existing_links and url not in working_links:
                                working_links.add(url)  
                                tqdm.write(f"\rРабочее зеркало: {url}")
                                f.write(url + '\n')  
                        else:
                            failed_links.append(url)
                    else:
                        failed_links.append(url)
                except requests.exceptions.RequestException:
                    failed_links.append(url)

    except KeyboardInterrupt:
        pass

    return list(working_links), failed_links  

def main():
    proxies = [
        {"http": "proxy:proxy"},
        {"http": "proxy:proxy"}
    ]

    os.system('cls' if os.name == 'nt' else 'clear')  
    print("Выберите режим поиска:")
    
    print("1. Глобальный поиск")
    print("2. Поиск по интервалу чисел")
    
    choice = input()

    if choice == '2':
        os.system('cls' if os.name == 'nt' else 'clear')  
        print("Поиск по интервалу чисел")
        start = int(input("Диапазон от: "))
        end = int(input("До: "))
        digits = int(input("Введите количество цифр в номере (например, '2' для 01 или '3' для 010): "))
        general_search = False
    elif choice == '1':
        os.system('cls' if os.name == 'nt' else 'clear')  
        print("Глобальный поиск")
        end = 999
        general_search = True
    else:
        print("Неверный выбор режима.")
        return

    base_url = "https://www.mylink{number}.com"
    output_file = 'mirror.txt'

    working_proxy = None
    for proxy in proxies:
        try:
            response = requests.get("https://www.google.com", proxies=proxy, timeout=10)
            if response.status_code == 200:
                os.system('cls' if os.name == 'nt' else 'clear') 
                working_proxy = proxy
                print(f"Рабочий прокси найден: {proxy}")
                break
        except requests.exceptions.RequestException:
            continue  

    if working_proxy:
        if general_search:
            working_links, failed_links = check_internet_connection(working_proxy, base_url, output_file, end=end, general_search=True)
        else:
            working_links, failed_links = check_internet_connection(working_proxy, base_url, output_file, start=start, end=end, general_search=False)
        
        os.system('cls' if os.name == 'nt' else 'clear')  
        print(f"Используемый прокси: {working_proxy}")
        if working_links:
            print("Новые зеркала:")
            for link in working_links:
                print(link)
        else:
            print(f"Новых зеркал не обнаружено =(")
    else:
        print("Не найдено ни одного рабочего прокси =(")

if __name__ == "__main__":
    main()
