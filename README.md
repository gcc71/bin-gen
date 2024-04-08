# bin-gen
This script creates random cpp source files and compiles them to generate random executables. The script was created to support creation of Deep Learning datasets.

## Requirements
bin-gen requires g++ and an input file containing valid cpp headers on the local system. 

## Usage
The command below creates 1 random executable and stores it in /bin which is a directory that can be specified. 
```
python bin_gen.py make-bins -c 1 -out bin
```

This command tests all generated executables. -v set to 1 is optional for verbose output. If no verbosity is desired do not include -v 1. 
```
python bin_gen.py test-execs -d bin -v 1
```