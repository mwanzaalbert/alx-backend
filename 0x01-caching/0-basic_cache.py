#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
basic_cache.py

This module implements a basic caching system through the BasicCache class,
which inherits from the BaseCaching class.

The BasicCache class provides the following functionalities:

- Storing items in a cache without any eviction policy.
- Allowing retrieval of cached items by their associated keys.

Usage:
    my_cache = BasicCache()
    my_cache.put("A", "Hello")
    value = my_cache.get("A")

The cache_data dictionary is used to store the cached items, where keys
are associated with their respective values.

Classes:
    BasicCache (BaseCaching): A basic cache storage system that allows
    storing and retrieving items based on provided keys without
    eviction policies.

Methods:
    put(key: str, item: str) -> None:
        Adds an item to the cache under the specified key. If either
        `key` or `item` is None, the method does nothing.

    get(key: str) -> Optional[str]:
        Retrieves an item from the cache by its key. Returns the item
        associated with the key, or None if the key doesn't exist.
"""

from base_caching import BaseCaching
from typing import Optional


class BasicCache(BaseCaching):
    """
    BasicCache class inherits from BaseCaching and is a basic cache storage
    system. This cache doesn't have any eviction policy and will store items
    based on provided keys.
    """

    def put(self, key: str, item: str) -> None:
        """
        Add an item to the cache under the specified key.

        Args:
            key (str): The key under which to store the item.
            item (str): The item to store in the cache.

        If either `key` or `item` is None, this function will do nothing.
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key: str) -> Optional[str]:
        """
        Retrieve an item from the cache by its key.

        Args:
            key (str): The key associated with the item to retrieve.

        Returns:
            str: The item associated with the key, or None if the key doesn't
                 exist.
        """
        return self.cache_data.get(key, None)


if __name__ == "__main__":
    my_cache = BasicCache()
    my_cache.print_cache()
    my_cache.put("A", "Hello")
    my_cache.put("B", "World")
    my_cache.put("C", "Holberton")
    my_cache.print_cache()
    print(my_cache.get("A"))
    print(my_cache.get("B"))
    print(my_cache.get("C"))
    print(my_cache.get("D"))
    my_cache.print_cache()
    my_cache.put("D", "School")
    my_cache.put("E", "Battery")
    my_cache.put("A", "Street")
    my_cache.print_cache()
    print(my_cache.get("A"))
