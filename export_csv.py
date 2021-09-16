import os
import re
import csv

def export_csv():
    list_file = []
    for file in os.listdir(r"Data"):
        if file.endswith(".png"):
            list_file.append(file)
    a = ','.join(list_file)
    StudentID = re.findall('(\d{7})',a)
    FullName= re.findall('\d{7}_(.+?)_\w{2}',a)
    Code= re.findall('\d{7}_.+?_(\w{2})',a)

    split_name =[]
    for name in FullName:
        x  = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', name)
        split_name.append(x)

    Surname = [x[0] for x in split_name]
    FirstName = [' '.join(x[1:]) for x in split_name]

    col = ['StudentID','Surname','FirstName','Code','sheetName']
    row = list(zip(StudentID,Surname,FirstName,Code,list_file))

    with open ('student.csv','w') as f:
        writer =csv.writer(f)
        writer.writerow(col)
        writer.writerows(row)
    print('---------------------')
    print('Export CSV completed')
    return