import os
import re
import csv
import pandas as pd
import function
import time
import export_csv

def generate_grading(df:pd.DataFrame):
    # df = pd.read_csv('student.csv')
    list_student = df['sheetName'].tolist()
    list_grade =[]
    i = 0
    answer_wrong = []
    
    while i < len(list_student):
        item = 'Data\\'+ list_student[i]
        # print(item)
        list_grade.append(function.One_Student_Result(item)[4])
        answer_wrong.append(function.One_Student_Result(item)[3])
        i +=1
        
    df['Grade'] = list_grade
    df['Pass/Fail'] = df['Grade'].apply(lambda x: 'fail' if x < 2 else 'pass')
    grading = df[['StudentID','Grade']]
    final_result = df[['StudentID','Surname','FirstName','Code','Grade','Pass/Fail']]

    final_result.to_csv('exam_result',index=False)
    
    return grading,answer_wrong,final_result
        
    # return answer_wrong,grading,final_result

def show_menu():
    # chạy menu theo 4 option, nếu chọn 99 là sẽ thoát chương trình
    print("Choose an option:")
    menu_program = {1: '1. Generating Data from Data Folder and export file "student.csv" ',
                    2: "2. Generating first 5 answer of student (please input StudentID)",
                    3: "3. Generating all answers of one student (please input StudentID)",
                    4: "4. Generating grading.csv (StudentID, Grading)",
                    5: "5. Summary which 3 questions are the most difficult",
                    6: "6. Generating the final result (pass/fail) of the class",
                    8: "...",
                    9: "99. Exit"
                    }
    for y in menu_program:
        print(menu_program[y])

    a = input("Choose an option (Menu from 1 -> 6, exit: 99):")
    x = int(a)
    while x != 99:
        print('You CHOOSED: ' + menu_program[x])
        if x == 1:
            try:
                export_csv.export_csv()
                
                a = input("Choose an option (Menu from 1 -> 6, exit: 99):")
                x = int(a)
                
            except IOError:
                print("Please choose correct number ")   
        elif x ==2:
            try:
                list_file = []
                for file in os.listdir(r"Data"):
                    if file.endswith(".png"):
                        list_file.append(file)
                
                for index, file in enumerate(list_file):
                    print(f'{index}. {file}')
                    time.sleep(0.05)
                print('Please choose list student as above(from 0 to 49):')
                selected = input()
                check = selected.isnumeric()
                while check ==True:
                    sheetNo = list_file[int(selected)]
                    print(f'You choose {sheetNo}')
                    print('-------------------')
                    print("First 5 Correct Answer")
                    dict = function.first_five_answer(sheetNo)[0]
                    for key in dict:
                        print(f'Question {key} -> Correct Answere: {dict[key]}')
                        time.sleep(0.1)
                        
                    print('-------------------')
                    print("First 5 Student's Answer")
                    dict = function.first_five_answer(sheetNo)[1]
                    for key in dict:
                        print(f"Question {key} -> Student's Answered: {dict[key]}")
                        time.sleep(0.1)
                        
                    print('-------------------')
                    print("Questions Student didn't asnwer correct:")
                    dict = function.first_five_answer(sheetNo)[2]
                    for key in dict:
                        print(f"Question {key} -> Student's Answered (Incorrect): {dict[key]}")
                        time.sleep(0.1)                                  
                    break
  
                a = input("Choose an option (Menu from 1 -> 6, exit: 99):")
                x = int(a)                
            except IOError:
                print("Please choose correct number ")                 
            
        elif x == 3:
            try:
                list_file = []
                for file in os.listdir(r"Data"):
                    if file.endswith(".png"):
                        list_file.append(file)
                
                for index, file in enumerate(list_file):
                    print(f'{index}. {file}')
                    time.sleep(0.05)
                print('Please choose list student as above(from 0 to 49):')
                selected = input()
                check = selected.isnumeric()
                while check ==True:
                    sheetNo = list_file[int(selected)]
                    
                    print(f'You choose {sheetNo}')
                    print('-------------------')
                    print("Total 60 Correct Answers")
                    sheetNo = f'Data\{sheetNo}'
                    dict = function.One_Student_Result(sheetNo)[0]
                    for key in dict:
                        print(f'Question {key} -> Correct Answer: {dict[key]}')
                        time.sleep(0.1)
                        
                    print('-------------------')
                    print("Total 60 Student's Answers")
                    dict = function.One_Student_Result(sheetNo)[1]
                    for key in dict:
                        print(f"Question {key} -> Student's Answered: {dict[key]}")
                        time.sleep(0.1)
                        
                    print('-------------------')
                    print("Questions Student didn't asnwer correct:")
                    dict = function.One_Student_Result(sheetNo)[2]
                    for key in dict:
                        print(f"Question {key} -> Student's Answered (Incorrect): {dict[key]}")
                        time.sleep(0.1) 
                    grade = function.One_Student_Result(sheetNo)[4]
                    Name = sheetNo[5:]
                    print(f'{Name} Total True Answer: {60-len(dict)}/60')
                    print(f'Total grade: {grade}') 
                    break
                    
                a = input("Choose an option (Menu from 1 -> 6, exit: 99):")
                x = int(a) 
                           
            except IOError:
                print("Please choose correct number ") 
        elif x == 4:
            df = pd.read_csv('student.csv')
            grading = generate_grading(df)[0]
            
            grading.to_csv('grading.csv',index=False)
            print('-------------------------')
            print("completed exporting file 'grading.csv'!!!")
            
            a = input("Choose an option (Menu from 1 -> 6, exit: 99):")
            x = int(a) 
        elif x == 5:
            df = pd.read_csv('student.csv')
            answer_wrong =  generate_grading(df)[1]
            b = ','.join(answer_wrong)
            import re
            pattern = '(\d{1,2})'
            x = re.findall(pattern,b)
            from collections import Counter
            # print(Counter(x))
            result =  Counter(x).most_common(3)
            print('-------------------------')
            print('Top 3 answer difficult most')
            print(f'question {result[0][0]} ({result[0][1]} students answer wrong) ')
            print(f'question {result[1][0]} ({result[1][1]} students answer wrong) ')
            print(f'question {result[2][0]} ({result[2][1]} students answer wrong) ')
            
            a = input("Choose an option (Menu from 1 -> 6, exit: 99):")
            x = int(a)               
            
        elif x == 6:
            df = pd.read_csv('student.csv')
            grading = generate_grading(df)[2]
            
            grading.to_csv('final_result.csv',index=False)
            print('-------------------------')
            print("completed exporting file 'final_result.csv'!!!")
            a = input("Choose an option (Menu from 1 -> 6, exit: 99):")
            x = int(a)              
        elif x == 99:
            print('Exit')
            exit()
        else:
            print('NOT correct,Please input again')
            for y in menu_program:
                print(menu_program[y])
            a = input("Choose an option (Menu from 1 -> 6, exit: 99):")
            x = int(a)   
    else:
        print('Exit Program!!!')
        exit()


# Đọc file kết hợp tách ra file riêng để xem toàn bộ chi tiết file theo tháng hoặc năm mình cần, khi đã chạy lần đầu xong cho data của năm và tháng đó thì sử dụng đọc file đã tách được có kích thước nhỏ hơn cho những lần chạy sau để tiết kiệm thời gian chạy.
if __name__ == '__main__':
    show_menu()