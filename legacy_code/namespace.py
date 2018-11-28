a = 1


def outer():
    a = 2
    print(a)
    print(locals()["a"])

    def middle():
        nonlocal a
        a += 3
        print(a)

        def inner():
            a = 4
            print(a)

        return inner

    return middle
print(a)

outer()()()