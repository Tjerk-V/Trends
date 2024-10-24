def sort(array, key):
    n = len(array)

    for i in range(n):
        already_sorted = True

        for j in range(n - i - 1):
            value1 = float(array[j][key])
            value2 = float(array[j + 1][key])
            if value1 < value2:
                array[j], array[j + 1] = array[j + 1], array[j]
                already_sorted = False

        if already_sorted:
            break

    return array