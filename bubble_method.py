array_of_int = [8, 4, 6, 7, 9, 1, 5, 3, 2]


def sort_array(array):
    var = 1
    while var < len(array):
        for item in range(len(array) - var):
            if array[item] > array[item + 1]:
                array[item], array[item + 1] = array[item + 1], array[item]
        var += 1
    return array


print(sort_array(array_of_int))
