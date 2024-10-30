#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache class inherits from BaseCaching and is a basic cache storage
    system. This cache doesn't have any eviction policy and will store items
    based on provided keys.
    """

    def put(self, key, item) -> None:
        """
        Add an item to the cache under the specified key.

        Args:
            key (str): The key under which to store the item.
            item (str): The item to store in the cache.

        If either `key` or `item` is None, this function will do nothing.
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key) -> str:
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
