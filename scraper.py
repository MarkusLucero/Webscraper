from requests import get
from typing import Dict, List
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from pathlib import Path
from lxml import html
from concurrent.futures import ThreadPoolExecutor
import timeit


def get_data(url):
    
    with closing(get(url, stream=True)) as response:
        if validated_response(response):
            return response.content
        else:
            return None

def fetch_html(urls) -> List[str]:
    with ThreadPoolExecutor(max_workers = 2) as executor:
        res = executor.map(get_data, urls)
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
    response_list = fetch_html(urls)
    create_directory()

    parse_response(response_list[0],"elgiganten_cheap","span","table-cell")
    parse_response(response_list[1],"elgiganten_price","div","product-price")


    stop = timeit.default_timer()
    print('Time: ', stop - start)


if __name__ == "__main__":
    main()
