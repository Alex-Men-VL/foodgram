import typing

from bs4 import BeautifulSoup

from django.http import HttpRequest
from django.template import loader


def render_shopping_list(
    request: HttpRequest,
    ingredients: typing.List[typing.Dict[str, typing.Union[str | int]]],
) -> str:
    """Получение списка покупок в виде строки из HTML шаблона

    :param ingredients: Список ингредиентов
    """

    template = loader.get_template('shopping_list.html')
    context = {'ingredients': ingredients}

    rendered_page = template.render(context, request)
    soup = BeautifulSoup(rendered_page, 'html.parser')
    return soup.get_text()
