frameNum = 4
crumbNum = 1
subsPerFrame = 2

#The above values get updated by extractor.py

def memError():
    [{} for i in range(10 ** 10)]
def wrongAns():
    print("meowasdf")
    exit()
def runtimeError():
    1/0
def timeError():
    while(1):
        pass


def runErrorCall(value, crumbNum):
    numDigits = subsPerFrame * 2
    binNum = format(int(value), "0" + str(numDigits) + "b")
    call = binNum[crumbNum*2:crumbNum*2+2]
    if call == "00":
        memError()
    if call == "01":
        wrongAns()
    if call == "10":
        runtimeError()
    if call == "11":
        timeError()

# your code should map the chosen input frame to a number which should then be passed to runErrorCall
# for example, if the input frame gets mapped to 12, you should call runErrorCall(12, crumbNum)
# in order to access later test cases, add code at the start to recognize the first test case and submit the correct ans
# remember to map something to "END" in order to stop sending submissions
# your code should only use the frameNumber
# PLACE CODE AFTER HERE ------------------------------------------------------------------------------------------------

#example, zbrka
num0, num1 = input().split(" ")

# for this example, we will treat each digit as a seperate frame, so two crumbs will be needed per frame
# we will map each number to its associated number, we will map the space char to 10, and then map END to 11

# put input into a list of digits (frames)
outList = []
for dig in num0:
    outList.append(int(dig))
outList.append(10) #append space
for dig in num1:
    outList.append(int(dig))
outList.append(11) #append END

runErrorCall(outList[frameNum], crumbNum) #make call to error





