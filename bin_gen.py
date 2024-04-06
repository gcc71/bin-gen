import os;

def compile_loop():
    for x in range(1,5):
        out_file_name = 'out_bins/test' + str(x) + '.exe'
        run_gpp('in_bins/hello_bin_gen.cpp', out_file_name)

def run_gpp(in_file_name, out_file_name):
    cmd_line = "g++ " + in_file_name + " -o " + out_file_name
    print(cmd_line)
    os.system(cmd_line)


if __name__ == "__main__":
    print('main')
    compile_loop()
    
    