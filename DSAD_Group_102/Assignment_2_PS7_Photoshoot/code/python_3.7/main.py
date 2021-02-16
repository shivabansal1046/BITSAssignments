dep_list = []
current_year = 2020
class student_info:
    def __init__(self, student_id, cgpa):
        self.student_id = student_id
        self.cgpa = cgpa
def fileReader(path):
    try:
        inputFile = open(path, 'r')
        return inputFile
    except(FileNotFoundError, IOError):
        print("file not found, exiting the program !!!")
        exit(1)

def outputWriter(output_file, content):
    out = open(output_file, 'w')
    print("writing hall of fame")
    out.write("---------- hall of fame ----------\n\n")
    out.write("Total eligible students: {students}".format(students = len(content[0])))
    out.write("\n\n")
    out.write("Qualified students:\n\n")
    for record in content[0]:
        out.write(record[0] +" / " + record[1] + "\n")
    out.write("------------------------------\n\n")
    out.write("\n---------- new course candidates ----------\n\n")
    out.write("Input: {cgpa_from} to {cgpa_to}".format(cgpa_from = content[1][0], cgpa_to = content[1][1]))
    out.write("\n\n")
    out.write("Total eligible students: {students}".format(students = len(content[2])))
    out.write("\n\n")
    out.write("Qualified students:\n\n")
    for record in content[2]:
        out.write(record[0] +" / " + record[1] + "\n")
    out.write("------------------------------\n\n")
    out.write("---------- department CGPA ----------\n\n")
    for record in content[3]:
        out.write(record[0] +": max: " + str(record[1]) + ", avg: " + str(record[2]) + "\n")

    out.close()


def main():

    print("Reading content from input file")
    file_records = fileReader('../../data/input.txt')
    input_arr = []
    products = []
    staging = []
    photo = []

    for input in file_records:
        if (input.split(":")[0].strip() == "Products"):
            products = input.split(":")[1].split("/")
        elif(input.split(":")[0].strip() == "Staging"):
            staging = input.split(":")[1].split("/")
        elif(input.split(":")[0].strip() == "Photo"):
            photo = input.split(":")[1].split("/")

    final_input = []
    for i in range(len(products)):
        final_input.append((products[i].strip(), staging[i].strip(), photo[i].strip()))

    for i in final_input:
        print(i)

if __name__ == "__main__":
    main()