## Prerequisites

After installing this code from Gitlab, the docker environment needs to be set up. Ensure that docker is installed on your system. Then, in the project directory, run 'docker compose build'. This should install the necessary dependencies needed on the system level and create the environment. 

## Running the application

Once the necessary dependencies have been installed, the application should be able to be used. Run the command 'python3 app.py [FILE]' - where [FILE] is the name of the source file (or path if not in local directory) that you wish to run the application against. The program should then run its static analysis and fuzzing functions sequentially against the provided code file. The target file should only be either a C or C++ file.

## Purpose
The program has two functions: the static analyser and the fuzzer. The static analysis function will search through code to detect vulnerable functions, whereas the fuzzer will send exponentially larger and larger payloads to detect a memory corruption / buffer overflow vulnerability against the code. The goal of this program is to create a simple tool that can be easily used to perform static analysis and lightweight fuzzing against code files, specifically focusing on C/C++ code.

## Understanding Output

Once the application has been successfully run against a code file, it should return the outcome of its findings. If there are no concerns, the application will state this clearly. If any vulnerabilities are found, the exact details of this will be highlighted. The static analysis function will detail each vulnerable function that it has detected, including its specific location within the code. The fuzzing function will send a crash message as soon as a payload manages to successfully cause a buffer overflow. 

## Additional Files

In order to validate the tool's effectiveness with ease, a range of vulnerable code files have been included in the subdirectory 'sample_code'. Each of the files within this directory showcases a vulnerability mapped to different CWEs. Additionally, to streamline the docker building process, a docker-compose file has been included. This allows for commands like 'docker compose up' to be used. There was also a jenkinsfile previously included for static analysis on the tool itself, but has since been removed following the completion of the tool. 