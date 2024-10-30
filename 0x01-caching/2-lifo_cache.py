#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LIFO Cache module

This module provides the LIFOCache class, a caching system that inherits from
BaseCaching and follows a Last-In-First-Out (LIFO) eviction policy. When the
cache exceeds its limit, it discards the most recently added item.
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache class that inherits from BaseCaching and implements a caching
    system with LIFO eviction policy.

    Examples:
        >>> my_cache = LIFOCache()
        >>> my_cache.put("A", "Hello")
        >>> my_cache.put("B", "World")
        >>> my_cache.put("C", "Holberton")
        >>> my_cache.put("D", "School")
        >>> my_cache.print_cache()
        Current cache:
        A: Hello
        B: World
        C: Holberton
        D: School
        >>> my_cache.put("E", "Battery")
        DISCARD: D
        >>> my_cache.print_cache()
        Current cache:
        A: Hello
        B: World
        C: Holberton
        E: Battery
        >>> my_cache.put("C", "Street")
        >>> my_cache.print_cache()
        Current cache:
        A: Hello
        B: World
        C: Street
        E: Battery
        >>> my_cache.put("F", "Mission")
        DISCARD: C
        >>> my_cache.print_cache()
        Current cache:
        A: Hello
        B: World
        E: Battery
        F: Mission
        >>> my_cache.put("G", "San Francisco")
        DISCARD: F
        >>> my_cache.print_cache()
        Current cache:
        A: Hello
        B: World
        E: Battery
        G: San Francisco
    """

    def __init__(self) -> None:
        """
        Initialize the LIFOCache with an empty stack to track insertion
        order."""
        super().__init__()
        self.__stack_keys = []

    def put(self, key: str, item: str) -> None:
        """
        Add an item to the cache. If the cache exceeds the maximum limit, the
        most recently added item (last in) is removed to make space for the
        new one.

        Args:
            key (str): The key under which to store the item.
            item (str): The item to store in the cache.

        If either `key` or `item` is None, this function doesn'thing.
        """
        if key is not None and item is not None:
            cache_limit = BaseCaching.MAX_ITEMS

            # If key exists, remove it to update the position in the stack
            if key in self.cache_data:
                self.__stack_keys.remove(key)
            # If cache limit exceeded and new key, discard the most recent item
            elif len(self.cache_data) >= cache_limit:
                key_to_remove = self.__stack_keys.pop()
                self.cache_data.pop(key_to_remove)
                print(f"DISCARD: {key_to_remove}")

            # Add new item to cache and stack
            self.cache_data[key] = item
            self.__stack_keys.append(key)

    def get(self, key: str) -> str:
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
    import doctest
    doctest.testmod(verbose=True)
