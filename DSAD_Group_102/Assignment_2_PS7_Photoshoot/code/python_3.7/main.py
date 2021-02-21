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

''' calculating photographer idle time and total elapse time'''

def calculateCompletionTime(input):
    idle_time, photoshoot_time, stage_time = 0, 0, 0
    '''
    Products: A / B / C / D / E / F
    Staging: 20 / 30 / 45 / 60 / 20 / 10
    Photo: 30 / 30 / 15 / 20 / 40 / 60
    '''

    for i in input:
        stage_time += i[1]
        temp_idle_time = stage_time - photoshoot_time
        if temp_idle_time > 0:
            photoshoot_time += i[2] + temp_idle_time
            idle_time += temp_idle_time
        else:
            photoshoot_time += i[2]
        #print("product name:{0}, idle time :{1} , photoshootime :{2} and stagetime:{3}".format(i[0], idle_time, photoshoot_time, stage_time))

    return photoshoot_time, idle_time



# Added temporary inbuilt function to support sorting requiremetn

def sortInbuilt(input, key, reverseOrder=False):
    def sort1(input):
        return input[1]

    def sort2(input):
        return input[2]
    if key == 1:
        input.sort(key=sort1, reverse=reverseOrder)
    else:
        input.sort(key=sort2)
    return input

# sorting input data based on the input column
def sortJobScheduling(arr):
    # length of array
    n = len(arr)
    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j][1] > arr[j + 1][1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    printJobSequence(arr)
    CalculatePrintIdleTime(arr, photo)

## main function to run the code
def main():
    print("Reading content from input file")
    #please change the path based on your input location
    file_records = fileReader('../../data/input.txt')
    input_arr = []
    final_input = []
    print("parsing input data file")
    for input_rec in file_records:
        if input_rec.split(":")[0].strip() == "Products":
            products = input_rec.split(":")[1].split("/")
        elif input_rec.split(":")[0].strip() == "Staging":
            staging = input_rec.split(":")[1].split("/")
        elif input_rec.split(":")[0].strip() == "Photo":
            photo = input_rec.split(":")[1].split("/")

    for i in range(len(products)):
        final_input.append((products[i].strip(), int(staging[i].strip()), int(photo[i].strip())))


    for i in final_input:
        print(i)

    photoshoot_time, idle_time = calculateCompletionTime(final_input)
    print("elapse and idle time on raw input:")
    print(photoshoot_time, idle_time)

    # sort input data based on staging time
    final_input = sortInbuilt(final_input, 1, reverseOrder = False)

    print("print Sorted input")
    for i in final_input:
        print(i)

    print("elapse and idle time on sorted stage input:")
    photoshoot_time, idle_time = calculateCompletionTime(final_input)
    print(photoshoot_time, idle_time)

if __name__ == "__main__":
    main()