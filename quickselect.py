def swap(a, i, j):
  a[i],a[j] = a[j],a[i]
  return 1 # return 1 to help count number of swaps

def partition_h(a, low, high, num_comp, num_swap):
  pivot = a[low]
  i,j = low+1,high
  while True:
    while i <= high:
      num_comp += 1
      if a[i] > pivot:
        break
      i += 1
    while j > low: # a[low] is pivot
      num_comp += 1
      if a[j] < pivot:
        break
      j -= 1
    if i > j:
      num_swap += swap(a,low,j)
      return j, num_comp, num_swap
    num_swap += swap(a,i,j)
    i += 1
    j -= 1

def qselect_h(a, k):
  num_comp, num_swap, low, high = 0,0,0,len(a)-1
  while low < high:
    pivotIdx, num_comp, num_swap = partition_h(a, low, high, num_comp, num_swap)
    if pivotIdx == k:
      break
    if pivotIdx > k:
      high = pivotIdx - 1
    else:
      low = pivotIdx + 1
  return a[k], num_comp, num_swap

def partition_g(a, low, high, k, num_comp, num_swap):
  # a: array of elements to select
  # k: the index to select
  # low, high: the lower/upper bound index between which the value resides
  # num_comp, num_swap: counters
  pivot = a[k] # pick pivot
  i,j = low,high # i,j will converge to k, instead of each other
  while True:
    while i < k: # mostly same as Hoare, except stop earlier at k instead of j
      num_comp += 1
      if a[i] > pivot:
        break
      i += 1
    while j > k: # mostly same as Hoare, except stop earlier at k instead of i
      num_comp += 1
      if a[j] < pivot:
        break
      j -= 1
    if i == k == j: # a[k] is the value we are looking for, just return that
      return k, k, num_comp, num_swap
    # in Hoare's quick select, the iteration continues until i,j crosses each other (when all elements have been partitioned).
    # But we can stop this iteration earlier if i == k or j == k, since by then we already know:
    # (1) Which side we will choose in the next iteration
    # (2) The other side (the part which has already been partitioned) are guarentted to not be the value we are looking for
    # (3) The current pivot is guaranteed to not be the value we are looking for
    # Therefore, we immediately return the correct side + the set of not-yet partitioned elements(which is guaranteed to be in the middle)
    # The next partition will then pick the another pivot
    if i == k: # pivot and all of right partition can be eliminated
      num_swap += swap(a,k,j) # get rid of the old pivot, old a[j] becomes new pivot
      return low, j-1, num_comp, num_swap
    if j == k: # pivot and all of right partition can be eliminated
      num_swap += swap(a,k,i) # get rid of the old pivot, old a[i] becomes new pivot
      return i+1, high, num_comp, num_swap
    num_swap += swap(a,i,j)
    i += 1
    j -= 1

def qselect_g(a, k):
  num_comp, num_swap, low, high = 0,0,0,len(a)-1
  while low < high:
    low, high, num_comp, num_swap = partition_g(a, low, high, k, num_comp, num_swap)
  return a[k], num_comp, num_swap

if __name__ == '__main__':
  from random import shuffle
  n = 1000
  c = list(range(1,2*n,2))
  shuffle(c)
  #c = [5,15,7,13,1,9,11,17,19,3]
  num_comp_sum_h, num_swap_sum_h = 0,0
  num_comp_sum_g, num_swap_sum_g = 0,0
  answer_correct = True
  print(c)
  for k in range(n):
    # list(c) creates a new, independent copy of c to select
    val_h, num_comp_h, num_swap_h = qselect_h(list(c),k)
    val_g, num_comp_g, num_swap_g = qselect_g(list(c),k)
    answer_correct &= (val_h == val_g == 2*k+1) # if any element mismatches then it'd be False
    print(f"{k: 5d}:\033[0;{'32m' if val_h==val_g==2*k+1 else '31m'}{val_g: >5d}\033[00m {num_comp_h: >5d}\033[0;{'32m>' if num_comp_h > num_comp_g else '32m=' if num_comp_h == num_comp_g else '31m<'}\033[00m{num_comp_g: <5d}{num_swap_h: >4d}\033[0;{'32m>' if num_swap_h > num_swap_g else '32m=' if num_swap_h == num_swap_g else '31m<'}\033[00m{num_swap_g: <4d}")
    num_comp_sum_h += num_comp_h
    num_swap_sum_h += num_swap_h
    num_comp_sum_g += num_comp_g
    num_swap_sum_g += num_swap_g
  print("Select index k, array value c[k], number of comparisons (h/g), number of swaps (h/g)")
  print("----------------------------------------")
  print(f"Hoare: Selecting {n} times (from index 0 to {n-1}) took a total of {num_comp_sum_h:d} comparisons and {num_swap_sum_h:d} swaps")
  print(f"Ours:  Selecting {n} times (from index 0 to {n-1}) took a total of {num_comp_sum_g:d} comparisons and {num_swap_sum_g:d} swaps")
  print(f"Hoare avg: {num_comp_sum_h/(n**2):f}n comparisons, {num_swap_sum_h/(n**2):f}n swaps per select.")
  print(f"Our avg:   {num_comp_sum_g/(n**2):f}n comparisons, {num_swap_sum_g/(n**2):f}n swaps per select.")
  print("----------------------------------------")
  print(f"All selected results match expected value: {answer_correct}")
