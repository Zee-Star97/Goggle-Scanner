# PLCS CW2 CWE-119 Vulnerable Code Example

## Overview
This directory contains **intentionally vulnerable code** that demonstrates **CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer**.  
The purpose of this project is **educational**, aimed at helping students, developers, and security researchers understand how buffer overflow vulnerabilities occur and how they can be identified and mitigated.

⚠️ **Do not use this code in production environments.**

---

## What is CWE-119?
**CWE-119** occurs when a program performs operations on a memory buffer without properly validating its boundaries.  
This can result in:

- Buffer overflows
- Memory corruption
- Program crashes
- Arbitrary code execution
- Security breaches

More details can be found in the official CWE documentation:
- https://cwe.mitre.org/data/definitions/119.html

---

## Vulnerability Description
The vulnerable code in this directory fails to properly validate input size before copying data into a fixed-size buffer.  
As a result, input larger than the allocated buffer can overwrite adjacent memory.

This vulnerability is commonly found in:
- C/C++ applications
- Low-level memory manipulation
- Unsafe string handling functions