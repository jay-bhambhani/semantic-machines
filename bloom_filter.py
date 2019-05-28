from typing import Text, List, Callable, Any
import logging
import mmh3
from bitarray import bitarray
logger = logging.getLogger(__name__)


class BloomFilter:

    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        self.array = bitarray(size)

    def fpp(self, items_inserted: int) -> float:
        """
        calculates probability of false positive given number of items a user inserted into bloomfilter
        :param items_inserted: number of items inserted into bloomfilter
        :return: probability of false positive
        """
        p = (1 - (1 / self.size)) ** (self.num_hashes * items_inserted)
        return (1-p) ** self.num_hashes

    def _map_hashes(self, item: Text, m: Callable[[object, int], Any]) -> List[int]:
        """
        higher order function that will take an item, perform hash functions and then
        any requisite method that will be performed on these hashes
        :param item: item to hash
        :param m: method to apply to hashes
        :return: list of hashes created
        """
        idxs = [mmh3.hash(item, i) % self.size for i in range(self.num_hashes)]
        return [m(idx) for idx in idxs]

    def add(self, item: Text) -> None:
        """
        adds item to bloomfilter. only strings can be added so any non-string item to be added will have
        to build a string representation of itself prior to adding
        :param item: item to add
        """
        idxs_saved = self._map_hashes(item, self._increment)
        logger.debug('hashed and stored item {i} at indexes {idxs}'.format(i=item, idxs=idxs_saved))

    def find(self, item: Text) -> bool:
        """
        hashes item and determines whether it exists in bloomfilter. similar to above, a string item has to be used
        for finding
        :param item: item to find in bloomfilter
        :return: boolean whether item is in filter or not
        """
        checks = self._map_hashes(item, self._check_index)
        logger.debug('item {i} returned checks {c} with hashes'.format(i=item, c=checks))
        if all(checks):
            return True
        return False

    def _increment(self, idx: int) -> int:
        """
        hidden method to change bitarray indexes
        :param idx: index to increment
        :return: index incremented
        """
        self.array[idx] = 1
        return idx

    def _check_index(self, idx) -> bool:
        """
        hidden method to check if index has been incremented
        :param idx: index to check
        :return: boolean if index is > 0
        """
        if self.array[idx]:
            return True
        else:
            return False

