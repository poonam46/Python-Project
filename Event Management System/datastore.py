class DataStore:
    def __init__(self):
        self.root = "Core Python/Project/Event Management System/Data/"

    def addData(self, filename, obj):
        str_obj = str(obj)

        with open(self.root + filename + ".txt" , 'a') as fp:
            fp.write(str_obj + '\n')
        #return 'Data Added Successfully'
    
    def getFilePointer(self, file_name):
        fp = open(self.root + file_name + ".txt" , 'r' ) 
        return fp


    def updateData(self, file_name, list):
        with open(self.root + file_name + ".txt" , 'w' ) as fp:
            for emp in list:
                fp.write(emp)
        return 'Data updated successfully...'

    def deleteData(self,file_name, list):
         with open(self.root + file_name + ".txt" , 'w' ) as fp:
            for emp in list:
                fp.write(emp)
         return 'Data deleted successfully...'