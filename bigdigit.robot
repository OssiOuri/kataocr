*** Settings ***
Library           OperatingSystem
Library           ocr.py
Library           ./test/big_digit_test_util.py

*** Variables ***

*** Test Cases ***
userstory_4
    [Documentation]    Reads the big char input file, converts big chars to ascii string and compares conversion. 
    run keyword    Convert Big Digits And Compare    ./test/userstory4/input.txt    ./test/userstory4/ref.txt


*** Keywords ***
Convert Big Digits And Compare
    [Arguments]    ${bigcharfile}    ${referencefile}
    Log    ${bigcharfile}
    @{account}=    run keyword    process bdigit file    ${bigcharfile}
    Log Many   @{account}
    @{ref_account}    run keyword    Read Reference Accounts    ${referencefile}
    ${index}=    set variable    ${0}
    : FOR    ${acc}    IN    @{account}    
    \    Should Be Equal    ${acc}    @{ref_account}[${index}]    
    \    ${index}     evaluate    ${index}+1
    Should Be True    ${index} > 11

