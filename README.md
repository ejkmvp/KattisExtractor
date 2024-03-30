# KattisExtractor
Extract Test Cases from Kattis

## How it Works
I did not come up with this idea btw. Kattis does not reveal failed test cases, but it does reveal why the test case fails. Thus, each submission failure code can be treated as an output. Thus, its possible to extract data about a test case

## Usage
This relies on submit.py, which comes from https://github.com/Kattis/kattis-cli
extractor.py - main python file to run
sub.py - file sent over to Kattis servers. This file should be modified to take in the test case input, split it into "frames", and send over a specific frame depending on the frameNum variable
submissionProcess.py - Maps return value from Kattis submission. This file should be modified to properly map the value from each frame 

run extractor.py and specify the problem name (name of problem in URL) and number of submissions per frame.
For an example, check the examples page

