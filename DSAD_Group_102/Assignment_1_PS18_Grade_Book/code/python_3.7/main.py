class StudentRecord:

    def __init__(self, student_id, cgpa):
        self.studentHash = calculateHash(student_id)
        self.studentId = student_id
        self.cgpa = float(cgpa)

departments = ('CSE', 'MEC', 'ARC', 'ECE')

'''creates an empty hash table and points to null'''
def initializeHash(size) -> []:
    return [None]*size

maxCGPAHashTable = initializeHash(200)

def fileReader(StudentHashRecords, path):
    inputFile = open(path, 'r')

    for input in inputFile:
        student = input.split("\\")
        insertStudentRec(StudentHashRecords, student[0], student[1])



'''calculates the hash of given input'''
def calculateHash(input):

    year = int(input[0:4]) % 100
    dept = departments.index(input[4:7])
    rollNum = input[7:]
    hashedVal = str(year) + str(dept) + rollNum

    return int(hashedVal)

'''This function inserts the student id and corresponding CPGA into the hash table.'''
def insertStudentRec(StudentHashRecords, studentId, CGPA):

    StudentHashRecords.append(StudentRecord(studentId, CGPA))

def calcMaxCGPA(StudentHashRecords):

    for record in StudentHashRecords:

        hashVal = calculateHash(record.studentId[0:7])

        try:
            if (maxCGPAHashTable[hashVal] < record.cgpa):
                maxCGPAHashTable[hashVal] = record.cgpa
        except:
            maxCGPAHashTable[hashVal] = record.cgpa


'''This function prints the list of all students who have graduated and topped their department in their year of graduation'''
def hallOfFame(StudentHashRecords):
    toppers = []
    for record in StudentHashRecords:
        if (record.cgpa == maxCGPAHashTable[calculateHash(record.studentId[0:7])]):
            toppers.append((record.studentId, record.cgpa))
    return toppers

'''This function prints the list of all students who have a CGPA within the given range and have graduated in the last 5 years
(Only students who graduated should be considered '''
def newCourseList(StudentHashRecords, CGPAFrom, CPGATo):
    elegibleStudents = []
    for record in StudentHashRecords:
        if(record.cgpa >= CGPAFrom and record.cgpa <= CPGATo):
            elegibleStudents.append(record)
    return elegibleStudents


'''This function prints the list of all departments followed by the maximum CGPA and average CGPA of all students in that department'''

def depAvg(StudentHashRecords):
    output = []

    j = 0
    for i in range(4):
        max_tempArr = []
        avg_tempArr = []
        for cgpa in maxCGPAHashTable:

            if(cgpa != None and j%10 == i):
                max_tempArr.append(cgpa)
            j = j + 1


        for record in StudentHashRecords:
            if (int(record.studentHash/10000)%10 == i):
                avg_tempArr.append(record.cgpa)


        output.append((max(max_tempArr), sum(avg_tempArr) / len(avg_tempArr)))



    return (output)



'''This function destroys all the entries inside hash table. 
This is a clean-up code'''
def destroyHash(inputHash):
    inputHash = []


def main():


    StudentHashRecords = []


    fileReader(StudentHashRecords, '../../data/200_List.txt')
    calcMaxCGPA(StudentHashRecords)



    print("########### Hall of fame ##########")

    hall_Of_fame = hallOfFame(StudentHashRecords)

    print(len(hall_Of_fame))
    for h in hall_Of_fame:
        print(h)
    print("########### elegible students for new courses ##########")



    eligible_students = newCourseList(StudentHashRecords, 3, 3.5)

    for i in eligible_students:
        print(i.studentId, i.cgpa)


    print("########### maximum of hash ##########")

    dep_avg = depAvg(StudentHashRecords)

    j = 0
    for i in dep_avg:

        print(departments[j] , i[0], i[1])
        j = j + 1



    destroyHash(maxCGPAHashTable)



if __name__ == "__main__":
    main()
