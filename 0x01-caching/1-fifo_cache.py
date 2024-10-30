#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIFO Cache module

This module provides the FIFOCache class, a caching system that inherits from
BaseCaching and follows a First-In-First-Out (FIFO) eviction policy. When the
cache exceeds its limit, it discards the oldest item.
"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache class that inherits from BaseCaching and implements a caching
    system with FIFO eviction policy.

    Examples:
        >>> my_cache = FIFOCache()
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
        DISCARD: A
        >>> my_cache.print_cache()
        Current cache:
        B: World
        C: Holberton
        D: School
        E: Battery
        >>> my_cache.put("C", "Street")
        >>> my_cache.print_cache()
        Current cache:
        B: World
        C: Street
        D: School
        E: Battery
        >>> my_cache.put("F", "Mission")
        DISCARD: B
        >>> my_cache.print_cache()
        Current cache:
        C: Street
        D: School
        E: Battery
        F: Mission
    """

    def put(self, key: str, item: str) -> None:
        """
        Add an item to the cache. If the cache exceeds the maximum limit, the
        oldest item (first added) is removed to make space for the new one.

        Args:
            key (str): The key under which to store the item.
            item (str): The item to store in the cache.

        If either `key` or `item` is None, this function doesn'thing.
        """
        if key is not None and item is not None:
            cache_limit = BaseCaching.MAX_ITEMS
            cache_size = len(self.cache_data)

            if cache_size >= cache_limit and key not in self.cache_data:
                oldest_key = next(iter(self.cache_data))
                # Remove the oldest item in the cache (FIFO)
                self.cache_data.pop(oldest_key)
                print(f"DISCARD: {oldest_key}")

            # Add the new item
            self.cache_data[key] = item

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
