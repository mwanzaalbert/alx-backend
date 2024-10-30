#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LRU Cache module

This module provides the LRUCache class, a caching system that inherits from
BaseCaching and follows a Least Recently Used (LRU) eviction policy.
"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """
    LRUCache class that inherits from BaseCaching and implements a caching
    system with LRU eviction policy.
    """

    def __init__(self) -> None:
        """
        Initialize the LRUCache with an empty order list to track access
        order."""
        super().__init__()
        self.__access_order = []  # Keeps track of the access order of keys

    def put(self, key: str, item: str) -> None:
        """
        Add an item to the cache. If the cache exceeds the maximum limit, the
        least recently used item is removed to make space for the new one.

        Args:
            key (str): The key under which to store the item.
            item (str): The item to store in the cache.

        If either `key` or `item` is None, this function doesn'thing.
        """
        if key is None or item is None:
            return

        # Update existing key & move it to the end to mark it as recently used
        if key in self.cache_data:
            self.__access_order.remove(key)
        # If cache limit is exceeded, discard the least recently used item
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            lru_key = self.__access_order.pop(0)
            del self.cache_data[lru_key]
            print(f"DISCARD: {lru_key}")

        # Add the new key-value pair to the cache and mark it as recently used
        self.cache_data[key] = item
        self.__access_order.append(key)

    def get(self, key: str) -> str:
        """
        Retrieve an item from the cache by its key.

        Args:
            key (str): The key associated with the item to retrieve.

        Returns:
            str: The item associated with the key, or None if the key doesn't
                 exist.
        """
        if key in self.cache_data:
            # Update the access order to mark the key as recently used
            self.__access_order.remove(key)
            self.__access_order.append(key)
            return self.cache_data[key]
        return None


if __name__ == "__main__":
    my_cache = LRUCache()
    my_cache.put("A", "Hello")
    my_cache.put("B", "World")
    my_cache.put("C", "Holberton")
    my_cache.put("D", "School")
    my_cache.print_cache()
    print(my_cache.get("B"))
    my_cache.put("E", "Battery")
    my_cache.print_cache()
    my_cache.put("C", "Street")
    my_cache.print_cache()
    print(my_cache.get("A"))
    print(my_cache.get("B"))
    print(my_cache.get("C"))
    my_cache.put("F", "Mission")
    my_cache.print_cache()
    my_cache.put("G", "San Francisco")
    my_cache.print_cache()
    my_cache.put("H", "H")
    my_cache.print_cache()
    my_cache.put("I", "I")
    my_cache.print_cache()
    my_cache.put("J", "J")
    my_cache.print_cache()
    my_cache.put("K", "K")
    my_cache.print_cache()
