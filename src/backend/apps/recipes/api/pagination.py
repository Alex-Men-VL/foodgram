from rest_framework import pagination


class PageNumberLimitPagination(pagination.PageNumberPagination):
    """Пагинатор, который обрабатывает параметр номера страницы и количества объектов на странице"""

    page_size_query_param = 'limit'
