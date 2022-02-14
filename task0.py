def find(arr):
    l = []
    for item in arr:
        if item not in l:
            l.append(item)
    return len(l)
        
arr = ['a', 'b', 'a', 'c', 'C', 'c']
print(find(arr))