from os import listdir
import sys
import scripts.wipe_dev

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print("Usage: run_script.py <script_name>")
        print("Available scripts:")
        for script in listdir("scripts"):
            if script.endswith(".py"):
                print("\t" + script[:-3])
        sys.exit(1)
    script_name = sys.argv[1]
    if script_name == "wipe_dev":
        scripts.wipe_dev.run()
    else:
        print("Unknown script: {}".format(script_name))
        sys.exit(1)