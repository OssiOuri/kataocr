import sys

def read_reference_accounts(ref_account_file):
    ref_list = []
    with open(ref_account_file, 'r') as f:
        for line in f: 
            ref_list.append(line.rstrip())
    return ref_list

if __name__ == '__main__':
    if(len(sys.argv) == 2):
        read_reference_accounts(str(sys.argv[1]))
    else:
        print 'usage: python bankocr_test.py <input file>'

