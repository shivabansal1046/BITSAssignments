""" Please configure the Input and Output file path of the file here """
output_file_path = "outputPS7.txt"
input_file_path = "input.txt"


# """ Function to read the file and throw the exception based on the result """
def fileReader(path):
    try:
        inputFile = open(path, 'r')
        return inputFile
    except(FileNotFoundError, IOError):
        print("file not found, exiting the program !!!")
        exit(1)


# This function is use for to print the job sequence
# Sample OutPut
# Product Sequence: F, A, E, B, C, D
# Total time to complete photoshoot: 205 minutes
# Idle time for Xavier: 10 minutes

def outputWriter(output_file_path, arr, elapse_time, idle_time):
    out = open(output_file_path, 'w')
    out.write("Product Sequence: " + ', '.join([str(x[0]) for x in arr]))
    out.write("\n")
    out.write("Total time to complete photoshoot: {0} minutes\n".format(elapse_time))
    out.write("Idle time for Xavier: {0} minutes".format(idle_time))

    print("Output successfully written in the output file located at: ", output_file_path)


# """ calculating photographer idle time and total elapse time """
def calculateCompletionTime(input_data):
    idle_time, photoshoot_time, stage_time = 0, 0, 0
    for i in input_data:
        stage_time += i[1]
        temp_idle_time = stage_time - photoshoot_time
        if temp_idle_time > 0:
            photoshoot_time += i[2] + temp_idle_time
            idle_time += temp_idle_time
        else:
            photoshoot_time += i[2]

    return photoshoot_time, idle_time


# Added temporary inbuilt function to support sorting requiremetn
""" Need to remove this function once we have custom built function with merge sort """


# """ sorting input data based on the input column """
def sortJobScheduling(arr, c_n):
    # length of array
    n = len(arr)
    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j][c_n] > arr[j + 1][c_n]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


# main function to run the code
def main():
    print("Reading content from the configured input file located at: ", input_file_path)

    # Sample Input:
    # Products: A / B / C / D / E / F
    # Staging: 20 / 30 / 45 / 60 / 20 / 10
    # Photo: 30 / 30 / 15 / 20 / 40 / 60

    # """ please change the path based on your input location """
    file_records = fileReader(input_file_path)
    final_input = []
    products = []
    staging = []
    photo = []

    print("parsing the input data file successfully")
    for input_rec in file_records:
        if input_rec.split(":")[0].strip().lower() == "products":
            products = input_rec.split(":")[1].split("/")
        elif input_rec.split(":")[0].strip().lower() == "staging":
            staging = input_rec.split(":")[1].split("/")
        elif input_rec.split(":")[0].strip().lower() == "photo":
            photo = input_rec.split(":")[1].split("/")

    for i in range(len(products)):
        final_input.append((products[i].strip(), int(staging[i].strip()), int(photo[i].strip())))

    """ As per Greedy approach, sorting input data based on staging time
        so that xavier can start photoshoot as soon as possible and idle time can be reduced which will eventually 
        reduce overall photoshoot time/
    """

    # """ Short teh input data based on the staging column which is on the middle """
    final_input = sortJobScheduling(final_input, 1)

    # """ Invoke function to calculate photoshoot_time and idle_time """
    photoshoot_time, idle_time = calculateCompletionTime(final_input)

    # """ invoke the common function to print the output """
    outputWriter(output_file_path, final_input, photoshoot_time, idle_time)


if __name__ == "__main__":
    main()