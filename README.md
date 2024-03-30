
# KattisExtractor
Extract Test Cases from Kattis

## WARNING (Kattis TOS)
This is for educational and experimental purposes only. Though the Kattis TOS does state that automated access is allowed, it doesn't specifically mention any restrictions on submissions (other than abiding by the rate limit). To use this software under TOS, a descriptive user-agent with a method of contact (email, phone, etc) must be used, and this software must be used on a personal account since "You may only have one personal account" and "We do not allow 'machine accounts'". I do not guarentee use of this program will not get your account deactivated. You can read the TOS at https://open.kattis.com/info/tos.
It's also important to note that this software is most definitely not allowed in any competition (ex. ICPC), and neither is it practical since it takes many failed submissions to extract just one test case.

## How it Works
I did not come up with this idea btw. Kattis does not reveal failed test cases, but it does reveal why the test case fails. Thus, each submission failure code can be treated as an output. Therefore, its possible to extract data about a test case.

## Usage
This relies on submit.py, which comes from https://github.com/Kattis/kattis-cli.
The remaining files are used as such...
- config.txt - Contains API Key. Should come from https://open.kattis.com/download/kattisrc
- extractor.py - main python file to run
- sub.py - file sent over to Kattis servers. This file should be modified to.. 
    - take in the test case input
    - split it into "frames"
    - send over a specific frame depending on the frameNum variable
- submissionProcess.py - Maps return value from Kattis submission. This file should be modified to properly map the value from each frame 

run extractor.py and specify the problem name (name of problem in URL) and number of submissions per frame.

For an example sub.py and submissionProcess.py, check the examples folder.

