## Prerequisites

After installing this code from Gitlab, the docker environment needs to be set up. Ensure that docker is installed on your system. Then, in the project directory, run 'docker compose build'. This should install the necessary dependencies needed on the system level.

## Running the application

Once the necessary dependencies have been installed, the application should be able to be used. Run the command 'python3 app.py [FILE]' - where [FILE] is the name of the source file (or path if not in local directory) that you wish to run the application against. The program should then run its static analysis and fuzzing functions sequentially against the provided code file. 

## Purpose
The program has two functions: the static analyser and the fuzzer. The static analysis function will search through code to detect vulnerable functions, whereas the fuzzer will send exponentially larger and larger payloads to detect a memory corruption / buffer overflow vulnerability against the code. A temporary executable file will be created during execution to enable fuzzing, but should be deleted thereafter. The goal of this program is to create a simple tool that can be easily used to perform static analysis and lightweight fuzzing against code files, specifically focusing on C/C++ code.

## Understanding Output

Once the application has been successfully run against a code file, it should return the outcome of its findings. If there are no concerns, the application will state this clearly. If any vulnerabilities are found, the exact details of this will be highlighted. The static analysis function will detail each vulnerable function that it has detected, including its specific location within the code. The fuzzing function will send a crash message as soon as a payload manages to successfully cause a buffer overflow. 

## Additional Files

To streamline the docker building process, a docker-compose file has been included. The Jenkinsfile is linked to this, but is not necessary in order to run the application. Regardless, it has been included for transparency and to validate relevant references in the report. The Jenkinsfile is used to perform a range of security analysis functions against the project code. Should you deem it necessary, this process can be repeated by running 'docker compose up -d' in the project directory and then setting up a jenkins pipeline via the UI (hosted on localhost:8080 by default).