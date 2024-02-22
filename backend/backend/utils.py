from math import sqrt

def sum_mult_vector(query, doc):
  return sum(query[i] * doc[i] for i in range(len(query)))

def sum_dist_vector(vector):
  return sqrt(sum(vector[i]**2 for i in range(len(vector))))

def binary_search(word, data):
  left, right = 0, len(data) - 1

  while left <= right:
    mid = left + (right - left) // 2

    if data[mid]['word'] == word:
      return data[mid]
    elif data[mid]['word'] < word:
      left = mid + 1
    else:
      right = mid - 1

  return -1