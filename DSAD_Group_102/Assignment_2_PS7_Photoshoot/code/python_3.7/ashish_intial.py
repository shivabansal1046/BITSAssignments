import time;
# Global initialization
final_input = []
products = []
staging = []
photo = []
burst_time_photo = []
arival_time_photo = []
sum_bustTime = 0
pos = 0
seq = []

min = 0


# Sample Output:
# Product Sequence: F, A, E, B, C, D
# Total time to complete photoshoot: 205 minutes
# Idle time for Xavier: 10 minutes

# Common File reader function
def fileReader(path):
    try:
        inputFile = open(path, 'r')
        return inputFile
    except(FileNotFoundError, IOError):
        print("file not found, exiting the program !!!")
        exit(1)


def printJobSequence(arr, n):
    print("Product Sequence: ", ','.join([str(arr[x][0]) for x in range(n)]))


def calculate_arial_time_photo(arr, n):
    at_time_sum = arr[0][1]
    arival_time_photo.append(arr[0][1])

    for i in range(1, n):
        at_time_sum += arr[i][1]
        arival_time_photo.append(at_time_sum)
    print("arival_time_photo: ", ','.join([str(arival_time_photo[x]) for x in range(n)]))


def calculate_burst_time_photo(arr, n):
    sum_burstTime =0
    for i in range(n):
        burst_time_photo.append(arr[i][2])
        sum_burstTime += arr[i][2]
    print("burst_time_photo: ", ','.join([str(burst_time_photo[x]) for x in range(n)]))
    return sum_burstTime


def print_Idle_Total_photo(n, total_burst_sum):
    global k
    max = 0
    idle = arival_time_photo[0]
    start = arival_time_photo[0]
    max = arival_time_photo[n-1]

    for i in range(n):
        for k in range(n):
            min = max
            for j in range(n):
                if arival_time_photo[j] != -1:
                    if arival_time_photo[j] < min:
                        min = arival_time_photo[j]
                        pos = j

        if start < arival_time_photo[pos]:
            idle += arival_time_photo[pos] - start
            start = arival_time_photo[pos]
            start += burst_time_photo[pos]
            arival_time_photo[pos] = -1
        else:
            start += burst_time_photo[pos]
            arival_time_photo[pos] = -1

    print("Total time to complete photoshoot: ", total_burst_sum + idle, "minutes")
    print("Idle time for Xavier : ", idle)


# This function is for calculating and printing the total elapsed time and idle time
# def calculate_print_total_idle_Time(sum_stage_photo_arr, stage_Input, photoInput, n):


# This function is for to short the input array value based on input column
def shortJobScheduling(arr, c_n):
    # length of array
    n = len(arr)
    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j][c_n] > arr[j + 1][c_n]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    printJobSequence(arr, n)
    calculate_arial_time_photo(arr, n)
    total_burst_sum = calculate_burst_time_photo(arr, n)
    print_Idle_Total_photo(n, total_burst_sum)


def main():
    # Sample Input:
    # Products: A / B / C / D / E / F
    # Staging: 20 / 30 / 45 / 60 / 20 / 10
    # Photo: 30 / 30 / 15 / 20 / 40 / 60

    # Reading content from input file to store in the local array
    t0 = time.time()
    file_records = fileReader('input.txt')
    sum_bustTime = 0

    for input_rec in file_records:
        if input_rec.split(":")[0].strip() == "Products":
            products = input_rec.split(":")[1].split("/")
        elif input_rec.split(":")[0].strip() == "Staging":
            staging = input_rec.split(":")[1].split("/")
        elif input_rec.split(":")[0].strip() == "Photo":
            photo = input_rec.split(":")[1].split("/")

    for i in range(len(products)):
        final_input.append((products[i].strip(), int(staging[i].strip()), int(photo[i].strip())))

    shortJobScheduling(final_input, 1)
    t1 = time.time()
    print("Time taken is:", t1-t0)


if __name__ == "__main__":
    main()
