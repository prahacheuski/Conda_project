from pprint import pprint

from geo.geo import Geo

ADDRESS_VEC: list = ['Minsk', 'Moscow', 'Bangui', '453 Booth Street, Ottawa ON']

# ===== Basic Geo Class =====
geo = Geo()
coords = geo.get_coordinates(ADDRESS_VEC, method_name='yandex')
coords_table = geo.get_multiple_method_coordinates(ADDRESS_VEC)

pprint(coords)
print(f'\n{"=" * 30}\n')
print(coords_table)
