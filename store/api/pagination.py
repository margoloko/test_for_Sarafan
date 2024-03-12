from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Класс кастомной пагинации, с возможностью устанавливать желаемый размер страницы."""

    page_size = 50
    page_size_query_param = "limit"
