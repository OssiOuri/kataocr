# Ossi Ouri
# Task description: http://codingdojo.org/cgi-bin/index.pl?KataBankOCR


import sys


def get_bdigit(d, digit_position):
    """Function receives big digit bank account (first parameter) and returns
    a single big digit incicated by the digit_position."""
    bdigit = []

    bdigit.append(d[0][3*digit_position:3*digit_position+3])
    bdigit.append(d[1][3*digit_position:3*digit_position+3])
    bdigit.append(d[2][3*digit_position:3*digit_position+3])

    return bdigit


def print_bdigit(d):
    """Debug function to print a big digit or big digit account.
    """
    print d[0]
    print d[1]
    print d[2]


def get_bdigit_cvalue(d):
    """ Function receives a big digit, converts that to a code value
    representing the big digit and returns the code value. Each big digit
    consists of 3x3 char matrix. Each char is coded in the following way:
    ' ' == 00,
    '|' == 01
    '_' == 11
    There shouldn't be any other char but in such a case:
    '?' == 10.
    """
    single_bdigit_line = ''
    single_bdigit_line += '' + d[0] + d[1] + d[2]

    value = 0
    for i in range(len(single_bdigit_line)):
        if (single_bdigit_line[i] == '_'):
            value = value | (3 << (i * 2))
        else:
            if (single_bdigit_line[i] == '|'):
                value = value | (1 << (i * 2))
            else:
                if (single_bdigit_line[i] == ' '):
                    value = value | (0 << (i * 2))
                else:
                    value = value | (2 << (i * 2))
    return value


def init_conversion_dictionary(d):
    """Function initializes hash function so that all big digits are identified.
    """
    bdigit_from_0_to_9 = [' _     _  _     _  _  _  _  _ ',
                          '| |  | _| _||_||_ |_   ||_||_|',
                          '|_|  ||_  _|  | _||_|  ||_| _|']

    for i in range(10):
        x = get_bdigit_cvalue(get_bdigit(bdigit_from_0_to_9, i))
        d[x] = i


def checksum(a):
    """
    account number:   3  4  5  8  8  2  8  6  5
    position names:  d9 d8 d7 d6 d5 d4 d3 d2 d1
    (d1+2*d2+3*d3 +..+9*d9) mod 11 = 0
    """
    value = 0
    for i in range(9):
        value += (int(a[8-i]) * (i+1))
    if ((value % 11) == 0):
        return True
    else:
        return False


def fix_bdigit(bdigit_cvalue, bdigit_to_dec):
    """ """
    change_candidates = []
    org_cvalue = bdigit_cvalue

    for i in range(11):
        bdigit_cvalue = bdigit_cvalue & (~(1 << i*2))
        bdigit_cvalue = bdigit_cvalue & (~(1 << i*2+1))
        # try 00 == ' '
        try:
            a = bdigit_to_dec[bdigit_cvalue]
            if bdigit_cvalue != org_cvalue:
                change_candidates.append(a)
        except:
            a = -9
        bdigit_cvalue = bdigit_cvalue | (1 << i*2)
        # try 01 == '|'
        try:
            a = bdigit_to_dec[bdigit_cvalue]
            if bdigit_cvalue != org_cvalue:
                change_candidates.append(a)
        except:
            a = -9
        bdigit_cvalue = bdigit_cvalue | (1 << i*2+1)
        # try 11 == '_'
        try:
            a = bdigit_to_dec[bdigit_cvalue]
            if bdigit_cvalue != org_cvalue:
                change_candidates.append(a)
        except:
            a = -9
        bdigit_cvalue = org_cvalue
    return change_candidates


def fix_all_digit(a, bdigit_account, bdigit_to_dec):
    """ """
    b = []
    candidates = []
    t = list(a)
    for i in range(len(t)):
        del candidates[:]
        cvalue = get_bdigit_cvalue(get_bdigit(bdigit_account, i))
        candidates = fix_bdigit(cvalue, bdigit_to_dec)
        for j in range(len(candidates)):
            org_t_i = t[i]
            t[i] = str(candidates[j])
            aa = ''
            aa = '' + aa.join(t)
            b.append(aa)
            t[i] = org_t_i
    return b


def find_bank_accounts_from_checksum_failure(b, bdigit_to_dec, bdigit_account):
    """ """
    a = b.pop(0)
    if len(b) > 0:
        return -1  #  shouldn't be, expecting only one...
    alist = fix_all_digit(a, bdigit_account, bdigit_to_dec)
    b.extend(alist)
    return 0


def fix_illegal_digit(a, bdigit_account, bdigit_to_dec):
    """ """
    b = []
    candidates = []
    t = list(a)
    for i in range(len(t)):
        if t[i] == '?':
            cvalue = get_bdigit_cvalue(get_bdigit(bdigit_account, i))
            candidates = fix_bdigit(cvalue, bdigit_to_dec)
            for j in range(len(candidates)):
                t[i] = str(candidates[j])
                aa = ''
                aa = '' + aa.join(t)
                b.append(aa)
            break
    return b


def find_bank_accounts_from_illegal(b, bdigit_to_dec, bdigit_account):
    """This function receives a list of illegal bank accounts, hash
    conversion table and corresponding original bank account in big digit
    format. Function generates single changes (add and remove empty, pipe or
    undescore chars) to each illegal big digit. This list of possible bank
    accounts is returned to caller.
    """
    fixed = False
    checked = 0

    for i in range(len(b)):
        if '?' in b[i]:
            a = b.pop(i)
            alist = fix_illegal_digit(a, bdigit_account, bdigit_to_dec)
            b.extend(alist)
            fixed = True
            break
        else:
            checked += 1
    if fixed is False:
        return -1
    #  ok, so on this round we were able to fix something, let's continue!
    find_bank_accounts_from_illegal(b, bdigit_to_dec, bdigit_account)
    return 0


