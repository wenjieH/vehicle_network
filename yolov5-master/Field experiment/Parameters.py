CommunicationRange = 100
Max_layer = 10
MaxValue = float('inf')

def Distance(x1, x2, y1, y2):
    return ((x1-x2)**2+(y1-y2)**2)**(1/2)