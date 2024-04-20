import random, string, os, sys, shutil, argparse, pathlib, json
from tqdm import tqdm

# this class is used to store file attributs
class dataFile:
    def __init__(self, path, size, file_name, file_ext):
        self.path = path
        self.size = size
        self.file_name = file_name
        self.file_ext = file_ext
    def to_dict(self):
        return{
            'path': self.path,
            'size': self.size,
            'file_name': self.file_name,
            'file_ext': self.file_ext

        }

# this function uses the dataFile class to retrieve all files from a given directory
def get_files(top_dir):
    dataFiles = []
    for currentpath, folders, files in os.walk(top_dir):
        for file in files:
            file_path = os.path.join(currentpath, file)
            file_name = pathlib.PureWindowsPath(file_path).name
            file_ext = pathlib.PureWindowsPath(file_path).suffix
            df = dataFile(file_path, os.path.getsize(file_path), file_name, file_ext)
            dataFiles.append(df)
    return dataFiles

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
    ran_includes = []
    
    # read in config
    json_file = 'config.json'
    with open(json_file) as json_data:
        data = json.load(json_data)
    
    # always include these includes
    for i in data['always_includes']:
        statements.append(i)
    
    # random include these includes
    for i in data['ran_includes']:
        ran_includes.append(i)
  
    for x in range(0,random.randint(min, max)):
        stat = ran_includes[random.randint(0, len(ran_includes) - 1)]
       
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
         
        # clear the list
        src_lines.clear()

def compile_all(src_directory, out_directory):
    # make out dir if not exist
    os.makedirs(out_directory, exist_ok = True)
   
    for files in tqdm(get_files(src_directory)):
        out_file_name = out_directory + '/' + files.file_name.replace('.cpp', '.exe')
        run_gpp(files.path, out_file_name)

# make random exe files
def make_bins(count, out_directory):
    gen_ran_src_files(count, 'tmp_src')
    compile_all('tmp_src', out_directory)
    shutil.rmtree('tmp_src')

# This function will execute all executables in a specified directory and capture exit codes
def test_execs(directory, verbose):
    errors = 0

    if not verbose:
        for f in tqdm(get_files(directory)):
            cmd_line = f.path
            ec = os.system(cmd_line + "> NUL")
            errors += ec
    else:# verbose
        for f in get_files(directory):
            cmd_line = f.path
            print("testing: " + cmd_line)
            ec = os.system(cmd_line)
            errors += ec
            print("Exit Code: " + str(ec)) 

    print("test complete with " + str(errors) + " errors")
 
# this function run the g++ compiler
def run_gpp(in_file_name, out_file_name):
    cmd_line = "g++ " + in_file_name + " -o " + out_file_name
    os.system(cmd_line)

# this function reads the upx report and display count
def read_upx_reprot(file_path):
    dll_list = []
    #make sure to open file in notepad and save it as UTF-8
    f = open(file_path, "r")
    for l in f:
        if 'win64/pe' in l:
            ss = l.split('win64/pe')
            file_name = ss[1].rstrip().replace(' ', '')
            dll_list.append(file_name)
        if 'win32/pe' in l:
            ss = l.split('win32/pe')
            file_name = ss[1].rstrip().replace(' ', '')
            dll_list.append(file_name)
    print("make sure to open file in notepad and save it as UTF-8 before trying to read it")
    print(len(dll_list), "compressed PE files...")

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
    
    # add test executables
    parser_test_exec = subparsers.add_parser('test-execs', help='Runs all executables in directory')
    parser_test_exec.add_argument('-d', '--directory', type=str, help='The target directory', required = True)
    parser_test_exec.add_argument('-v', '--verbose', type=int, help='The target directory', required = False)
    
    # add read upx report
    parser_test_exec = subparsers.add_parser('read-upx-report', help='Reads upx report file')
    parser_test_exec.add_argument('-f', '--file', type=str, help='The file path', required = True)
    




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

    if args.command_name == 'test-execs':
        test_execs(args.directory, args.verbose)
    
    if args.command_name == 'read-upx-report':
        read_upx_reprot(args.file)





    
    