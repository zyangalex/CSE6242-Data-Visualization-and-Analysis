# Credits: https://github.com/fastai/course-v3/tree/master/nbs/dl2

import os
import sys
import re
import json

def is_export(cell):
    if cell['cell_type'] != 'code': return False
    src = cell['source']
    if len(src) == 0 or len(src[0]) < 7: return False
    return re.match(r'^\s*#\s*export\s*$', src[0], re.IGNORECASE) is not None

def removeTestLines(cellText):
    matchList = [re.search("^\s*tests", cell) for cell in cellText] # If any spaces are in front
    linesToRemoveIdx = [matchList.index(i) for i in matchList if i is not None]
    linesToRem = [cellText[i] for i in linesToRemoveIdx]
    for i in linesToRem:
        cellText.remove(i)
    return cellText

def notebook2scriptSingle(fname, destination):
    "Finds cells starting with `#export` and puts them into a new module"
    fname_out = 'submission.py'
    main_dic = json.load(open(fname,'r',encoding="utf-8"))
    code_cells = [c for c in main_dic['cells'] if is_export(c)]

    module = f'''
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: {fname}

'''
    for cell in code_cells:
        text = removeTestLines(cell['source'])
        module += ''.join(text[1:]) + '\n\n'

    # remove trailing spaces
    module = re.sub(r' +$', '', module, flags=re.MULTILINE)
    output_path = os.path.join(destination, fname_out)
    open(output_path,'w').write(module[:-2])
    print(f"Converted {fname} to {output_path}")

LATE_POLICY = \
    """Late Policy:
    
      \"I have read the late policy for CS6424.\"
    """

HONOR_PLEDGE = \
    """Honor Pledge:
    
      \"I have read the Collaboration and Academic Honesty policy for CS6424.
      I certify that I have or will use outside references only in accordance with
      this policy, that I have or will cite any such references via code comments,
      and that I have not or will not copy any portion of my submission from another
      past or current student.\"\n
    """

def require_pledges():
    print(LATE_POLICY)
    ans = input("Please type 'yes' to agree and continue>")
    assert ans.lower() == "yes", "Late policy not accepted"
    print("\n")

    print(HONOR_PLEDGE)
    ans = input("Please type 'yes' to agree and continue>")
    assert ans.lower() == "yes", "Honor pledge not accepted"
    print("\n")

if __name__ == '__main__':
    require_pledges()

    try:
        if (len(sys.argv) > 2): # Warning if extra parameters have been provided
            print("Please note that the notebook will now be submitted to the first directory specified immediately "
                  "after \'helpers/notebook.ipynb\'. Any arguments that come after are ignored.\n")
        folder_location = sys.argv[1]
        os.makedirs(folder_location,exist_ok=True)
        notebook2scriptSingle('/home/notebook/work/Q3.ipynb', folder_location)
    except IndexError:
        print("An error has occurred in trying to export your notebook.ipynb. Please verify "
              "whether you have provided a folder name to the command when running the script. "
              "The format of a proper command is \'python helpers/notebook2script.ipynb path/to/folder\'.")
