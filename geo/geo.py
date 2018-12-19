from typing import Union, Dict, Optional, Iterable, List
from collections import namedtuple
from cmath import isclose
from pprint import pprint
import pandas as pd
import warnings
import requests
import geocoder
import re


class Geo(object):
    __slots__ = '__methods_confidence_map', '__rel_tol'
    __wkt_pattern: re.compile = re.compile(r'^POINT\((?P<x>\S+)\s+(?P<y>\S+)\)$')
    Point: namedtuple = namedtuple('Point', ('address', 'x', 'y'))  # mapping between address and coordinates

    def __init__(self, methods_confidence_map: Optional[Dict[str, float]] = None, rel_tol: float = 1e-09) -> None:
        """
        TODO: Write comment
        :param methods_confidence_map:
        :param rel_tol: is the relative tolerance – it is the maximum allowed difference between 'x' and 'y'
                        coordinates points of two sources 'wkt' and 'osm', relative to the larger absolute value
                        of 'a' or 'b'. For example, to set a tolerance of 5%, pass rel_tol=0.05.
                        The default tolerance is 1e-09, which assures that the two values are
                        the same within about 9 decimal digits. rel_tol must be greater than zero.
        """
        self.__methods_confidence_map: Optional[Dict[str, float]] = methods_confidence_map
        self.__rel_tol: float = rel_tol

    def __parse_wtk(self, in_str: str) -> Dict[str, str]:
        """
        TODO: Write comment
        :param in_str:
        :return:
        """
        search_result = self.__wkt_pattern.search(in_str)
        result = search_result.groupdict() if search_result else None
        return result

    def __get_wkt(self, address: str, query_result) -> Optional[Point]:
        """
        TODO: Write comment
        :param address:
        :param query_result:
        :return:
        """
        result = None

        try:
            wkt = self.__parse_wtk(query_result.wkt) if query_result.wkt else None

        except AttributeError:
            pass

        else:
            if wkt:
                x, y = wkt.get('x', None), wkt.get('y', None)
                if x and y:
                    result = self.Point(address, float(x), float(y))

        return result

    def __get_osm(self, address: str, query_result) -> Optional[Point]:
        """
        TODO: Write comment
        :param address:
        :param query_result:
        :return:
        """
        result = None

        try:
            osm = query_result.osm

        except AttributeError:
            pass

        else:
            if osm:
                x, y = osm.get('x', None), osm.get('y', None)
                if x and y:
                    result = self.Point(address, float(x), float(y))

        return result

    def __get_lat_and_lng(self, address: str, query_result) -> Optional[Point]:
        """
        TODO: Write comment
        :param address:
        :param query_result:
        :return:
        """
        wkt = self.__get_wkt(address, query_result)
        osm = self.__get_osm(address, query_result)

        if wkt and osm:
            if isclose(wkt.x, osm.x, rel_tol=self.__rel_tol) and isclose(wkt.y, osm.y, rel_tol=self.__rel_tol):
                result = wkt

            else:
                raise ValueError(f'Values in the fields are not equal: WKT={wkt}\tOSM={osm}')

        else:
            result = (wkt or osm)

        return result

    def get_coordinates(self, address: Union[str, Iterable[str]], method_name: str,
                        leave_null_values: bool = False) -> Optional[Union[Point, List[Point]]]:
        """
        TODO: Write comment
        :param address:
        :param method_name:
        :param leave_null_values:
        :return:
        """
        result: list = []
        method = getattr(geocoder, method_name)

        with requests.Session() as session:
            if isinstance(address, str):
                try:
                    res = method(address, session=session)

                except Exception:
                    pass  # Place to add logging

                else:
                    result.append(self.__get_lat_and_lng(address, res))

            else:
                for addr in address:
                    try:
                        res = method(addr, session=session)

                    except Exception:
                        pass  # Place to add logging

                    else:
                        result.append(self.__get_lat_and_lng(addr, res))

        if not leave_null_values:
            result = list(filter(None, result))

        return result if len(result) > 1 else result[0] if result else None

    def get_multiple_method_coordinates(self, address: Union[str, List[str]],
                                        method_name_vec: Optional[Union[str, Iterable[str]]] = None) \
            -> Optional[pd.DataFrame]:
        """
        TODO: Write comment
        :param address:
        :param method_name_vec:
        :return:
        """
        assert self.__methods_confidence_map is not None, 'Constructor argument "methods_confidence_map" is required'

        df_vec: list = []

        for method_name in method_name_vec:
            if method_name not in self.__methods_confidence_map:
                warnings.warn(f'Method "{method_name}" not found in "methods_confidence_map".', Warning)

            else:
                current_res = self.get_coordinates(address, method_name, leave_null_values=True)

                if current_res:
                    data_: dict = {k: [[v.x, v.y] if v else None] for k, v in zip(address, current_res)}
                    df_vec.append(pd.DataFrame(data=data_, index=[method_name], columns=address))

        result_df: pd.DataFrame = pd.concat(df_vec)
        result_df.dropna(how='all', inplace=True)

        return result_df


if __name__ == '__main__':
    methods_degree_of_confidence_map: Dict[str, float] = {'arcgis': 0.5, 'baidu': 0.5, 'bing': 0.8, 'gaode': 0.5,
                                                          'geocodefarm': 0.5, 'geolytica': 0.5, 'geonames': 0.5,
                                                          'ottawa': 0.5, 'google': 0.95, 'here': 0.5, 'locationiq': 0.5,
                                                          'mapbox': 0.7, 'mapquest': 0.5, 'opencage': 0.5, 'osm': 0.5,
                                                          'tamu': 0.5, 'tomtom': 0.7, 'w3w': 0.5, 'yahoo': 0.8,
                                                          'yandex': 0.8, 'tgos': 0.5}

    geo = Geo(methods_degree_of_confidence_map)
    coordinates = geo.get_coordinates(['Minsk', 'Moscow', 'Bangui', '453 Booth Street, Ottawa ON'],
                                      method_name='yandex')
    coordinates_df = geo.get_multiple_method_coordinates(['Minsk', 'Moscow', 'Bangui', '453 Booth Street, Ottawa ON'],
                                                         method_name_vec=('yandex', 'google'))
    pprint(coordinates)
    print(f'\n{"=" * 30}\n')
    print(coordinates_df)
