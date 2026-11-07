import os

BOLD = "\033[1m"
RESET = "\033[0m"

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def quicksort(arr, left, right):
    if left < right:
        partition_pos = partition(arr, left, right)
        quicksort(arr, partition_pos + 1, right)
        quicksort(arr, left, partition_pos - 1)

def partition(arr, left, right):
    i = left
    j = right - 1
    pivot = arr[right]

    while i < j:
        while i < right and arr[i] <= pivot:
            i += 1
        while j > left and arr[j] >= pivot:
            j -= 1

        if i < j:
            arr[i], arr[j] = arr[j], arr[i]

    if arr[i] > pivot:
        arr[i], arr[right] = arr[right], arr[i]
    return i

def colored_text(text, color):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)

    return f"{BOLD}\033[38;2;{r};{g};{b}m{text}\033[0m{RESET}"