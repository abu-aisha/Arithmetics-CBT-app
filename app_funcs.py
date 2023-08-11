import random

def gen_quests(operators,level,q_no):

    if level ==1:
        low_bound = 0
        up_bound = 10
    elif level ==2:
        low_bound = 0
        up_bound = 100
    elif level ==3:
        low_bound = -100
        up_bound = 100
    else:
        return "Invalid level"

    question_ans_dict = {}
    unq_quests_count = 0
    while unq_quests_count <q_no:
        operator = random.choice(operators)
        if operator == 'mul':
            b = random.randint(low_bound,up_bound)
            a = random.randint(low_bound,up_bound)
            ans = a*b

            Qvals_list = [a,operator,b]
            question_ans_dict[ans] =  Qvals_list
        elif operator == 'div':
            Ans_is_whole = False
            while not Ans_is_whole:
                if level == 3:
                    # Avoiding zero division error 
                    b_iszero = True
                    while b_iszero:
                        b = random.randint(low_bound,up_bound)  
                        a = random.randint(low_bound,up_bound) 
                        if b != 0:
                            b_iszero = False
                else:
                    b = random.randint(1,up_bound)  # Avoiding zero division error 
                    a = random.randint(low_bound,up_bound) 

                ans = a/b
                decimal = str(ans).split('.')[1]
                if decimal== '0' and ans >=0:
                    Ans_is_whole = True
                else:
                    Ans_is_whole = False
            Qvals_list = [a,operator,b]
            question_ans_dict[int(ans)] =  Qvals_list
        elif operator == 'add':
            b = random.randint(low_bound,up_bound)
            a = random.randint(low_bound,up_bound)
            ans = a+b
            Qvals_list = [a,operator,b]
            question_ans_dict[ans] =  Qvals_list
        elif operator == 'substr':
            if level == 3:
                b = random.randint(low_bound,up_bound)
                a = random.randint(low_bound,up_bound)
            else:
                b = random.randint(low_bound,up_bound)
                a = random.randint(b,up_bound)
            ans = a-b
            Qvals_list = [a,operator,b]
            question_ans_dict[ans] =  Qvals_list

            # If they are the same question they will definitely have the same answers but 
            # having the same answers does not mean they are the same questions
        ### Counting unique questions
        temp1_list = [''.join([str(b) for b in ii]) for ii in question_ans_dict.values()]
        unq_quests_count =len(set(temp1_list))

    return question_ans_dict
