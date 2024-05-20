from rest_framework.pagination import PageNumberPagination



class CustomPagination(PageNumberPagination):
    page_size_query_param = 'size'
    max_page_size = 100  # You can adjust this as needed


