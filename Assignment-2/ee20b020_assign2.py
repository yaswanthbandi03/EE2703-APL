import sys
import numpy as np                          


class element_def():                         #class for the elements
    def __init__(self,line):
        self.line = line
        self.tokens = self.line.split()
        self.name = element_type(self.tokens[0])
        self.from_node = self.tokens[1]
        self.to_node = self.tokens[2]


        if len(self.tokens) == 5:
            self.type = 'dc'
            self.value = float(self.tokens[4])

        elif len(self.tokens) == 6:
            self.type = 'ac'
            Vm = float(self.tokens[4])/2
            phase = float(self.tokens[5])
            real = Vm * np.cos(phase)
            imag = Vm * np.sin(phase)
            self.value = complex(real,imag)

        else:
            self.type = 'dc-only'
            self.value = float(self.tokens[3])



def element_type(token):            #Gets the element name   
    if token[0] == 'R':
        return 'resistor'
    elif token[0] == 'L':
        return 'inductor'
    elif token[0] == 'C':
        return 'capacitor'
    elif token[0] == 'V':
        return 'independent voltage source'
    elif token[0] == 'I':
        return 'independent current source'


def freq(lines):                    #Returns the frequency of the source
    frequency = 0
    for line in lines:
        if line[:3] == '.ac':
            frequency = float(line.split()[2])
    return frequency
def get_key(d,value): #Gets the corresponding key for a value in the dictionary
    for key in d.keys():
        if d[key] == value :
            return key

def node_mappedping(circuit): #Returns a dictionary of nodes from the circuit definition.
    d = {"GND" : 0} 
    nodes = [element_def(line).from_node for line in circuit]
    nodes += [element_def(line).to_node for line in circuit]
    nodes = list(set(nodes)) #all distinct nodes
    nodes.remove("GND")
    nodes=sorted(nodes)
    nodes.append("GND")
    print(nodes)

    
    count = 1
    for node in nodes:
        if node != 'GND' :
            d[node] = count
            count += 1
    return d

def make_dict(circuit,element): #Makes a dictionary for each component of the particular type of element
    e=element
    d = {}
    ele_names = [element_def(line).tokens[0] for line in circuit if element_def(line).tokens[0][0]== e]
    for i, name in enumerate(ele_names):
        d[name] = i
    return d


def find_node(circuit, node_key, node_mapped): #Findices the lines and position ie from and to of the given node 
    indices = []
    for i in range(len(circuit)):
        for j in range(len(circuit[i].split())):
            if circuit[i].split()[j] in node_mapped.keys():
                if node_mapped[circuit[i].split()[j]] == node_key:
                    indices.append((i, j))

    return indices


def update_matrix(node_key): #Updates the M and b matrix for the given node
    indices = find_node(circuit, node_key, node_mapped)
    for ind in indices:
        #getting all the attributes of the element using the class definition
        element = element_def(circuit[ind[0]])
        ele_name = circuit[ind[0]].split()[0]
        #resistors
        if ele_name[0] == 'R':
            if ind[1] == 1: #from_node
                adj_key = node_mapped[element.to_node]
                M[node_key, node_key] += 1/(element.value)
                M[node_key, adj_key] -= 1/(element.value)
                    
            if ind[1] == 2 : #to_node
                adj_key = node_mapped[element.from_node]
                M[node_key, node_key] += 1/(element.value)
                M[node_key, adj_key] -= 1/(element.value)      
        #inductors
        if ele_name[0] == 'L' :
            try:
                if ind[1]== 1:
                    adj_key = node_mapped[element.to_node]
                    M[node_key, node_key] -= complex(0,1/(2 * np.pi * frequency * element.value))
                    M[node_key, adj_key] += complex(0,1/(2 * np.pi * frequency * element.value))
                if ind[1] == 2 :
                    adj_key = node_mapped[element.from_node]
                    M[node_key, node_key] -= complex(0,1/(2 * np.pi * frequency * element.value))
                    M[node_key, adj_key] += complex(0,1/(2 * np.pi * frequency * element.value))
            except ZeroDivisionError:               #in dc case as frequency = 0
                idx = ind_d[ele_name]
                if ind[1]== 1:
                    adj_key = node_mapped[element.to_node]
                    M[node_key, n + p + idx] += 1 
                    M[n + p + idx, node_key] -= 1
                    b[n + p + idx] = 0
                if ind[1]== 2:
                    M[node_key, n + p + idx] -= 1
                    M[n + p + idx, node_key] += 1
                    b[n + p + idx] = 0
        #capacitors
        if ele_name[0] == 'C' :
            if ind[1]== 1: #from_node
                adj_key = node_mapped[element.to_node]
                M[node_key, node_key] += complex(0, 2 * np.pi * frequency * (element.value))
                M[node_key, adj_key] -= complex(0, 2 * np.pi * frequency * (element.value))
            if ind[1] == 2 :#to_node
                adj_key = node_mapped[element.from_node]
                M[node_key, node_key] += complex(0, 2 * np.pi * frequency * (element.value))
                M[node_key, adj_key] -= complex(0, 2 * np.pi * frequency * (element.value))
        #independent voltage source
        if ele_name[0] == 'V' :
            index = volt_d[ele_name]
            if ind[1]== 1:
                adj_key = node_mapped[element.to_node]
                M[node_key,n+index] += 1
                M[n+index,node_key] -= 1
                b[n+index] = element.value
            if ind[1] == 2 :
                adj_key = node_mapped[element.from_node]
                M[node_key,n+index] -= 1
                M[n+index,node_key] +=1
                b[n+index] = element.value
        #independent current source
        if ele_name[0] == 'I' :
            if ind[1]== 1:
                b[node_key] -= element.value
            if ind[1] == 2 :
                b[node_key] += element.value
    
