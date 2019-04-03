#### General functions ####

# Read each line of file
def read_file_each_line():
    try:
        readLine = []
        file = open('test.txt')
        readLine = file.read().split("\n")
        file.close()
        print(readLine)
    except:
        print("It does not work!")