def remove_checksum_invalid_bank_accounts(a):
    """This function receives a list of bank accounts and removes checksum
    invalid accounts from the list.
    """
    for i in range(len(a)):
        if (checksum(a[i])) == False:
            #  print 'rejecting %s due to checksum mismatch' % a[i]
            a.pop(i)
            remove_checksum_invalid_bank_accounts(a)
            break
    return


def fix_checksum_fail_bank_account(org_b_account,
                                   bdigit_to_dec,
                                   bdigit_account):
    """This function receives bank_account (org_b_account) which is 9 digit
    bank account in decimal format. Function also receives hash
    conversion table and corresponding original big digit account. Function
    returns fixed bank account or if cannot fix then original account marked
    with 'ERR' if checsum persistently fails and 'AMB' if multiple checksum
    correct solutions found.
    """
    a = []
    a.append(org_b_account)
    status = find_bank_accounts_from_checksum_failure(a,
                                                      bdigit_to_dec,
                                                      bdigit_account)
    if status < 0:
        # finding failed, return original account + ERR
        org_b_account += ' ERR'
        return org_b_account
    remove_checksum_invalid_bank_accounts(a)

    #  fix succeeded and now check if only one valid candidate!
    if len(a) == 1:
        # yes, yes, yes, we have a fixed winner!
        return str(a[0])
    else:
        if len(a) > 1:
            org_b_account += ' AMB'
            return org_b_account
        #  empty list, then return original + ILL
        org_b_account += ' ERR'
        return org_b_account


def fix_illegal_bank_account(org_b_account, bdigit_to_dec, bdigit_account):
    """This function receives bank_account (org_b_account) which is 9 digit
    bank account in decimal format and which is supposed to contain at least
    one corrupted digit replaced with '?'. Function also reveives hash
    conversion table and corresponding original big digit account. Function
    returns fixed bank account or if cannot fix then original account marked
    with ' ILL' if persistently illegal and 'AMB' if multiple checksum correct
    solutions found.
    """
    a = []
    a.append(org_b_account)

    status = find_bank_accounts_from_illegal(a, bdigit_to_dec, bdigit_account)
    if status < 0:
        #  finding failed, return original account + ILL
        org_b_account += ' ILL'
        return org_b_account
    remove_checksum_invalid_bank_accounts(a)

    #  fix succeeded and now check if only one valid candidate!
    if len(a) == 1:
        # yes, yes, yes, we have the winner!
        return str(a[0])
    else:
        if len(a) > 1:
            org_b_account += ' AMB'
            return org_b_account
        #  empty list, then return original + ILL
        org_b_account += ' ILL'
        return org_b_account


def bdigit_account_to_dec(bdigit_account, bdigit_to_dec):
    """ Function receives a 9 big digit account number (bdigit_account) and
    pre-configured hash table to convert big digits to decimal. Function
    returns account in a string format. If big digit bank account is corrupted
    this functions tries to fix it automatically.
    """
    b_account = ''
    a = ''

    for i in range(9):
        cvalue = get_bdigit_cvalue(get_bdigit(bdigit_account, i))
        try:
            #  Try if succesfull hash conversion from big digit to decimal.
            a = bdigit_to_dec[cvalue]
        except:
            # Well, no match. Try to fix later. Now just mark no match.
            a = '?'
        b_account += str(a)

    if '?' in b_account:
        b_account = fix_illegal_bank_account(b_account,
                                             bdigit_to_dec,
                                             bdigit_account)
    else:
        #  No unidentified big digits, however checksum might still fail and
        #  if it does fail then we need to try to fix it.
        if (checksum(b_account)) == False:
            b_account = fix_checksum_fail_bank_account(b_account,
                                                       bdigit_to_dec,
                                                       bdigit_account)
    return b_account


def get_bdigit_account(bdigit_account, fi):
    """Function reads a big digit account number from file fi and stores that
    to bdigit_account. Valid bdigit_account is returned to caller if function
    returns True otherwise function returns False. It is expected that file fi
    consists of 3 line bdigit accounts and one extra empty line for each
    account.
    """
    line_nmb = 0
    for line in fi:
        line = line.rstrip('\n')
        if (line_nmb + 1) % 4 == 0:
            return True
        else:
            bdigit_account.append(line)
            line_nmb += 1
    return False


def process_bdigit_file(input_file):
    """Reads bank accounts in big digit format from the given input file
    and converts them to decimal format. Returns a list of bank accounts
    in a list of strings.
    See more from http://codingdojo.org/cgi-bin/index.pl?KataBankOCR
    This implementation passes user story 4 tests.
    """
    #  hash conversion initializations
    bdigit_to_dec = dict()
    init_conversion_dictionary(bdigit_to_dec)

    bank_account = []  # list of bank accounts in decimal format
    bdigit_account = []  # one bank account in big digit format

    with open(input_file, 'r') as fi:
        while(get_bdigit_account(bdigit_account, fi)):
            a = bdigit_account_to_dec(bdigit_account, bdigit_to_dec)
            bank_account.append(a)
            del bdigit_account[:]
    return bank_account


if __name__ == '__main__':
    if(len(sys.argv) == 2):
        b = []
        b = process_bdigit_file(sys.argv[1])
        with open('output.txt', 'w') as fo:
            for i in range(len(b)):
                fo.write(b[i]+'\n')
    else:
        print 'usage: python ocr.py <input file>'





