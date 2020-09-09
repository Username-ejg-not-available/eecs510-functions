
def fact(num):
    if num < 2:
        return 1
    return num * fact(num - 1)

def bSort(arr,size):
    #bubble sort
    sorted = False
    for i in range(size-1):
        if sorted:
            break
        sorted = True
        for j in range(size - i - 1):
            if arr[j] > arr[j+1]:
                temp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = temp
                sorted = False
    return arr