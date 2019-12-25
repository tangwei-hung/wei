# The input format of the list of integers is like 1 2 3 4 5 6 
user_number_list=list(map(int,input('Please enter the integers numbers:').split()))

pairs_number=[]
for i in range(len(user_number_list)):
    for j in user_number_list[i:]:
        first_num=user_number_list[i]
        second_num=j
        if (first_num*second_num % 2) == 0 and ((first_num+second_num) % 2)==1:
            pairs_number.append((first_num,second_num))

print(pairs_number)
