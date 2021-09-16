import cv2
import numpy as np
import imutils
from imutils import contours
from pandas.core.frame import DataFrame
import pandas as pd
import re
import csv



def One_Student_Result(sheetName):
    StudentID = re.findall('(\d{7})',sheetName)
    FullName= re.findall('\d{7}_(.+?)_\w{2}',sheetName)
    x1,x2,y1,y2=0,0,0,0
    questions = 5
    answers = 5
    total_solution_ans = [0,2,3,3,1,#1->5
                        1,2,3,2,2,#6>10
                        1,2,3,0,0,#11->15
                        1,1,2,3,2,#16->20
                        1,2,2,3,4,#21->25
                        2,3,3,2,4,#26->30
                        2,0,1,0,4,#31->35
                        4,3,2,2,3,#36->40
                        2,3,4,3,2,#41->45
                        1,1,0,0,2,#46->50
                        1,3,4,4,4,#51->55
                        0,0,1,3,2]#56->60
    dict_difference = {}
    dict_answer = {}
    dict_student_ans = {}
    i_pos = 0
    total_student_ans = []
    for i_pos in range(0,12):
        image =cv2.imread(sheetName)
        doc1 = image.copy()
        x1,x2 = 148,275
        if i_pos > 5:
            ipos = i_pos//5
            y1,y2= 480,710
        else:
            ipos = i_pos
            y1,y2 = 120,350
        correct_ans = total_solution_ans[(ipos*5):(ipos*5)+5]
        student_ans = []

        x1 += 137*ipos
        x2 += 137*ipos
        image = image[x1:x2,y1:y2,:]

        image = imutils.resize(image,height=500,width=500)
                    
        gray_doc = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur_doc = cv2.GaussianBlur(gray_doc, (5,5), 0)
        edge_doc = cv2.Canny(blur_doc, 75, 200)
        grade_cnt= cv2.findContours(edge_doc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        grade_cnt= imutils.grab_contours(grade_cnt)

        paper = image
        warped = gray_doc
        masked = image
        gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)
        # split the thresholded image into boxes
        def split_image(image):
            # make the number of rows and columns 
            # a multiple of 5 (questions = answers = 5)
            r = len(image) // questions * questions 
            c = len(image[0]) // answers * answers
            image = image[:r, :c]
            # split the image horizontally (row-wise)
            rows = np.vsplit(image, questions)
            boxes = []
            for row in rows:
                # split each row vertically (column-wise)
                cols = np.hsplit(row, answers)
                for box in cols:
                    boxes.append(box)
            return boxes

        boxes = split_image(thresh)
        
        score = 0
        green = (0,255,0)
        red = (255,0,0)
        # loop over the questions
        for i in range(0, questions):
            user_answer = None
            
            # loop over the answers
            for j in range(answers):
                pixels = cv2.countNonZero(boxes[j + i * 5])
                # if the current answer has a larger number of 
                # non-zero (white) pixels then the previous one
                # we update the `user_answer` variable
                if user_answer is None or pixels > user_answer[1]:
                    user_answer = (j, pixels)
                    ans = j

            # find the contours of the bubble that the user has filled
            cnt, _ = cv2.findContours(boxes[user_answer[0] + i * 5], 
                                            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            student_ans.append(ans)
            total_student_ans.append(ans)
            
        correct_ans = [chr(x+65) for x in correct_ans]
        student_ans = [chr(x+65) for x in student_ans]
        for indx, item in enumerate(correct_ans):
            dict_answer[f'question: {indx+1 + i_pos*5}'] = item
        for indx, item in enumerate(student_ans):
            dict_student_ans[f'{indx+1 + i_pos*5}'] = item

    dict_total_ans = {}
    total_solution_ans = [chr(x+65) for x in total_solution_ans]
    total_student_ans = [chr(x+65) for x in total_student_ans]
    for indx, item in enumerate(total_solution_ans):
        dict_total_ans[f'{indx+1}'] = item

    for indx, item in enumerate(total_student_ans):
        if item != total_solution_ans[indx]:
            dict_difference[f'{indx+1}'] = item
   
    list_wrong_answer = ','.join(dict_difference.keys())
    grade = round(len(list_wrong_answer)/60,2)
    #export image
    # cv2.imshow(f'The answer of student: {FullName} -{StudentID}',doc1)
    # cv2.waitKey(10) 
    ###return###
    return dict_total_ans,dict_student_ans,dict_difference,list_wrong_answer,grade

def first_five_answer(sheetName):
    StudentID = re.findall('(\d{7})',sheetName)
    FullName= re.findall('\d{7}_(.+?)_\w{2}',sheetName)
    questions = 5
    answers = 5
    correct_ans = [0,2,3,3,1]
    student_ans = []

    #read student sheet
    image =cv2.imread(f'Data\{sheetName}')
    # image =cv2.imread('2000113_NguyenBaoNgan_3A.png')
    image = image[150:275,120:350,:]
    #image = image[147:270,:400,:]
    image = imutils.resize(image,height=500,width=500)
                
    gray_doc = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_doc = cv2.GaussianBlur(gray_doc, (5,5), 0)
    edge_doc = cv2.Canny(blur_doc, 75, 200)
    grade_cnt= cv2.findContours(edge_doc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    grade_cnt= imutils.grab_contours(grade_cnt)



    paper = image
    warped = gray_doc
    masked = image
    gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)
    doc_copy1 = image.copy()

    # split the thresholded image into boxes
    def split_image(image):
        # make the number of rows and columns 
        # a multiple of 5 (questions = answers = 5)
        r = len(image) // questions * questions 
        c = len(image[0]) // answers * answers
        image = image[:r, :c]
        # split the image horizontally (row-wise)
        rows = np.vsplit(image, questions)
        boxes = []
        for row in rows:
            # split each row vertically (column-wise)
            cols = np.hsplit(row, answers)
            for box in cols:
                boxes.append(box)
        return boxes

    boxes = split_image(thresh)
    
    score = 0
    green = (0,255,0)
    red = (255,0,0)
    # loop over the questions
    for i in range(0, questions):
        user_answer = None
        
        # loop over the answers
        for j in range(answers):
            pixels = cv2.countNonZero(boxes[j + i * 5])
            # if the current answer has a larger number of 
            # non-zero (white) pixels then the previous one
            # we update the `user_answer` variable
            if user_answer is None or pixels > user_answer[1]:
                user_answer = (j, pixels)
                ans = j

        # find the contours of the bubble that the user has filled
        cnt, _ = cv2.findContours(boxes[user_answer[0] + i * 5], 
                                        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        student_ans.append(ans)

    dict_difference = {}
    dict_answer = {}
    dict_student_ans = {}
    correct_ans = [chr(x+65) for x in correct_ans]
    student_ans = [chr(x+65) for x in student_ans]
    for indx, item in enumerate(correct_ans):
        dict_answer[f'question: {indx+1}'] = item
    for indx, item in enumerate(student_ans):
        dict_student_ans[f'question: {indx+1}'] = item

    for indx, item in enumerate(student_ans):
        if item != correct_ans[indx]:
            dict_difference[f'question: {indx+1}'] = item
            
    #export image
    cv2.imshow(f'First Five Question Student: {FullName} -{StudentID}',thresh)
    cv2.waitKey(100)            
    return dict_answer, dict_student_ans, dict_difference


