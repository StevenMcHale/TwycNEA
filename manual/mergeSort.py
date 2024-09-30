# Merge Sort

def mergeSort(mergeList):
  if len(mergeList) > 1:
    mid = len(mergeList) // 2     # Gets the midpoint as an integer

    
    lefthalf = mergeList[:mid]  # Puts the left half of mergelist into lefthalf
    righthalf = mergeList[mid:] # Puts the right half of mergelist into righthalf

    
    # keeps calling itself until all elements of mergelist are in separte lists
    mergeSort(lefthalf)
    mergeSort(righthalf)

    # resets values for i, j and k
    i = 0
    j = 0
    k = 0

    # Two lists are merged into one list with all of the elements in order
    while i < len(lefthalf) and j < len(righthalf):
      if lefthalf[i] < righthalf[j]:
        mergeList[k] = lefthalf[i]
        i = i + 1
      else:
        mergeList[k] = righthalf[j]
        j = j + 1
      k = k + 1


    # checks if left half has elements not merged
    while i < len(lefthalf):
      mergeList[k] = lefthalf[i]
      i = i + 1
      k = k + 1


    # checks if right half has elements not merged
    while j < len(righthalf):
      mergeList[k] = righthalf[j]
      j = j + 1
      k = k + 1
