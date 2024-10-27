#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Server Pagination Module

This module provides a `Server` class that enables pagination of a dataset
loaded from a CSV file. The dataset used in this example contains popular baby
names, but the functionality is generic and can be applied to other similar
datasets.

Classes:
    Server: A class that manages loading, caching, and paginating data from the
    'Popular_Baby_Names.csv' file.

Functions:
    index_range(page: int, page_size: int) -> Tuple[int, int]:
        Helper function that calculates the start and end indexes for
        pagination based on the specified page and page size.

Features:
    - Load and cache dataset from a CSV file on demand.
    - Retrieve data for a specific page using the `get_page` method.
    - Provide detailed pagination information using `get_hyper`, including:
        - `page_size`: The length of the data returned for the current page.
        - `page`: The current page number.
        - `data`: List of rows representing the current page's data.
        - `next_page`: The next page number, or `None` if there's no next page.
        - `prev_page`: The previous page number, or `None` if there's no
                        previous page.
        - `total_pages`: Total number of pages based on the dataset size and
                        page size.

Example Usage:
    server = Server()
    # Get simple paginated data
    print(server.get_page(page=1, page_size=10))

    # Get detailed pagination information with `get_hyper`
    print(server.get_hyper(page=1, page_size=10))
"""

import csv
import math
from typing import List, Any, Dict, Optional

index_range = __import__('0-simple_helper_function').index_range


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initializes the Server with a private dataset attribute to store the
        loaded data."""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Loads and caches the dataset from the CSV file if not already loaded.

        Returns:
            List[List]: A list of rows from the CSV file, excluding the header.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip the header

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieves a specific page of data from the dataset based on pagination
        parameters.

        Args:
            page (int): The page number to retrieve, starting from 1. Defaults
                        to 1.
            page_size (int): The number of items per page. Defaults to 10.

        Returns:
            List[List]: A list of rows for the specified page. Returns an
                        empty list if the page or page size are out of range.

        Raises:
            AssertionError: If `page` or `page_size` are not positive integers.
        """
        # Validate inputs
        assert isinstance(
            page, int) and page > 0, "Page must be a positive integer."
        assert isinstance(page_size, int) and page_size > 0, (
            "Page size must be a positive integer.")

        # Ensure the dataset is loaded
        dataset = self.dataset()

        # Calculate start and end indexes for the requested page
        start_index, end_index = index_range(page, page_size)

        # Return an empty list if the indexes are out of range
        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Retrieves a dictionary with pagination information for a specific page
        of data.

        Args:
            page (int): The page number to retrieve, starting from 1.
                        Defaults to 1.
            page_size (int): The number of items per page. Defaults to 10.

        Returns:
            Dict[str, Any]: A dictionary containing pagination information,
                            including the current page data, page size, and
                            navigation details.
        """
        # Ensure the dataset is loaded
        dataset = self.dataset()
        total_items = len(dataset)
        total_pages = math.ceil(total_items / page_size)

        # Fetch the data for the requested page
        data = self.get_page(page, page_size)

        # Calculate next and previous page numbers
        next_page: Optional[int] = page + 1 if page < total_pages else None
        prev_page: Optional[int] = page - 1 if page > 1 else None

        # Prepare the response dictionary
        return {
            "page_size": len(data),          # Actual size of the returned data
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages
        }


if __name__ == "__main__":
    server = Server()

    # Testing the get_hyper method
    print(server.get_hyper(1, 2))
    print("---")
    print(server.get_hyper(2, 2))
    print("---")
    print(server.get_hyper(100, 3))
    print("---")
    print(server.get_hyper(3000, 100))
