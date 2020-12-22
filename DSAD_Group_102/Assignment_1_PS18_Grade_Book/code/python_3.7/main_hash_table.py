dep_list = []

class student_info:
    def __init__(self, student_id, cgpa):
        self.student_id = student_id
        self.cgpa = cgpa
def fileReader(path):
    inputFile = open(path, 'r')
    return inputFile

def initializeHash(size, obj):
    return  HashTable(size)

def insertStudentRec(StudentHashRecords, studentId, CGPA):
    StudentHashRecords.add(student_info(studentId, studentId))

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

        self.table = table
        self.size = int(self.size * size_fraction)

def main():

    student_hash_table = initializeHash(100, student_info)
    file_records = fileReader('../../data/200_List.txt')
    for input in file_records:
        student = input.split("\\")
        insertStudentRec(student_hash_table, student[0], student[1])


    for i in student_hash_table.table:
        if(i != None):
            print(i.student_id, i.cgpa)
    print(len(student_hash_table.table))
    destroyHash(student_hash_table)
    print(len(student_hash_table.table), student_hash_table.size, student_hash_table.fill_counter)
if __name__ == "__main__":
    main()




