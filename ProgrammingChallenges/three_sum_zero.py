def threeSumZero(arr):
  if len(arr) < 3:
    print("None")
    return None

  arr.sort()

  for i in range(0, len(arr) - 2):
    left = i + 1
    right = len(arr) - 1

    while left < right:
      sum = arr[i] + arr[left] + arr[right]

      if sum == 0:
        print([arr[i], arr[left], arr[right]])
        return [arr[i], arr[left], arr[right]]
      elif sum < 0:
        left += 1
      else:
        right -= 1

  print("None")
  return None

print(threeSumZero([3, 5, 8, 10, -9, -11]) == [-11, 3, 8])
print(threeSumZero([0, 3, 4, 8, -1, -3]) == [-3, -1, 4])
print(threeSumZero([]) is None)
