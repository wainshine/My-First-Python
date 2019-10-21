# 本代码修改自 https://www.ownthink.com

import sys
import csv

with open('/Users/wainshine/Workman/ownthink_v2.csv', 'r', encoding='utf8') as fin:
    reader = csv.reader(fin)
    for index, read in enumerate(reader):
        print(read)

        if index > 50:
            sys.exit(0)
