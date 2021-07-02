import argparse

from utility import Utility


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--operation', help='Type of operation', type=str)
    parser.add_argument('--src', help='Path to src', type=str)
    parser.add_argument('--to', help='Path to dst', type=str)
    parser.add_argument('--threads', help='Amount of threads', type=int)
    
    args = parser.parse_args()
    utility = Utility(threads=args.threads, src=args.src)
    args.src = utility.pure_path(args.src)
    utility.do_operation(args.operation, args.src, args.to)
        

    

    