from requests import get
from typing import Dict
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from pathlib import Path
from lxml import html
from concurrent.futures import ThreadPoolExecutor
import timeit


def url_list(urls) -> Dict[int, str]:
    keys = range(len(urls))
    return dict(zip(keys, urls))


def get_data(urls) -> Dict[int, str]:
    response_list = {}
    for key, url in urls.items():
        try:
            with closing(get(url, stream=True)) as response:
                if validated_response(response):
                    response_list[key] = response.content
                else:
                    return None
        except RequestException as e:
            return None
    return response_list

def get_data2(url):
    
    with closing(get(url, stream=True)) as response:
        if validated_response(response):
            return response.content
        else:
            return None

def fetch(urls):
    with ThreadPoolExecutor(max_workers = 2) as executor:
        res = executor.map(get_data2, urls)
    return list(res)

def validated_response(response) -> bool:
    if("text/html" in response.headers["content-type"]):
        return True
    else:
        return False


def parse_response(url_data, file_name, element, class_name) -> None:
    soup = BeautifulSoup(url_data, 'lxml')
    Path('results/' + file_name + '.txt').touch()
    with open('results/' + file_name + '.txt', 'w') as writer:
        for div in soup.find_all(element, class_=class_name):
            writer.write(div.get_text()+'\n')


def create_directory() -> None:
    try:
        Path("results").mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        print("A directory with this name already exists!")


def main():
    urls = ['https://www.elgiganten.se/cms/sommarrea/sommarrea/',
                     'https://www.elgiganten.se/cms/sommarrea/sommarrea/']
    start = timeit.default_timer()
    response_list = fetch(urls)
    create_directory()

    parse_response(response_list[0],"elgiganten_cheap","span","table-cell")
    parse_response(response_list[1],"elgiganten_price","div","product-price")



    stop = timeit.default_timer()
    print('Time: ', stop - start)


if __name__ == "__main__":
    main()
