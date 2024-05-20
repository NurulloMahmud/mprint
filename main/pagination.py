from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response



class CustomPagination(PageNumberPagination):
    page_size_query_param = 'size'
    max_page_size = 100  # You can adjust this as needed

    def get_paginated_response(self, data):
        return Response({
            'totalItems': self.page.paginator.count,
            'itemsPerPage': self.page.paginator.per_page,
            'currentPage': self.page.number,
            'totalPages': self.page.paginator.num_pages,
            'data': data
        })

