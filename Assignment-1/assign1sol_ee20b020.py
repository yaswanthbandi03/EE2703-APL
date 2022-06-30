import sys                                        #importing the python sys module           

if(len(sys.argv)!=2):                             #there should be two command lines arguments needed to be given python code file and the clt.netlist file
    sys.exit('Invalid number of arguments')
else: 
    name = sys.argv[1]                            #storing the netlist file name that contains the circuit
    if (not name.endswith(".netlist")):
            print("Wrong file type!")                               
    with open(name, "r") as f:                        #opening the netlist file
        lines = f.readlines()                         
 
    
    
    #initialising the dictionary containing all the components of the circuit 
components = { "R":"resistor" , "C":"capacitor" , "L":"indictor" , "V":"voltage_source" , "I":"current_source" , "E":"vcvs" , "G":"vccs" , "H":"ccvs" , "F":"cccs"}

try:
    a = len(lines)                                #the number of lines in the given file
    q = 0                                
    for i in range(a):               
        if (lines[i] == ".circuit\n"):              #finding which line of the file .circuit is contained 
            b = i
            q = q+1
        elif (lines[i] == ".end\n"):                #finding which line of the file .end is contained
            c = i
            q = q+1
    if(q != 2):                                   #creating an error when either of the .circuit or the .end is not contained
        int("a") 
        
    #defining a new string which only contains the code between .circuit and .end as "cir"                                
    cir = lines[b+1:c]                            #slicing the line of the file which contains the actual circuit between .circuit and .end
    d = c-b-1
    token = [ ]                                   #defining token as an empty 1dimensional list
    print("The given circuit file contains the following components of the following values:\n")
    for i in range(d): 
        token.append([])                          #making the token as the 2dimensional 
        token[i].append("")
        q = 0
        r = len(cir[i])                           #the number of the elements in the each line of the actual circuit
        
    #creating each tokens as one word the (1st dimension of the token contains the words of the ith line and the 2nd dimension contains the words of the each line    
        for k in range(r):
            if(cir[i][k]!=" " and cir[i][k]!="#" and cir[i][k]!="\n" ):          
                token[i][q] = token[i][q] + cir[i][k]                             
            elif(cir[i][k] == "#" or cir[i][k] == "\n"):
                break
            else:
                if(cir[i][k+1]!=" " and cir[i][k+1]!="#" ):
                    token[i].append("")       
                    q = q+1
                    
    #printing the each line of the analyzed circuit using the dictionary of the components
        print("Line {} of defined circuit contains a {} between node{} and node{} of value {} \n".format(i,components[token[i][0][0]],token[i][1],token[i][2],token[i][3]))                         
                    
                    
    #printing the file in the reversed order
    print("Printing the file containing the circuit in the reverse order")
    for i in range(d):
        r = len(token[i])
        for j in range(r):
            print(token[d-i-1][r-j-1],end = " ")
        print()                                           #adding a new line to the and the after printing all the tokens in a paticular line
                
                                              
       #when the exception comes ie when the circuit does not contain the .circuit and the .end file it should give an error                                       
except Exception:                                  
    print("Invalid file") 
    print("The given file does not contain .circuit or .end")
