dep_list = []
current_year = 2020
class student_info:
    def __init__(self, student_id, cgpa):
        self.student_id = student_id
        self.cgpa = cgpa
def fileReader(path):
    inputFile = open(path, 'r')
    return inputFile

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

def initializeHash(size, obj):
    return  HashTable(size)

def insertStudentRec(StudentHashRecords, studentId, CGPA):
    StudentHashRecords.add(student_info(studentId, CGPA))

def destroyHash(StudentHashRecords):
    StudentHashRecords.table = []
    StudentHashRecords.size = 0
    StudentHashRecords.fill_counter = 0

class HashTable:

    def __init__(self, size):
        self.size = size
        self.table = [None]*size
        self.fill_counter = 0

    def calculateHash(self, key):
        year = int(key[0:4]) % 100
        department = key[4:7]
        rollNum = key[7:]
        try:
            dept = dep_list.index(department)
        except:
            dept = len(dep_list)
            dep_list.append(department)
        hashVal = ((year % 100)*10 + dept)*10000 + int(rollNum)
        return hashVal

    def add(self, student):

        ### check hash size in case hash is filled above threshold i.e 0.9 then increase by given fraction i.e. 1.5

        if(self.fill_counter > self.size * 0.9):
            print("resizing the hash table as it has reached threshold value i.e {fill_counter}".format(fill_counter = self.fill_counter))
            self.resizeHash(1.5)
            print("New Hash table size {size}".format(size = self.size))

        id_hash = self.calculateHash(student.student_id)
        index_val = id_hash % self.size


        if(self.table[index_val] == None):
            self.table[index_val] = student
            self.fill_counter = self.fill_counter + 1
        else:
            while(self.table[index_val] != None):
                if(index_val == len(self.table)-1 ):
                    index_val = 0
                else:
                    index_val = index_val + 1
                if(self.table[index_val] == None):
                    self.table[index_val] = student
                    self.fill_counter = self.fill_counter + 1
                    break

    def resizeHash(self, size_fraction= 2):

        table = [None]* int(self.size*size_fraction)
        i = 0
        for entry in self.table:
            table[i] = entry
            i = i + 1

        self.table = table
        self.size = int(self.size * size_fraction)

def hallOfFame(StudentHashRecords):
    max_cgpa = [None]*100
    topper = []
    for record in StudentHashRecords:
        if(record != None and (int(record.student_id[:4])) < (current_year - 5)):
            year = int(record.student_id[3:4])
            dep = int(dep_list.index(record.student_id[4:7]))
            dep_index = year*10 + dep
            if (max_cgpa[dep_index] != None):
                if (max_cgpa[dep_index] < record.cgpa):
                    max_cgpa[dep_index] = record.cgpa
            else:
                max_cgpa[dep_index] = record.cgpa

    for record in StudentHashRecords:
        if(record != None and (int(record.student_id[:4])) < (current_year - 5)):
            year = int(record.student_id[3:4])
            dep = int(dep_list.index(record.student_id[4:7]))
            dep_index = year*10 + dep
            if (max_cgpa[dep_index] == record.cgpa):
                    topper.append([record.student_id, record.cgpa])
    return topper


### hash table query function #########

# def newCourseList(StudentHashRecords, CGPAFrom, CPGATo): This function prints the list of all students who have
# a CGPA within the given range and have graduated in the last 5 years (Only students who graduated should be
# considered. Calculate the applicable year range accordingly). The input CGPAs can be read from the file
# promptsPS18.txt. The input can be identified with the tag mentioned below courseOffer: 3.5 : 4.0 Print the
# eligible students for a new course whose CGPA is between the range

def newCourseList(student_hash_table, cgpa_from, cgpa_to):
    qualified_students = []
    # get the qualified students based on their CGPA
    for rec in student_hash_table.table:
        if not rec is None:
            if (
                    (int(rec.student_id[:4])) < (current_year - 5) and
                    cgpa_from <= float(rec.cgpa) <= cgpa_to
            ):
                qualified_students.append((rec.student_id, rec.cgpa))
    return qualified_students

# def depAvg(StudentHashRecords): This function prints the list of all departments followed by the maximum CGPA and
# average CGPA of all students in that department. The output should be captured in outputPS18.txt following format
# CSE: max: 3.5, avg: 3.4
def depAvg(student_hash_table):
    final_dep_return_array = [None] * len(dep_list)
    dep_max_arr = [float(0)] * len(dep_list)
    dep_avg_arr = [float(0)] * len(dep_list)
    dep_each_count = [float(0)] * len(dep_list)

    # loop over the students to count and get the cgpas of students
    # based on their departments
    for student_record in student_hash_table.table:
        if not student_record is None:
            # Get the department and cgpa from the hashtable collection
            department = student_record.student_id[4:7]

            dep_avg_arr[dep_list.index(department)] += float(student_record.cgpa)
            dep_each_count[dep_list.index(department)] += 1

            # cgpa for the department
            if dep_max_arr[dep_list.index(department)] < float(student_record.cgpa):
                cgpa = float(student_record.cgpa)
                dep_max_arr[dep_list.index(department)] = float(student_record.cgpa)

    for count_num in range(len(dep_max_arr)):
        final_dep_return_array[count_num] = dep_list[count_num], dep_max_arr[count_num], round(
            dep_avg_arr[count_num] / dep_each_count[count_num], 2)
    return final_dep_return_array

def main():

    print("initializing hash table")
    student_hash_table = initializeHash(100, student_info)
    print("Reading content from input file")
    file_records = fileReader('inputPS18.txt')
    print("building hash table")
    for input in file_records:
        student = input.split("\\")
        insertStudentRec(student_hash_table, student[0].strip(), student[1].strip())

    print("reading input params file")

    file_records = fileReader("promptsPS18.txt")
    input_params = []
    for input in file_records:
        if (len(input) > 0):
            input_params.append(input.split(":"))


    hall_of_fame_param = input_params[0][1].strip()
    cgpa_param = (input_params[1][1].strip(),input_params[1][2].strip())

    print("hall of fame input:" + hall_of_fame_param)
    global current_year
    if(hall_of_fame_param != ""):
        current_year = int(hall_of_fame_param)
    print("current_year", current_year)
    print("new course to offer cgpa range: " +cgpa_param[0], cgpa_param[1])

    print("need to add hall of fame function call")

    hall_of_dame = hallOfFame(student_hash_table.table)

    print("calling new course list candidates function")
    new_course_list = newCourseList(student_hash_table, float(cgpa_param[0]), float(cgpa_param[1]))

    print("calling new department cgpa function")

    dep_avg = depAvg(student_hash_table)

    print("writer funtion to write output as per the requirement")

    outputWriter("outputPS18.txt", [hall_of_dame, [cgpa_param[0], cgpa_param[1]], new_course_list , dep_avg])
    
    print("destroying hash table as part of clean up")
    destroyHash(student_hash_table)
if __name__ == "__main__":
    main()