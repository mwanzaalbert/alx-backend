#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Server Pagination Module

This module provides a `Server` class to manage and paginate a dataset of
popular baby names
loaded from a CSV file. The class includes methods to cache the dataset and
retrieve a specific page of data based on pagination parameters.

Classes:
    Server: A class to handle data loading and pagination from the
    'Popular_Baby_Names.csv' file.

Functions:
    index_range(page: int, page_size: int) -> Tuple[int, int]:
        Calculates the start and end indexes for pagination based on the
        provided page and page size.

>>> server = Server()
>>> print(server.get_page(3000, 100))
[]
"""

import csv
import math
from typing import List

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


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

    server = Server()

    # Test cases for get_page method
    try:
        should_err = server.get_page(-10, 2)
    except AssertionError:
        print("AssertionError raised with negative values")

    try:
        should_err = server.get_page(0, 0)
    except AssertionError:
        print("AssertionError raised with 0")

    try:
        should_err = server.get_page(2, 'Bob')
    except AssertionError:
        print("AssertionError raised when page and/or page_size are not ints")

    print(server.get_page(1, 3))
    print(server.get_page(3, 2))
    print(server.get_page(3000, 100))
