
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'analyze')


while True:
    print("input : real_left")
    a=str(input())
    print("input : test_left")  
    b=str(input())
    print("input : real_right")
    c=str(input())
    print("input : test_right")
    d=str(input())
    if(a=="k" or b=="k" or c=="k" or d=="k"):
        break
    doc_ref.add({
        u'left_real': a,
        u'left_test': b,
        u'right_real': c,
        u'right_test': d
        })
    print("save")



    
'''
新增資料
while True:
    print("input : real_left")
    a=str(input())
    print("input : test_left")  
    b=str(input())
    print("input : real_right")
    c=str(input())
    print("input : test_right")
    d=str(input())
    if(a=="k" or b=="k" or c=="k" or d=="k"):
        break
    
    doc_ref.add({
        u'left_real': a,
        u'left_test': b,
        u'right_real': c,
        u'right_test': d
        })
    print("save")




'''


'''

data 處理

data_test_left=[]
data_test_right=[]
data_real_left=[]
data_real_right=[]
docs = doc_ref.get()
count=0
for doc in docs:
    data_test_right.append(float(doc.to_dict()["right_test"]))
    data_real_right.append(float(doc.to_dict()["right_real"]))
    data_test_left.append(float(doc.to_dict()["left_test"]))
    data_real_left.append(float(doc.to_dict()["left_real"]))
    count+=1
print(count)





data_test=[]
data_real=[]


docs = doc_ref.get()
count=0
for doc in docs:
    data_test.append(float(doc.to_dict()["right_test"]))
    data_real.append(float(doc.to_dict()["right_real"]))
    count+=1

for doc in docs:    
    data_test.append(float(doc.to_dict()["left_test"]))
    data_real.append(float(doc.to_dict()["left_real"]))
    count+=1
'''