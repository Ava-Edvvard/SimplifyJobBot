import requests


# Объект для работы с базой директус (docs.directus.io) на домене simplify-bots
class SimplifyDB:
    # Объявление http сессии
    session = requests.session()
    # Ссылка на api simplify-bots с расположением директус
    hostname = 'https://api.simplify-bots.com'
    # Рабочая среда (коллекция) на simplify-bots
    collection = 'routes_level_up_bot'
    # Словарь с ссылками на основные задействованные разделы базы директус
    api_urls = {
        'items': f'{hostname}/items/{collection}',
        'assets': f'{hostname}/assets'
    }

    def __init__(self, access_token):
        """

        :param access_token: токен для доступа к базе `директус`
        """
        self.access_token = access_token

    def get_items(self, *sort, **filters):
        """

        :param sort: принимает параметры (*args) для сортировки выборки docs.directus.io/reference/query.html#sort
        :param filters: принимает параметры с ключами (**kwargs) для фильтрации
        при выборке docs.directus.io/reference/query.html#filter
        :rtype: dict
        """
        # Ссылка по умолчанию для запроса к базе директус
        # параметры: limit:-1 (не ограничивать выборку); filter[status]:true (только айтемы которые выводятся)
        items_uri = f'{self.api_urls["items"]}?access_token={self.access_token}&limit=-1&filter[status]=true'
        if sort:
            # Если есть параметры по которым необходимо отсортировать выборку, то они добавляются в запрос
            items_uri += f'&sort={",".join(sort)}'
        if filters:
            # Если есть параметры по которым необходимо отфильтровать выборку, то они добавляются в запрос
            for key, value in filters.items():
                items_uri += f'&filter[{key}]={value}'
        return self.session.get(items_uri).json()['data']

    def get_file_content(self, file_id):
        """
        Метод для скачивания файл из базы директус docs.directus.io/reference/files.html

        :param file_id: параметр принимает идентификатор на asset из базы директус
        :return: binary
        """
        return self.session.get(f'{self.api_urls["assets"]}/{file_id}').content

    def get_file_link(self, file_id):
        """
        Метод для составления ссылки на файл из базы директус

        :param file_id: Идентификатор файла из базы директус
        :return: str
        """
        return f'{self.api_urls["assets"]}/{file_id}'

    def get_item_by_id(self, item_id):
        """
        Метод для получения айтема из базы директус docs.directus.io/reference/items.html

        :param item_id: Идентфкатор айтема данные о котором нужно получить
        :return: list[dict]
        """
        return self.session.get(f'{self.api_urls["items"]}/{item_id}?access_token={self.access_token}').json()['data']


if __name__ == '__main__':
    db = SimplifyDB('UokPEWhb7Gjf2hrqjRv_FlHOzWPSViPG')
    print(db.get_items('row', 'column', last_block=5))