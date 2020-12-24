dep_list = []
output_file = '../../data/ashish_out_out_data.txt'
current_year = 2020
class student_info:
    def __init__(self, student_id, cgpa):
        self.student_id = student_id
        self.cgpa = cgpa
def fileReader(path):
    inputFile = open(path, 'r')
    return inputFile

def outputWriter(output_file):
    with open(output_file, 'a+') as of:
        of.write("need to write as per output standard once all the functions provided")

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

### hash table query function #########

# def newCourseList(StudentHashRecords, CGPAFrom, CPGATo): This function prints the list of all students who have
# a CGPA within the given range and have graduated in the last 5 years (Only students who graduated should be
# considered. Calculate the applicable year range accordingly). The input CGPAs can be read from the file
# promptsPS18.txt. The input can be identified with the tag mentioned below courseOffer: 3.5 : 4.0 Print the
# eligible students for a new course whose CGPA is between the range
def newCourseList(student_hash_table, cgpa_from, cgpa_to):
    qualified_students = []
    # get the qualified students based on their CGPA
    for student_count in range(len(student_hash_table.table)):
        if not student_hash_table.table[student_count] is None:
            if (

                    (int(student_hash_table.table[student_count].student_id[:4]) + 4) >= (current_year - 5) and
                    cgpa_from <= float(student_hash_table.table[student_count].cgpa) <= cgpa_to
            ):
                qualified_students.append(student_hash_table.table[student_count])

    # print the qualified students
    with open(output_file, 'a+') as of:
        of.write('---------- new course candidates ----------\n')
        of.write('Input: %s to %s\n' % (str(cgpa_from), str(cgpa_to)))
        of.write('Total eligible students: %d\n' % len(qualified_students))
        of.write('Qualified students:\n')
        for student_qualified_count in range(len(qualified_students)):
            if not qualified_students[student_qualified_count] is None:
                qual_student_id = qualified_students[student_qualified_count].student_id
                qual_cgpa = qualified_students[student_qualified_count].cgpa
                of.write('%s / %s\n' % (qual_student_id, str(qual_cgpa)))


# def depAvg(StudentHashRecords): This function prints the list of all departments followed by the maximum CGPA and
# average CGPA of all students in that department. The output should be captured in outputPS18.txt following format
# CSE: max: 3.5, avg: 3.4
def depAvg(student_hash_table):
    cse_count, mec_count, ece_count, arc_count = 0, 0, 0, 0
    cse_max, mec_max, ece_max, arc_max = 0, 0, 0, 0
    cse_sum_dep, mec_sum_dep, ece_sum_dep, arc_sum_dep = 0, 0, 0, 0
    cse_avg, mec_avg, ece_avg, arc_avg = 0, 0, 0, 0

    # loop over the students to count and get the cgpas of students
    # based on their departments
    for student_count in range(len(student_hash_table.table)):
        if not student_hash_table.table[student_count] is None:
            department = student_hash_table.table[student_count].student_id[4:7]
            cgpa = float(student_hash_table.table[student_count].cgpa)
            if department == 'CSE':
                cse_count += 1
                cse_sum_dep += cgpa
            if cgpa > cse_max:
                cse_max = cgpa
            elif department == 'MEC':
                mec_count += 1
                mec_sum_dep += cgpa
            if cgpa > mec_max:
                mec_max = cgpa
            elif department == 'ECE':
                ece_count += 1
                ece_sum_dep += cgpa
            if cgpa > ece_max:
                ece_max = cgpa
            elif department == 'ARC':
                arc_count += 1
                arc_sum_dep += cgpa
            if cgpa > arc_max:
                arc_max = cgpa

    # average_values
    cse_avg = cse_sum_dep / cse_count if cse_count != 0 else 0
    mec_avg = mec_sum_dep / mec_count if mec_count != 0 else 0
    ece_avg = ece_sum_dep / ece_count if ece_count != 0 else 0
    arc_avg = arc_sum_dep / arc_count if arc_count != 0 else 0
    # CSE: max: 3.5, avg: 3.4

    # print the max and averages for each department
    with open(output_file, 'a+') as of:
        of.write('---------- department CGPA ----------\n')
        of.write('CSE: max: %s, avg: %s\n' %
                 (str(cse_max), str(round(cse_avg, 2))))
        of.write('MEC: max: %s, avg: %s\n' %
                 (str(mec_max), str(round(mec_avg, 2))))
        of.write('ECE: max: %s, avg: %s\n' %
                 (str(ece_max), str(round(ece_avg, 2))))
        of.write('ARC: max: %s, avg: %s\n' %
                 (str(arc_max), str(round(arc_avg, 2))))
        of.write('-------------------------------------\n')


def main():

    print("initializing hash table")
    student_hash_table = initializeHash(100, student_info)
    print("Reading content from input file")
    file_records = fileReader('../../data/inputPS18.txt')
    print("building hash table")
    for input in file_records:
        student = input.split("\\")
        insertStudentRec(student_hash_table, student[0].strip(), student[1].strip())

    print("reading input params file")

    file_records = fileReader("../../data/promptsPS18.txt")
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

    #hallOfFame(student_hash_table.table)

    print("calling new course list candidates function")
    newCourseList(student_hash_table, float(cgpa_param[0]), float(cgpa_param[1]))

    print("calling new department cgpa function")

    depAvg(student_hash_table)

    print("writer funtion to write output as per the requirement")

    outputWriter("../../outputPS18.txt")
    
    print("destroying hash table as part of clean up")
    destroyHash(student_hash_table)
if __name__ == "__main__":
    main()