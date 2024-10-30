#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LFU Cache module

This module provides the LFUCache class, a caching system that inherits from
BaseCaching and follows a Least Frequently Used (LFU) eviction policy.
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache class that inherits from BaseCaching and implements a caching
    system with LFU eviction policy.
    """

    def __init__(self) -> None:
        """Initialize the LFUCache with additional tracking dictionaries."""
        super().__init__()
        self.__frequency = {}   # Tracks the frequency of each key
        self.__usage_order = {}  # Tracks order of usage for @ frequency level

    def __update_usage(self, key):
        """
        Update the usage information for a key, promoting it to the next
        frequency level.
        """
        freq = self.__frequency[key]
        self.__frequency[key] += 1

        # Remove the key from the current frequency usage order
        self.__usage_order[freq].remove(key)
        if not self.__usage_order[freq]:
            del self.__usage_order[freq]

        # Add the key to the next frequency level
        new_freq = freq + 1
        if new_freq not in self.__usage_order:
            self.__usage_order[new_freq] = []
        self.__usage_order[new_freq].append(key)

    def put(self, key: str, item: str) -> None:
        """
        Add an item to the cache. If the cache exceeds the maximum limit,
        the least frequently used item is removed, with the LRU policy applied
        in case of ties.

        Args:
            key (str): The key under which to store the item.
            item (str): The item to store in the cache.

        If either `key` or `item` is None, this function doesn'thing.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Update the item and promote its frequency
            self.cache_data[key] = item
            self.__update_usage(key)
        else:
            # Check if cache size exceeds the limit
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Find lowest frequency level with the least recently used item
                min_freq = min(self.__usage_order.keys())
                key_to_discard = self.__usage_order[min_freq].pop(0)
                if not self.__usage_order[min_freq]:
                    del self.__usage_order[min_freq]

                # Remove the item from cache and frequency tracker
                del self.cache_data[key_to_discard]
                del self.__frequency[key_to_discard]
                print(f"DISCARD: {key_to_discard}")

            # Add new key-value pair and initialize its frequency and usage
            self.cache_data[key] = item
            self.__frequency[key] = 1
            if 1 not in self.__usage_order:
                self.__usage_order[1] = []
            self.__usage_order[1].append(key)

    def get(self, key: str) -> str:
        """
        Retrieve an item from the cache by its key, promoting its frequency.

        Args:
            key (str): The key associated with the item to retrieve.

        Returns:
            str: The item associated with the key, or None if the key doesn't
                 exist.
        """
        if key in self.cache_data:
            # Update the usage and frequency
            self.__update_usage(key)
            return self.cache_data[key]
        return None


if __name__ == "__main__":
    my_cache = LFUCache()
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
    print(my_cache.get("I"))
    print(my_cache.get("H"))
    print(my_cache.get("I"))
    print(my_cache.get("H"))
    print(my_cache.get("I"))
    print(my_cache.get("H"))
    my_cache.put("J", "J")
    my_cache.print_cache()
    my_cache.put("K", "K")
    my_cache.print_cache()
    my_cache.put("L", "L")
    my_cache.print_cache()
    my_cache.put("M", "M")
    my_cache.print_cache()
