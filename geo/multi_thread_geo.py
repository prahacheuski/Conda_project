from typing import Union, Dict, Optional, Iterable, List, Tuple
from multiprocessing import Pool

from geo import Geo


class MultiThreadGeo(object):
    __slots__ = '__geo', '__number_of_threads'

    def __init__(self, geo: Geo, number_of_threads: int = 5):
        self.__geo: Geo = geo
        self.__number_of_threads: int = number_of_threads

    def __m_thread_run(self, callback, address: List[str]):
        with Pool(processes=self.__number_of_threads) as pool:
            result = pool.map(func=callback, iterable=address, chunksize=int(len(address) / self.__number_of_threads))

        return result

    def get_coordinates(self, address: List[str], method_name: str,
                        leave_null_values: bool = False) -> Optional[Union[Geo.Point, List[Geo.Point]]]:
        return self.__m_thread_run(self.__geo.get_coordinates, address)
