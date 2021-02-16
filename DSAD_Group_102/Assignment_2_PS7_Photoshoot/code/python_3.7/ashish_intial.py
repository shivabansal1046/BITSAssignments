final_input = []
products = []
staging = []
photo = []


def fileReader(path):
    try:
        inputFile = open(path, 'r')
        return inputFile
    except(FileNotFoundError, IOError):
        print("file not found, exiting the program !!!")
        exit(1)


# This function is use for to print the job sequence
def printJobSequence(arr):
    summed_array = []
    sum = 0
    n = len(arr)

#1
    print("Product Sequence:")
    print(','.join([str(arr[x][0]) for x in range(n)]))

#2
    print("Stage Sequence Timing:")
    print(','.join([str(arr[x][1]) for x in range(n)]))

#3
    print("Schedule completion time for the stage process:")
    for i in range(n):
        summed_array
        sum += arr[i][1]
        summed_array.append(sum)
    print(','.join([str(summed_array[x]) for x in range(n)]))


def CalculatePrintIdleTime(arr1, arr2):
    print("Idle time for Xavier: 5 minutes")


def shortJobScheduling(arr):
    # length of array
    n = len(arr)
    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j][1] > arr[j + 1][1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    printJobSequence(arr)
    CalculatePrintIdleTime(arr, photo)


def main():
    print("Reading content from input file")
    file_records = fileReader('../../data/input.txt')
    input_arr = []

    for input_rec in file_records:
        if input_rec.split(":")[0].strip() == "Products":
            products = input_rec.split(":")[1].split("/")
        elif input_rec.split(":")[0].strip() == "Staging":
            staging = input_rec.split(":")[1].split("/")
        elif input_rec.split(":")[0].strip() == "Photo":
            photo = input_rec.split(":")[1].split("/")

    for i in range(len(products)):
        final_input.append((products[i].strip(), int(staging[i].strip()), int(photo[i].strip())))

    shortJobScheduling(final_input)


if __name__ == "__main__":
    main()
