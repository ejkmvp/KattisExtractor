import submit
import configparser
import time
import requests
import sys
from submissionProcess import *

judgementMap = {
    10: "00",
    14: "01",
    9: "10",
    12: "11"
}

def attemptLogin():
    global cfg
    for x in range(5): #try 5 times
        try:
            login_reply = submit.login_from_config(cfg)
        except Exception as e:
            print("Exception occured during login attempt, trying again:", str(e))
            time.sleep(5)
            continue
        if login_reply.status_code == 429: # rate limit. idk if this code can even be thrown
            print("rate limit!! waiting 1 minute")
            time.sleep(60)
            continue
        elif login_reply.status_code == 403: #token is expired/invalid
            print("Token expired/invalid: please repull config file and then hit enter to continue")
            input()
            cfg.read("config.txt")
            continue
        elif login_reply.status_code != 200:
            print("Error. Status code", login_reply.status_code)
            time.sleep(5)
        else:
            return login_reply
    raise Exception("Login failed 5 times")

def attemptSubmission(problem): #login_reply is global so we can update cookies if necessary
    global login_reply
    global cfg
    submit_url = submit.get_url(cfg, 'submissionurl', 'submit')
    while True:
        try:
            result = submit.submit(submit_url, login_reply.cookies, problem, "Python 3", ["sub.py"], "")
        except Exception as e:
            print("Error during submission, trying again", str(e))
            time.sleep(2)
            continue
        if result.status_code == 429:
            print("rate limit!! waiting 1 minute")
            time.sleep(60)
            continue
        if result.status_code == 403 or result.status_code == 401: #im guessing one of these means we need to relogin
            print("Auth Error: attempting to re-login:")
            time.sleep(1)
            login_reply = attemptLogin(cfg)
            time.sleep(1)
            continue
        if result.status_code != 200:
            print("Error. Status code", result.status_code)
            time.sleep(1)
            continue
        # now, result contains the result
        print("Submission success")
        return result

def getJudgementId(submission_url):
    global login_reply
    global cfg
    while True:
        try:
            judgement_status = requests.get(submission_url + '?json', cookies=login_reply.cookies, headers=submit._HEADERS)
        except Exception as e:
            print("Error during judgement Request, trying again", str(e))
            time.sleep(2)
            continue
        if judgement_status.status_code == 429:
            print("rate limit!! waiting 1 minute")
            time.sleep(60)
            continue
        if judgement_status.status_code == 403 or judgement_status.status_code == 401: #im guessing one of these means we need to relogin
            print("Auth Error: attempting to re-login:")
            time.sleep(1)
            login_reply = attemptLogin(cfg)
            time.sleep(1)
            continue
        if judgement_status.status_code != 200:
            print("Error. Status code", result.status_code)
            time.sleep(1)
            continue
        submission_code = judgement_status.json()['status_id']
        if submission_code <= 5:
            print("Solution is still running, waiting 1 second")
            time.sleep(1)
            continue
        return submission_code

if len(sys.argv) not in [3, 4, 5]:
    print("\nUsage: python extractor.py <problemName> <SubmissionsPerFrame> [iterationStart=0] [iterationEnd=-1]")
    print("sub.py: edit bottom of file so that it will run when submitted for the problem")
    print("submissionProcess.py: edit processData function so that it properly processes the submission outputs")
    print("config.txt: contains config data from https://open.kattis.com/download/kattisrc")
    exit()

print("Before continuing, make sure that:")
print("1. sub.py functions (by testing inputs on it yourself)")
print("2. submissionProcess.py properly handles input data, including a mapping to \"END\" to indicate no more submissions")
print("3. config.txt contains updated token")
input("Press enter to continue:")

problem = sys.argv[1]
subsPerFrame = int(sys.argv[2])
iterStart = 0
if len(sys.argv) >= 4:
    iterStart = int(sys.argv[3])
iterMax = -1
if len(sys.argv) == 5:
    iterMax = int(sys.argv[4])

#read in config
print("-----\n")
print("Reading in Config")
cfg = configparser.ConfigParser()
cfg.read("config.txt")
if "token" not in cfg["user"]:
    print("Token not found in config.txt")
    for item in cfg:
        print(item)
    exit()
if "username" not in cfg["user"]:
    print("Username not found in config.txt")
    exit()
print("Attempting Login")
#attempt login
login_reply = attemptLogin()
print("Login Successful")

result = []
output = []
x = iterStart
keepSearch = True
while keepSearch:
    frameNum = int(x / subsPerFrame)
    crumbNum = x % subsPerFrame
    #dirty solution: open up sub.py to inject x
    with open("sub.py", "r") as f:
        lines = f.readlines()
    with open("sub.py", "w") as f:
        f.write("frameNum = " + str(frameNum) + "\n")
        f.write("crumbNum = " + str(crumbNum) + "\n")
        f.write("subsPerFrame = " + str(subsPerFrame) + "\n")
        for line in lines[3:]:
            f.write(line)

    while True:
    #attempt submission
        #TODO add some limit here. if there are more than N submissions, just call it off and
        submission_result = attemptSubmission(problem)
        #get submission URL
        submission_url = submit.get_submission_url(submission_result.content.decode('utf-8').replace('<br />', '\n'), cfg)
        if submission_url == None:
            print("submission limit likely reached, waiting 30 seconds before trying again")
            time.sleep(30)
        else:
            break
        #get judgement code
    judgement_code = getJudgementId(submission_url)
    print("received error:", judgement_code)
    if judgement_code not in judgementMap.keys():
        print("Unexpected result code, trying again")
        continue
    else:
        result.append(judgementMap[judgement_code])
        if len(result) == subsPerFrame:
            outputVal = ""
            for item in result:
                outputVal += item
            outValue = str(processFrame(int(outputVal, 2)))
            if outValue == "END":
                print("received END")
                keepSearch = False
            print("received value:", outValue)
            output.append(outValue)
            result = []
        if x == iterMax:
            keepSearch = False
        x += 1

    # ----------------------------------------------------------------------------------------------------

print("Finished")
print(output)


