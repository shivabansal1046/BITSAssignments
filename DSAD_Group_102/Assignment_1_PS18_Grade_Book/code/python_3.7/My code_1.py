
#f = open ("inputPS18.txt", "r")


# Creating Hashtable as
# a nested list.
HashTable = [[] for _ in range(200)]

ID=list()

CGPA=list()
# Hashing Function to return
# key for every value.


def Hashing(str):
    return hash(str)

#% len(HashTable)


# Insert Function to add
# values to the hash table

#def insert(HashTable, keyvalue , cgpa):


Student_ID ={}  
Temp_ID ={}
ARC_ID ={}
CSE_ID = {}
ECE_ID = {}
MEC_ID = {}
HallofFame={}
Year =[]
def get_key(val):
    for key, value in Student_ID.items():
         if val == value:
             return key

    return "key doesn't exist"

def get_value(key2):
    for key, value in Student_ID.items():
         if key2 == key:
             return value

    return "key doesn't exist"


with open("inputPS18.txt", "r") as fp:



   line = fp.readline()
   cnt = 1
   while line:
       #print("Line {}: {}".format(cnt, line.strip()))
       line = fp.readline()
       ID = line[0:11]

       #print(ID)

       Mark = line[22:25]
       #CGPA = float(Mark)
       Student_ID[ID]=Mark
       #HashTable[ID]=Hashing(ID)
       #print(CGPA)
       cnt += 1

#print(Student_ID)
#print(get_key('5.0'))
#print(get_key('4.3'))


#print(get_value('2020MEC6544'))
#print(get_value('2013ARC1051'))
Check_Year = 2010

for key in Student_ID.keys() :
   
    
    year = key[0:4]
    dept = key[4:7]
    roll = key[7:]

    if key[0:4] == str(Check_Year):

        if key[4:7] == "ARC" and key[0:4] == str(Check_Year):

            S_ID = key

            S_CGPA = get_value(key)

            ARC_ID[S_ID] = S_CGPA

            Temp_S = sorted(ARC_ID.items(), key=lambda x: x[1])

            #print(ARC_ID)

            Temp_S.reverse()

            print(Temp_S)

        elif key[4:7] == "MEC" and key[0:4] == str(Check_Year):
             
            S1_ID = key

            S1_CGPA = get_value(key)

            MEC_ID[S1_ID] = S1_CGPA

            Temp_S1 = sorted(MEC_ID.items(), key=lambda x: x[1])

            #print(MEC_ID)

            Temp_S1.reverse()

            #print(Temp_S1)   
        

        elif key[4:7] == "CSE" and key[0:4] == str(Check_Year):

            S2_ID = key

            S2_CGPA = get_value(key)

            CSE_ID[S2_ID] = S2_CGPA

            Temp_S2 = sorted(CSE_ID.items(), key=lambda x: x[1])

            #print(CSE_ID)

            Temp_S2.reverse()

            #print(Temp_S2)

        elif key[4:7] == "ECE" and key[0:4] == str(Check_Year):

            S3_ID = key

            S3_CGPA = get_value(key)

            ECE_ID[S3_ID] = S3_CGPA

            Temp_S3 = sorted(ECE_ID.items(), key=lambda x: x[1])

            #print(ECE_ID)

            Temp_S3.reverse()

            #print(Temp_S3)

    else:

            Check_Year = Check_Year +1
        






print(HallofFame)
           
   

#lst1 = sorted(Student_ID.items(), key= lambda x:x[0])



#lst2 = sorted(Student_ID.items(), key= lambda x:x[1])

#print(lst1)
#print(lst2)
