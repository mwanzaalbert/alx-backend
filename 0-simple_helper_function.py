#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pagination Utility Module.

This module provides a utility function to support pagination. Specifically,
it includes the `index_range` function, which calculates the start and end
indexes for a given page and page size, making it easy to extract the
appropriate slice of data for a specific page.

Functions:
    index_range(page: int, page_size: int) -> Tuple[int, int]
        Calculates and returns the start and end indexes for pagination, given
        a page number and page size.

Example Usage:
    >>> from pagination import index_range
    >>> index_range(1, 10)
    (0, 10)

    >>> index_range(3, 15)
    (30, 45)

This module is equipped with doctests, and can be run as a standalone script
to verify functionality.
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the start and end index for a specific page and page size in
    pagination.

    Args:
        page (int): The page number, 1-indexed (e.g., page 1 corresponds to the
                                                first set of results).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start index (inclusive) and
                        end index (exclusive) for the items on the requested
                        page.

    Example:
        >>> res = index_range(1, 7)
        >>> print(type(res))
        <class 'tuple'>
        >>> print(res)
        (0, 7)

        >>> res = index_range(page=3, page_size=15)
        >>> print(type(res))
        <class 'tuple'>
        >>> print(res)
        (30, 45)
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    return start_index, end_index


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
