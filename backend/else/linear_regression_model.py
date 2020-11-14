import warnings
from collections import OrderedDict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#線性迴歸模型
#firebase init
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'analyze')
doc_ref_1 = db.collection(u'model').document(u'model')
warnings.filterwarnings('ignore')
#建立資料並檢視資料

# while True: 
while True:
	data_test_left=[]
	data_test_right=[]
	data_real_left=[]
	data_real_right=[]
	docs = doc_ref.get()
	count=0
	for doc in docs:
	    print(doc.id)
	    data_test_right.append(float(doc.to_dict()["right_test"]))
	    data_real_right.append(float(doc.to_dict()["right_real"]))
	    data_test_left.append(float(doc.to_dict()["left_test"]))
	    data_real_left.append(float(doc.to_dict()["left_real"]))
	    count+=1
	print(count)
	data_test=data_test_left+data_test_right
	data_real=data_real_left+data_real_right
	print("資料筆數",count)

	print(data_test)
	print(data_real)
	#實際
	examDict={'實際':data_test,
	          '預估':data_real}

	examOrderedDict=OrderedDict(examDict)
	examDf=pd.DataFrame(examOrderedDict)
	examDf.head()
	#print(np.arange(0.5,5.5,0.25))
	#檢視資料描述統計資訊
	examDf.describe()
	exam_X=examDf['實際']
	exam_y=examDf['預估']
	#散點圖
	#plt.scatter(exam_X,exam_y,color='b',label='考試資料')
	#橫縱軸標籤
	#plt.legend(loc=2)
	#plt.xlabel('real')
	#plt.ylabel('estimate')
	#plt.show()

	#變數間的相關係數
	rDf=examDf.corr()
	print(rDf)

	train_X,test_X,train_y,test_y =train_test_split(exam_X,exam_y,train_size=0.8)
	#輸出訓練集和測試集資料大小
	print('訓練集大小',train_X.shape,train_y.shape)
	print('測試集大小',test_X.shape,test_y.shape)
	train_X=train_X.values.reshape(-1,1)
	train_y=train_y.values.reshape(-1,1)
	test_X=test_X.values.reshape(-1,1)
	test_y=test_y.values.reshape(-1,1)
	print('訓練集大小',train_X.shape,train_y.shape)
	print('測試集大小',test_X.shape,test_y.shape)

	model=LinearRegression()
	model.fit(train_X,train_y)
	rate=round(model.score(test_X,test_y),4)
	print('模型得分為',round(model.score(test_X,test_y),4))

	a=model.intercept_
	b=model.coef_
	print('模型的迴歸方程是:y=%f+%f x'%(a,b))

	doc_ref_1.update({u'rate': str(rate*100), u'intercept':str(a),u'coef': str(b)})