from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination for all endpoints.

    - Default: 20 items per page
    - Max: 100 items per page
    - Client can control via ?page_size=X
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Custom response format with metadata.

        Returns:
            Response: paginated response including
            - count
            - next / previous links
            - total pages
            - current page
            - results
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })


class LargeResultsSetPagination(PageNumberPagination):
    """
    Pagination for large datasets (e.g., measurements, logs).

    - Default: 50 items per page
    - Max page size: 200
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class SmallResultsSetPagination(PageNumberPagination):
    """
    Pagination for small datasets or detailed views.

    - Default: 10 items per page
    - Max page size: 50
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50