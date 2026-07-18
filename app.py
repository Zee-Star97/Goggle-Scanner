import os
import re
import subprocess
import argparse
import sys

# Vulnerability regexes matching specific CWEs
VULNERABILITIES = {
    'CWE-119/120 (Buffer Overflows)': [
        r'\bgets\b', r'\bstrcpy\b', r'\bstrcat\b', r'\bsprintf\b', r'\bvsprintf\b', r'\bscanf\b'
    ],
    'CWE-131/190 (Memory/Integer Issues)': [
        r'\balloca\b', r'\bmemcpy\b'
    ],
    'CWE-78 (OS Command Injection)': [
        r'\bsystem\b', r'\bpopen\b', r'\bexecl\b', r'\bexecle\b', r'\bexecv\b', r'\bexecvp\b'
    ],
    'CWE-134 (Format String Vulnerability)': [
        r'\b(?:printf|fprintf|syslog|snprintf)\s*\(\s*(?!["\'])[\w\d_>.\-]+'
    ]
}

# Whitelist to mitigate false flags
WHITELIST_MARKERS = [r'//\s*SAFE', r'//\s*IGNORE']

# Function to run static analysis on source file
def run_static_analysis(source_file):

    # Output error if file not found
    if not os.path.isfile(source_file):
        print(f" Static Analysis Error: File '{source_file}' not found.")
        return False

    print(f"\nStarting Static Analysis on: {source_file}")
    print("-" * 30)
    
    findings = []
    in_multiline_comment = False

    # Open and read the source file
    try:
        with open(source_file, 'r', encoding='utf-8') as file:

            # Parsing the contents line by line
            for line_num, line in enumerate(file, 1):
                original_line = line.rstrip()

                # Detecting whitelist markers
                if any(re.search(wl, original_line, re.IGNORECASE) for wl in WHITELIST_MARKERS):
                    continue

                clean_line = original_line

                # Handling comments over multiple lines
                if in_multiline_comment:
                    if '*/' in clean_line:
                        clean_line = clean_line.split('*/', 1)[1]
                        in_multiline_comment = False
                    else:
                        continue

                if '/*' in clean_line:
                    if '*/' in clean_line:
                        clean_line = re.sub(r'/\*.*?\*/', '', clean_line)
                    else:
                        in_multiline_comment = True
                        clean_line = clean_line.split('/*', 1)[0]

                # Handling inline comments
                clean_line = clean_line.split('//')[0]
                clean_line = re.sub(r'".*?(?<!\\)"', '""', clean_line) 

                if not clean_line.strip():
                    continue

                # Noting any flagged vulnerabilities according to previous regexes
                for category, patterns in VULNERABILITIES.items():
                    for pattern in patterns:
                        match = re.search(pattern, clean_line)
                        if match:
                            func_name = match.group(0).split('(')[0].strip()
                            findings.append({
                                'line': line_num,
                                'category': category,
                                'func': func_name,
                                'code': original_line.strip()
                            })

    # Output error if source file cannot be read       
    except Exception as e:
        print(f"Error reading source file: {e}")
        return False

    if not findings:
        # Output message if no flagged vulnerabilities (or only whitelist markers)
        print("No unsafe function signatures detected.")
    else:
        for finding in findings:
            # Print the details of each flagged vulnerability
            print(f"    Line {finding['line']} | {finding['category']}")
            print(f"    Function: {finding['func']}")
            print(f"    Code:   {finding['code']}\n")
        print(f"Total potential vulnerabilities flagged: {len(findings)}")
    
    return True

# Function to compile source code into an executable
def compile_source(source_file):
    
    print(f"\nCompiling {source_file}...")
    print("-" * 30)
    
    # Identifying the correct compiler based on file extension
    ext = os.path.splitext(source_file)[1].lower()
    compiler = 'g++' if ext in ['.cpp', '.cc', '.cxx'] else 'gcc'
    
    # Defining the resulting executable
    output_exe = os.path.splitext(source_file)[0] + ("_fuzz_target.exe" if os.name == 'nt' else "_fuzz_target.out")

    try:
        # Running the compiler
        result = subprocess.run(
            [compiler, source_file, "-o", output_exe], 
            capture_output=True, 
            text=True,
            shell=False
        )
        
        # Output an error if compilation failed
        if result.returncode != 0:
            print("Compilation Failed! See details below:")
            print(result.stderr)
            return None
        
        # Output message on success
        print(f"Compilation successful.")
        return output_exe
    
    except FileNotFoundError:
        # Error message if no file found
        print(f"Compiler Error: '{compiler}' is not installed or not found in system PATH.")
        return None
    except Exception as e:
        # Error message for other unexpected exception
        print(f"Unexpected compilation error: {e}")
        return None

# Function to perform fuzzing on the executable file
def run_fuzzer(executable_path):

    # Output error if no executable found
    if not os.path.isfile(executable_path):
        print(f"Fuzzer Error: Executable '{executable_path}' not found.")
        return

    print(f"\nStarting Fuzzing on: {executable_path}")
    print("-" * 30)

    # Exponentially larger payload sizes to attempt segmentation faults
    payload_sizes = [64, 256, 1024, 4096, 10000, 50000]
    
    # Generating the payload
    for size in payload_sizes:
        print(f"Sending payload of size: {size} bytes...")
        payload = b"A" * size

        try:
            process = subprocess.Popen(
                [executable_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Sending the payload
            process.communicate(input=payload, timeout=3)

            # If a negative return code is given, assume successful memory overload and output message
            if process.returncode < 0:
                print(f"\n           Crash detected! Program exited with signal code: {process.returncode}")
                print(f"           Payload: {size} bytes.")
                print(f"           Indicator of CWE-119 (Memory Corruption).")
                return 
        
        except subprocess.TimeoutExpired:
            # Output a timeout error message
            process.kill()
            print("Error: Process timed out.")
        except PermissionError:
            # Output missing permission error
            print("Error: Permission denied.")
            return
        except Exception as e:
            # Output general exception error
            print(f"Unexpected execution error: {e}")
            return

    # Output message if no crash encountered
    print("Fuzzing complete. No crashes detected.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="End-to-end Lightweight SAST and Fuzzer toolkit.")
    
    # Now only accepts a single positional argument for the source file
    parser.add_argument("file", help="Path to source code file for analysis")
    args = parser.parse_args()

    source_path = args.file

    # Running the static analyser
    if run_static_analysis(source_path):
        
        # Compiling the source code
        executable = compile_source(source_path)
        
        # Running the fuzzer
        if executable:
            run_fuzzer(executable)
            
            # Delete the temporary executable file
            print("\nCleaning up temporary executable...")
            try:
                os.remove(executable)
                print("Cleanup complete.")
            except OSError as e:
                # Output error if temp file cannot be removed
                print(f" Error removing {executable}: {e}")