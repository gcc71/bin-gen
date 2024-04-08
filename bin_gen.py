import random, string, os, sys, shutil, argparse
import mt_util as mt

#this function generates a random word of a given length
def randomword(length):
  letters = string.ascii_letters
  return ''.join(random.choice(letters) for i in range(length))

#this function generates random string variable assignment statements
def gen_ran_string_var_stat(min, max):
    statements = []
    statements.append("using namespace std;")
    for x in range(0,random.randint(min, max)):
        ran_var_statement = "string " + randomword(random.randint(4, 12)) + " = \"" + randomword(random.randint(4, 12)) + "\";"
        statements.append(ran_var_statement)
    return statements

#this function generates random int variable assignment statements
def gen_ran_int_var_stat(min, max):
    statements = []
    for x in range(0,random.randint(min, max)):
        ran_var_statement = "int " + randomword(random.randint(4, 12)) + " = " + str(random.randint(1, 1200)) + ";"
        statements.append(ran_var_statement)
    return statements

# this function generates random include statements
# note: function requires valid include statement input file 'valid_mageo_includes.txt'
# The input file contains valid include statements for the machine where this code runs
def gen_ran_include_stat(min, max):
    statements = []
    # always include these includes
    statements.append('#include <iostream>')
    statements.append('#include <vector>')
    statements.append('#include <string>')

    # open valid includes file for random selections
    with open('valid_mageo_includes.txt') as f:
        content = f.readlines()
        content = [x.strip() for x in content]

    for x in range(0,random.randint(min, max)):
        stat = content[random.randint(0, len(content) - 1)]#debug here
        if stat not in statements:
            statements.append(stat)
    
    return statements

# This function generates a random main function
def gen_ran_main(min, max):
    statements = []
    statements.append("int main(){")
   
    for i in range(0,random.randint(min, max)):
        line = "\tcout << \"" + randomword(26) + "\" << endl;"
        statements.append(line)
    statements.append("}")
    return statements

# This function generates random src files
def gen_ran_src_files(count, out_directory):
    # make out dir if not exist
    os.makedirs(out_directory, exist_ok = True)
    
    # create list for src code lines Note: it needs to be cleared for each iteration
    src_lines = []
    
    for i in range(0, count):
        
        # write includes
        for s in gen_ran_include_stat(4,32):
            src_lines.append(s)
        
        # call a random number of int var statements
        for x in gen_ran_int_var_stat(1, 10):
            src_lines.append(x)
                       
        # call a random number of string var statements
        for x in gen_ran_string_var_stat(1, 10):
            src_lines.append(x)
        
        # call generate random main
        for s in gen_ran_main(4,10):
            src_lines.append(s)
        
        # write to file
        file_name = out_directory + "/" + randomword(10) + str(i) + ".cpp"
        with open(file_name, 'a') as the_file:
            for sl in src_lines:
                the_file.write(sl + '\n')
        
        # test prints        
        # for sl in src_lines:
        #     print(sl)
        
        # clear the list
        src_lines.clear()

def compile_all(src_directory, out_directory):
    # make out dir if not exist
    os.makedirs(out_directory, exist_ok = True)

    for files in mt.get_files(src_directory):
        out_file_name = out_directory + '/' + files.file_name.replace('.cpp', '.exe')
        run_gpp(files.path, out_file_name)

def make_bins(count, out_directory):
    gen_ran_src_files(count, 'tmp_src')
    compile_all('tmp_src', out_directory)
    shutil.rmtree('tmp_src')


# def compile_loop():
#     for x in range(1,5):
#         out_file_name = 'out_bins/test' + str(x) + '.exe'
#         for files in mt.get_files('in_src'):
#             print(files.path)
        # run_gpp('in_bins/hello_bin_gen.cpp', out_file_name)

def run_gpp(in_file_name, out_file_name):
    cmd_line = "g++ " + in_file_name + " -o " + out_file_name
    print(cmd_line)
    os.system(cmd_line)

# begin main
if __name__ == "__main__":

    #add arg parse tree
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command_name', help='Command help')
    
    # add generate src files with args
    parser_projects = subparsers.add_parser('gen-src-files', help='Generates source files')
    parser_projects.add_argument('-c', '--count', type=int, help='The count of files to be generated', required = True)
    parser_projects.add_argument('-d', '--srcdir', type=str, help='The out directory for files to be generated', required = True)
    
    # add compile command with args
    parser_compile = subparsers.add_parser('com-src-files', help='Generates source files')
    parser_compile.add_argument('-in', '--indir', type=str, help='The src directory', required = True)
    parser_compile.add_argument('-out', '--outdir', type=str, help='The out directory', required = True)

    # add make bins command with args
    parser_mk_bins = subparsers.add_parser('make-bins', help='Generates bin files')
    parser_mk_bins.add_argument('-out', '--outdir', type=str, help='The out file directory', required = True)
    parser_mk_bins.add_argument('-c', '--count', type=int, help='The count of bin files to be generated', required = True)

      
    # parse args and handle
    args = parser.parse_args()

    if args.command_name is None:
        print("Select a command. '-h/--help' for references.")
        sys.exit(1)    
    
    if args.command_name == 'gen-src-files':
        gen_ran_src_files(args.count, args.srcdir)
    
    if args.command_name == 'com-src-files':
        compile_all(args.indir, args.outdir)
    
    if args.command_name == 'make-bins':
        make_bins(args.count, args.outdir)




    
    