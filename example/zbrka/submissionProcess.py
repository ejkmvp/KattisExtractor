#processFrame is given the integer mapped to from each frame.
#Here, you will write a function to reverse this mapping.
#the output of this function is ultimately appended to a final output list
def processFrame(value):
    #example - zbrka
    #values should be in the range from 0 to 11 inclusive
    if value == 10:
        return " "
    if value == 11:
        return "END"
    return str(value)
