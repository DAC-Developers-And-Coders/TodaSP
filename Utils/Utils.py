import os

BOLD = "\033[1m"
RESET = "\033[0m"

LEGAL_NATURE = {
    "PUBLIC": [
        "1015", "1023", "1031", "1040", "1058",
        "1066", "1074", "1082", "1104", "1112",
        "1120", "1139", "1147", "1155", "1163",
        "1171", "1180", "1198", "1210", "1228",
        "1236", "1244", "1252", "1260", "1279",
        "1287", "1295", "1309", "1317", "1325",
        "1333", "1341"
    ],
    "PRIVATE": [
        "2011", "2038", "2046", "2054", "2062",
        "2070", "2089", "2097", "2127", "2135",
        "2143", "2151", "2160", "2178", "2194",
        "2216", "2224", "2232", "2240", "2259",
        "2267", "2275", "2283", "2291", "2305",
        "2313", "2321", "2330", "2348", "2356"
    ],
    "NON_PROFIT": [
        "3034", "3069", "3077", "3085", "3107",
        "3115", "3131", "3204", "3212", "3220",
        "3239", "3247", "3255", "3263", "3271",
        "3280", "3298", "3301", "3310", "3328",
        "3999"
    ],
    "NATURAL_PERSON": [
        "4014", "4022", "4081",
        "4090", "4111", "4120"
    ],
    "INTERNATIONAL_ORGANIZATIONS": [
        "5010", "5029", "5037"
    ]
}

FACILITIES_CODES = {
    "Farmácia": [43],
    "Posto de Saúde": [1],
    "Unidade Básica de Saúde": [2],
    "Hospital": [5, 7, 15, 62],
    "Centro de Parto Normal": [61],
    "Pronto Socorro": [20, 21],
    "Pronto Atendimento": [73],
    "Clínica/Diagnóstico": [4, 22, 36, 39]
}

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