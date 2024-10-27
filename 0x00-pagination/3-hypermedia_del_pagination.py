#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict, Any


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize the server with a private dataset and indexed dataset."""
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Load and cache dataset from CSV file, skipping the header."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip header

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by position, allowing deletion-resilience."""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {i: dataset[i]
                                      for i in range(len(dataset))}
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None,
                        page_size: int = 10) -> Dict[str, Any]:
        """
        Returns a dictionary with pagination information that is
        deletion-resilient.

        Args:
            index (int): Start index of the requested page.
            page_size (int): Number of items per page.

        Returns:
            Dict[str, Any]: Contains the following keys:
                - 'index': Start index of the current page.
                - 'next_index': Start index for the next page.
                - 'page_size': Number of items on the current page.
                - 'data': List of rows for the current page.

        Raises:
            AssertionError: If the index is out of range.
        """
        indexed_dataset = self.indexed_dataset()

        # Assert index within range
        assert isinstance(index, int) and 0 <= index < len(
            indexed_dataset), "Index out of range."

        # Retrieve data from the specified index up to the page_size,
        # adjusting for missing entries
        data, current_index = [], index
        while len(data) < page_size and current_index < len(indexed_dataset):
            item = indexed_dataset.get(current_index)
            if item:
                data.append(item)
            current_index += 1

        # Calculate the next index to start the following page
        next_index = current_index if current_index < len(
            indexed_dataset) else None

        # Return pagination data as a dictionary
        return {
            "index": index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data,
        }


if __name__ == "__main__":
    server = Server()

    try:
        server.get_hyper_index(300000, 100)
    except AssertionError:
        print("AssertionError raised when out of range")

    index = 3
    page_size = 2

    print("Nb items: {}".format(len(server._Server__indexed_dataset)))

    # 1- request first index
    res = server.get_hyper_index(index, page_size)
    print(res)

    # 2- request next index
    print(server.get_hyper_index(res.get('next_index'), page_size))

    # 3- remove the first index
    del server._Server__indexed_dataset[res.get('index')]
    print("Nb items: {}".format(len(server._Server__indexed_dataset)))

    # 4- request again the initial index -> the first data retrieved is not
    # the same as the first request
    print(server.get_hyper_index(index, page_size))

    # 5- request again initial next index -> same data page as the request 2-
    print(server.get_hyper_index(res.get('next_index'), page_size))
