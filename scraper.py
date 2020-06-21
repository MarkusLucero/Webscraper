from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def get_data(url):
    """ Closing will exit the clode block regardless when leaving the code block """

    try:
        with closing(get(url, stream=True)) as response:
            if validated_response(response):
                print(response.content)
                return response.content
            else:
                return None
    except RequestException as e:
        return None


def validated_response(response):

    if("text/html" in response.headers["content-type"]):
        return True
    else:
        return False


def main():
    url_data = get_data('https://www.biltema.se/')
    print(url_data)


if __name__ == "__main__":
    main()
