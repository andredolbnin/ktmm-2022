def find(arr):
    d = {}
    for item in arr:
        if item in d.keys():
            d[item] += 1
        else:
            d[item] = 1
    return len(d)
        
arr = ['a', 'b', 'a', 'c', 'C']
print(find(arr))