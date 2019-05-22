from typing import Text, List, Callable, Any
import logging
import mmh3

logger = logging.getLogger(__name__)


class BloomFilter:

    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        self.array = [0] * size

    def fpp(self, items_inserted: int) -> float:
        p = (1 - (1 / self.size)) ** (self.num_hashes * items_inserted)
        return (1-p) ** self.num_hashes

    def _map_hashes(self, item: Text, f: Callable[int, Any]) -> List[int]:
        idxs = [mmh3.hash(item, i) % self.size for i in range(self.num_hashes)]
        return [f(idx) for idx in idxs]

    def add(self, item: Text):
        idxs_saved = self._map_hashes(item, self._increment)
        logger.debug('hashed and stored item {i} at indexes {idxs}'.format(i=item, idxs=idxs_saved))

    def find(self, item: Text) -> bool:
        checks = self._map_hashes(item, self._check_index)
        logger.debug('item {i} returned checks {c} with hashes'.format(i=item, c=checks))
        if all(checks):
            return True
        return False

    def _increment(self, idx: int) -> int:
        self.array[idx] = 1
        return idx

    def _check_index(self, idx) -> bool:
        if self.array[idx]:
            return True
        else:
            return False