#main function starts from here
if len(sys.argv) != 2:            # The program will throw in an error if there isn't exactly 2 arguments in the commandline.                                           
    print("Please provide the correct 2 arguments in the commandline.") 
    exit()
try:
    with open(sys.argv[1]) as f:
        lines = f.readlines()
        CIRCUIT = ".circuit"
        END = ".end"
        AC = '.ac'
        frequency = freq(lines)  #frequency of the source, currently supports only single frequency circuits
        start = 0
        end = 1
        for line in lines:              # extracting circuit definition start and end lines
            if CIRCUIT == line[:len(CIRCUIT)]:
                start = lines.index(line)
            elif END == line[:len(END)]:
                end = lines.index(line)
                break
        if start >= end:                # validating circuit block
            print('Invalid circuit definition')
            exit(0)

        
        circuit = []
        for line in [' '.join(line.split('#')[0].split()) for line in lines[start+1:end]]:
            circuit.append(line)                
        #1. preprocessing of the file done

        node_mapped = node_mappedping(circuit)
        #2. table of distinct nodes present in the circuit
        #numbers assigned to the nodes correspond to the rows of the incidence matirx

        volt_d = make_dict(circuit, "V")
        ind_d = make_dict(circuit,'L')
        
        p = len([i for i in range(len(circuit)) if circuit[i].split()[0][0] == 'V'])
        n = len(node_mapped)
        dim = n + p   
        #dimension of M if source is AC.
        #if source is DC, we need to add inductors also

        if frequency == 0: #dc signal, l acts as closed wire in steady state.
            M = np.zeros((dim+len(ind_d),dim+len(ind_d)),dtype=np.complex)
            b = np.zeros(dim+len(ind_d),dtype=np.complex)
        else:
            M = np.zeros((dim,dim),dtype=np.complex)
            b = np.zeros(dim,dtype=np.complex)

        for i in range(len(node_mapped)): #update matrix for the ith node
            update_matrix(i)
        #as Vgnd = 0
        M[0] = 0
        M[0,0] =1

        #M and b arrays are constructed
        print('The node dictionary is :',node_mapped)
        print('M = :\n',M)
        print('b = :\n',b)
    
        try:
            x = np.linalg.solve(M,b)   #solving Mx = b  
        except Exception:
            print('The incidence matrix cannot be inverted as it is singular.')
            sys.exit()

        print('Voltage convention : From node is at a lower potential and To node is at higher voltage')     
        
        for i in range(n):
            print("node {} voltage is {}".format(get_key(node_mapped,i),round(x[i],3)))
        for j in range(p):
            print('Current through source {} is {}'.format(get_key(volt_d,j),x[n+j]))
        if frequency == 0:
            for i in range(len(ind_d)):
                print("Current through inductor {} is {}".format(get_key(ind_d,i),x[n+p+i]))

except IOError:
    print('Invalid file')
    exit()