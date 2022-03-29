import csv
import os
from ToDo import*

class StorageManager:

    menu =[]

    def __init__(self,filename):
        self.path = filename
        if os.path.isfile(self.path):
            temp = open(self.path)
            temp_r = csv.reader(temp)
            for row in temp_r:
                if row != ['NO.', 'STATUS', 'DEADLINE'.center(17, ' '), 'DESCRIPTION']:
                    tem = []
                    for i, b in enumerate(row):
                        tem.append(str(b).strip())
                    if tem[2] == '-':
                        StorageManager.menu.append(ToDo(tem[3].split(' '), tem[0], True if tem[1] == 'X' else False))
                    else:
                        StorageManager.menu.append(
                            Deadline(tem[3].split(' '), tem[0], tem[2].split('_'), True if tem[1] == 'X' else False))
            temp.close()
        else:
            self.write_csv('')
        return

    def write_csv(self, data):
        temp = open(self.path, 'w', newline='')
        temp_w = csv.writer(temp)
        temp_w.writerow(['NO.', 'STATUS', 'DEADLINE'.center(17, ' '), 'DESCRIPTION'])
        for e in data:
            temp_w.writerow(e.com())
        temp.close()
        return