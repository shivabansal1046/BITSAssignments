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
def outputWriter(output_file, arr, elapse_time, idle_time):
    out = open(output_file, 'w')
    out.write("Product Sequence: " + ', '.join([str(x[0]) for x in arr]))
    out.write("\n")
    out.write("Total time to complete photoshoot: {0} minutes\n".format(elapse_time))
    out.write("Idle time for Xavier: {0} minutes".format(idle_time))

''' calculating photographer idle time and total elapse time'''

def calculateCompletionTime(input):
    idle_time, photoshoot_time, stage_time = 0, 0, 0
    for i in input:
        stage_time += i[1]
        temp_idle_time = stage_time - photoshoot_time
        if temp_idle_time > 0:
            photoshoot_time += i[2] + temp_idle_time
            idle_time += temp_idle_time
        else:
            photoshoot_time += i[2]
    return photoshoot_time, idle_time


# Added temporary inbuilt function to support sorting requiremetn
''' Need to remove this function once we have custom built function with merge sort'''
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

    return arr

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



    ''' As per Greedy approach, sorting input data based on staging time
        so that xavier can start photoshoot as soon as possible 
        and idle time can be reduced which will eventually 
        reduce overall photoshoot time
    '''
    #final_input = sortInbuilt(final_input, 1, reverseOrder = False)
    final_input = sortJobScheduling(final_input)

    photoshoot_time, idle_time = calculateCompletionTime(final_input)
    outputWriter("../../data/outputPS7.txt", final_input, photoshoot_time, idle_time)

if __name__ == "__main__":
    main()