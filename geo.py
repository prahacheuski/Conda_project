from collections import namedtuple
from cmath import isclose
import geocoder
import re


class Geo(object):
    __slots__ = '__methods_confidence_map', '__rel_tol'
    __wkt_pattern: re.compile = re.compile(r'^POINT\((?P<x>\S+)\s+(?P<y>\S+)\)$')
    Point: namedtuple = namedtuple('Point', ('x', 'y'))

    def __init__(self, methods_confidence_map: dict, rel_tol: float = 1e-09):
        """

        :param methods_confidence_map:
        :param rel_tol: is the relative tolerance – it is the maximum allowed difference between a and b,
                        relative to the larger absolute value of a or b. For example, to set a tolerance of 5%,
                        pass rel_tol=0.05. The default tolerance is 1e-09, which assures that the two values are
                        the same within about 9 decimal digits. rel_tol must be greater than zero.
        """
        self.__methods_confidence_map: dict = methods_confidence_map
        self.__rel_tol: float = rel_tol

    def __parse_wtk(self, in_str: str) -> dict:
        search_result = self.__wkt_pattern.search(in_str)
        result = search_result.groupdict() if search_result else None
        return result

    def __get_wkt(self, query_result) -> Point:
        result = None

        try:
            wkt = self.__parse_wtk(query_result.wkt)

        except AttributeError:
            pass

        else:
            if wkt:
                x, y = wkt.get('x', None), wkt.get('y', None)
                if x and y:
                    result = self.Point(float(x), float(y))

        return result

    def __get_osm(self, query_result) -> Point:
        result = None

        try:
            osm = query_result.osm

        except AttributeError:
            pass

        else:
            if osm:
                x, y = osm.get('x', None), osm.get('y', None)
                if x and y:
                    result = self.Point(float(x), float(y))

        return result

    def __get_lat_and_lng(self, query_result):
        wkt = self.__get_wkt(query_result)
        osm = self.__get_osm(query_result)

        if wkt and osm:
            if isclose(wkt.x, osm.x, rel_tol=self.__rel_tol) and isclose(wkt.y, osm.y, rel_tol=self.__rel_tol):
                result = wkt

            else:
                raise ValueError(f'Values in the fields are not equal: WKT={wkt}\tOSM={osm}')

        else:
            result = (wkt or osm)

        return result

    def get_point(self, address: str, return_method_name: bool = False) -> Point:
        lat_lng_vec: list = []

        for method, confidence in self.__methods_confidence_map.items():
            try:
                res: geocoder = eval(f'geocoder.{method}(address)')

            except Exception:
                pass
                # print(f'Skip method "{method.capitalize()}" because of errors.')

            else:
                lat_lng = self.__get_lat_and_lng(res) if res else None

                if lat_lng:
                    lat_lng_vec.append((method, lat_lng))

        if lat_lng_vec:
            lat_lng_vec = sorted(lat_lng_vec, key=lambda vec: self.__methods_confidence_map.get(vec[0]), reverse=True)
            method_name, x, y = lat_lng_vec[0][0], lat_lng_vec[0][1].x, lat_lng_vec[0][1].y

            for i in range(1, len(lat_lng_vec)):
                method_name_, x_, y_ = lat_lng_vec[i][0], lat_lng_vec[i][1].x, lat_lng_vec[i][1].y

                if not (isclose(x, x_, rel_tol=self.__rel_tol) and isclose(y, y_, rel_tol=self.__rel_tol)):
                    if self.__methods_confidence_map[method_name_] > self.__methods_confidence_map[method_name]:
                        method_name, x, y = method_name_, x_, y_

                    elif self.__methods_confidence_map[method_name_] == self.__methods_confidence_map[method_name]:
                        raise ValueError(f'"X", "Y" values are inconsistent:\nMethod "{method_name}" values x={x} y={y}'
                                         f'\nMethod "{method_name_}" values x={x_} y={y_}\n')

            result = (method_name, self.Point(x, y)) if return_method_name else self.Point(x, y)

        else:
            result = None

        return result


if __name__ == '__main__':
    methods_degree_of_confidence_map = {'arcgis': 0.5,
                                        'baidu': 0.5,
                                        'bing': 0.8,
                                        'gaode': 0.5,
                                        'geocodefarm': 0.5,
                                        'geolytica': 0.5,
                                        'geonames': 0.5,
                                        'ottawa': 0.5,
                                        'google': 0.95,
                                        'here': 0.5,
                                        'locationiq': 0.5,
                                        'mapbox': 0.7,
                                        'mapquest': 0.5,
                                        'opencage': 0.5,
                                        'osm': 0.5,
                                        'tamu': 0.5,
                                        'tomtom': 0.7,
                                        'w3w': 0.5,
                                        'yahoo': 0.8,
                                        'yandex': 0.8,
                                        'tgos': 0.5}

    geo = Geo(methods_degree_of_confidence_map)
    minsk = geo.get_point('Minsk', return_method_name=True)
    moscow = geo.get_point('Moscow', return_method_name=True)
    bangui = geo.get_point('Bangui', return_method_name=True)
    print('Minsk: {minsk[1]} (source - {minsk[0]})\n'
          'Moscow: {moscow[1]} (source - {moscow[0]})\n'
          'Bangui: {bangui[1]} (source - {bangui[0]})'.format(**locals()))
