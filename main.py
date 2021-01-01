# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


#def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    #print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
    #print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

class transformer:
    def __init__(self):
        pass

    def get_transformer(Un, Sn, Pk, Uk, Io, Po, ratio):  # Un,Sn,Pk,Uk%,Io%,Po,ratio
        pass

Topology=[[]]

class BUS_PQ:
    def __init__(self,P,Q,position):
        pass

class BUS_PV:
    def __init__(self,P,V,position):
        pass

class BUS_Vtheta:
    def __init__(self,V,theta,position):
        pass

#type 1:cu+n=1+S=300mm2
def get_wire(type,Dm,r,length):#(材料，面积，股数)，Dm，r,长度,
    pass

def get_transformer(Un,Sn,Pk,Uk,Io,Po,ratio):#Un,Sn,Pk,Uk%,Io%,Po,ratio
    pass

def transform(Topology,*args ):#变压器的权重为负，
    pass

def get_admittance_matrix(Topology):
    pass

def calculate_A(admittance_matrix,*args):
    pass

def calculate_Y(*args):
    pass

def Newton_iteraion(Y, A, X, accuracy):  # Y=AX
    pass

#def calculate_S():
    pass
