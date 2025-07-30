""" Hash Table ADT

Defines a Hash Table using a modified Linear Probe implementation for conflict resolution.
"""
from __future__ import annotations

from data_structures.referential_array import ArrayR
from typing import Generic, TypeVar, Union

K = TypeVar('K')
V = TypeVar('V')


class FullError(Exception):
    pass


class HashyStepTable(Generic[K, V]):
    """
    Hashy Step Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """
    REMOVED = object()

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes=None) -> None:
        """
        Initialise the Hash Table.

        Complexity:
        Best Case Complexity: O(max(N, M)) where N is the length of TABLE_SIZES and M is the length of sizes.
        Worst Case Complexity: O(max(N, M)) where N is the length of TABLE_SIZES and M is the length of sizes.
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes
        self.size_index = 0
        self.array: ArrayR[Union[tuple[K, V], None]] = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

    def hash(self, key: K) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.

        Complexity:
        Both the best and worst-case compelxity is O(K) where K refers to the number of characters in the key and
        it occurs due to the for loop that occurs in all instances in order to process each character of the key and come up with a
        hash value to use for the key.

        Best Case Complexity: O(K) where K refers to the number of characters in the key
        Worst Case Complexity: O(K) where K refers to the number of characters in the key
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K) -> int:
        """
        Used to determine the step size for our hash table.

        Complexity: See hash.

        Best Case Complexity: O(K) where K refers to the number of characters in the key
        Worst Case Complexity: O(K) where K refers to the number of characters in the key
        """
        return 1 + (self.hash(key) % (self.table_size - 1))

    @property
    def table_size(self) -> int:
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def _hashy_probe(self, key: K, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using hashy probing.

        Raises:
        KeyError: When the key is not in the table, but is_insert is False.
        FullError: When a table is full and cannot be inserted.

        Complexity:
        In the best-case complexity, it occurs when the key is found or there is a removed slot or an empty space is found in
        the first probe. It occurs when there are no collisions and the first slot is readily available for the 
        key to be inserted into, so, only the hash() method complexity is taken into account which has a complexity of O(K) where K is the
        number of characters in the key.

        In the worst-case complexity, it occurs when the hash table is almost completely filled up in which the probing continues
        until nearly all the N elements are gone through before a slot is open for insertion. It happens when there are no empty
        slots or no removed slots or the key is not found until the probe nearly reaches the end of the hash table due to many
        collisions occuring, thus, it leads to O(N) complexity where N is the number of keys currently being stored in the hash table. The hash() 
        method is also called which has a complexity of O(K), so, the final complexity is O(N + K).

        Best Case Complexity: O(K) where K refers to the number of characters in the key
        Worst Case Complexity: O(N + K) where N is the number of keys currently being stored in the hash table and K refers to the number 
        of characters in the key
        """
        location = self.hash(key)
        step_sizes = self.hash2(key)

        for _ in range(self.table_size):
            if self.array[location] is None:
                if is_insert == True:
                    return location 
                else:
                    raise KeyError(f"Key {key} not found.")
            elif self.array[location] == HashyStepTable.REMOVED:
                if is_insert == True:
                    return location  
            elif self.array[location][0] == key:
                return location 

            location = (location + step_sizes) % self.table_size
    
    def keys(self) -> list[K]:
        """
        Returns all keys in the hash table.

        :complexity: O(N) where N is self.table_size.
        """
        res = []
        for x in range(self.table_size):
            if self.array[x] is not None:
                res.append(self.array[x][0])
        return res

    def values(self) -> list[V]:
        """
        Returns all values in the hash table.

        :complexity: O(N) where N is self.table_size.
        """
        res = []
        for x in range(self.table_size):
            if self.array[x] is not None:
                res.append(self.array[x][1])
        return res

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See hashy probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :complexity: See hashy probe.
        :raises KeyError: when the key doesn't exist.
        """
        location = self._hashy_probe(key, False)

        if self.array[location] is not HashyStepTable.REMOVED and self.array[location][0] == key:
            return self.array[location][1]

    def __setitem__(self, key: K, data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        :complexity: See hashy probe.
        :raises FullError: when the table cannot be resized further.
        """
        location = self._hashy_probe(key, True)

        if self.array[location] is None or self.array[location] is HashyStepTable.REMOVED:
            self.array[location] = (key, data)
            self.count += 1

        elif self.array[location][0] == key:
            self.array[location] = (key, data)
            return None
        
        if len(self) > self.table_size * 2 / 3:
            self._rehash()

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) using lazy deletion

        Complexity: See hashy probe.

        Best Case Complexity: O(K) where K refers to the number of characters in the key
        Worst Case Complexity: O(N + K) where N is the number of keys currently being stored in the hash table and K refers to the number 
        of characters in the key
        """
        location = self._hashy_probe(key, False)

        if self.array[location] is not HashyStepTable.REMOVED and self.array[location][0] == key:
            self.array[location] = HashyStepTable.REMOVED
            self.count -= 1

    def is_empty(self) -> bool:
        return self.count == 0

    def is_full(self) -> bool:
        return self.count == self.table_size

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        Complexity: Both the best and worst-case complexity is O(N) where N is the number of keys currently being stored in the
        hash table because the hash table is resized and all elements inside the old hash table needs to be inserted into a new hash
        table that has a larger size and we are inserting N elements into this new hash table. In both cases, it has to go through a
        for loop N times to check if the item is None and if it is not, it inserts the element into the new hash table and
        then goes to the next iteration, so, even if most of the elements are None, the loop still has to iterate through N elements
        in the old hash table.

        Best Case Complexity: O(N) where N is the number of keys currently being stored in the hash table
        Worst Case Complexity: O(N) where N is the number of keys currently being stored in the hash table
        """
        previous_array = self.array
        self.size_index += 1

        if self.size_index == len(self.TABLE_SIZES):
            return None
        
        self.array = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

        for item in previous_array:
            if item is not None:
                key, value = item
                self[key] = value

    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular
        order).
        :complexity: O(N * (str(key) + str(value))) where N is the table size
        """
        result = ""
        for item in self.array:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result
