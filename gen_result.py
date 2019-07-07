import pandas as pd
import sys, pickle, string, os
import xgboost as xgb
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression, LogisticRegressionCV
from sklearn.preprocessing import StandardScaler
from subprocess import call
from sklearn.datasets import dump_svmlight_file
from sklearn.cross_validation import ShuffleSplit

predictions = {}
for r in range(40):
	print r
	train_data = pd.read_csv("data/train.csv")
	test_data = pd.read_csv("data/test.csv")


	test_user=test_data['user']
	test_merchant=test_data['merchant']

	split = ShuffleSplit(train_data.shape[0], n_iter = 1, test_size=0.16)
	for tr, te in split:
		train1, train2 = tr, te

	train1_data = train_data.iloc[train1,:]
	train2_data = train_data.iloc[train2,:]

	train_label1 = train1_data['label']
	train_label2 = train2_data['label']
	train_label = train_data['label']
	#print train_label
	del train_data['label']
	del train1_data['label']
	del train2_data['label']
	del test_data['label']
	del test_data['user']
	del test_data['merchant']

	dtrain1 = xgb.DMatrix( train1_data.values, label=train_label1.values)
	dtrain2 = xgb.DMatrix( train2_data.values, label=train_label2.values)
	dtest = xgb.DMatrix( test_data.values)


	print "training gbc:tree boosters"
	param = {'bst:max_depth':3, 'bst:eta':0.1, 'silent':1, 'objective':'binary:logistic', 'nthread' : 8, 'eval_metric':'auc' }
	num_round = 125
	bst = xgb.train( param, dtrain1, num_round)

	pred_label_train = bst.predict(dtrain2)
	pred_label_test = bst.predict( dtest )



	
	print "training extra trees forest"
	clf = ExtraTreesClassifier(n_estimators=1000, n_jobs=8,min_samples_split=10)
	clf.fit(train1_data, train_label1)
	pred_label_train2 = clf.predict_proba(train2_data)[:,1]
	pred_label_test2 = clf.predict_proba(test_data)[:,1]

	pred_train = np.hstack(( np.reshape(pred_label_train,(-1,1)), np.reshape(pred_label_train2,(-1,1)) ))
	pred_test = np.hstack(( np.reshape(pred_label_test,(-1,1)), np.reshape(pred_label_test2,(-1,1)) ))
	
	'''
	print "random forest trees forest"
	clf = RandomForestClassifier(n_estimators=100, n_jobs=8,min_samples_split=6)
	clf.fit(train1_data, train_label1)
	pred_label_train4 = clf.predict_proba(train2_data)[:,1]
	pred_label_test4 = clf.predict_proba(test_data)[:,1]

	pred_train = np.hstack(( pred_train, np.reshape(pred_label_train4,(-1,1)) ))
	pred_test = np.hstack(( pred_test, np.reshape(pred_label_test4,(-1,1)) ))
	'''
	print "Gradient Boosting Classifier"
	clf = GradientBoostingClassifier(n_estimators=1000, min_samples_split=10)
	clf.fit(train1_data, train_label1)
	pred_label_train6 = clf.predict_proba(train2_data)[:,1]
	pred_label_test6 = clf.predict_proba(test_data)[:,1]

	pred_train = np.hstack(( np.reshape(pred_label_train,(-1,1)), np.reshape(pred_label_train6,(-1,1)) ))
	pred_test = np.hstack(( np.reshape(pred_label_test,(-1,1)), np.reshape(pred_label_test6,(-1,1)) ))

	#pred_train = np.hstack(( pred_train, np.reshape(pred_label_train6,(-1,1)) ))
	#pred_test = np.hstack(( pred_test, np.reshape(pred_label_test6,(-1,1)) ))




	#vw
	print "Vowpal Wabbit"
	ss = StandardScaler()
	train1_data_norm = ss.fit_transform(train1_data)
	train2_data_norm = ss.transform(train2_data)
	test_data_norm = ss.transform(test_data)


	ntrain1_label = train_label1.copy()
	ntrain1_label.values[np.where(ntrain1_label == 0)] = -1
	ntrain2_label = train_label2.copy()
	ntrain2_label.values[np.where(ntrain2_label == 0)] = -1
	dump_svmlight_file(train1_data, ntrain1_label, "train1.vw", zero_based=False)
	dump_svmlight_file(train2_data, ntrain2_label,"train2.vw", zero_based=False)
	dump_svmlight_file(test_data, np.zeros((test_data_norm.shape[0],)), "test.vw", zero_based=False)
	print 1

	of = open( "vw_train1set.csv" ,"w")
	of2 = open("vw_train2set.csv" ,"w")
	of3 = open("vw_testset.csv" ,"w")
	fi = open("train1.vw","r")
	for lines in fi:
		li = lines.strip().split()
		of.write( li[0] )
		of.write(" | ")
		of.write( string.join(li[1:]," "))
		of.write("\n")
	of.close()
	fi = open("train2.vw", "r")
	for lines in fi:
		li = lines.strip().split()
		of2.write( li[0] )
		of2.write(" | ")
		of2.write( string.join(li[1:]," "))
		of2.write("\n")
	of2.close()
	fi = open("test.vw","r")
	for lines in fi:
		li = lines.strip().split()
		of3.write( "1")
		of3.write(" | ")
		of3.write( string.join(li[1:]," "))
		of3.write("\n")
	of3.close()
	call("vw -c /Users/shen/Desktop/newtry/vw_train1set.csv --passes 100 --loss_function=logistic -f /Users/shen/Desktop/newtry/vw_trainset_model.vw",shell=True)
	call("vw /Users/shen/Desktop/newtry/vw_train2set.csv -t -i /Users/shen/Desktop/newtry/vw_trainset_model.vw  --loss_function=logistic --link=logistic -p /Users/shen/Desktop/newtry/vwpreds_train2.txt", shell=True)
	call("vw /Users/shen/Desktop/newtry/vw_testset.csv -t -i /Users/shen/Desktop/newtry/vw_trainset_model.vw  --loss_function=logistic --link=logistic -p /Users/shen/Desktop/newtry/vwpreds_test.txt", shell=True)
	pred_label_train7 = []
	fi = open( "vwpreds_train2.txt" ,"r")
	for lines in fi:
		li = lines.strip().split()
		pred_label_train7.append(float(li[0]))
	pred_label_test7 = []
	fi.close()
	fi = open( "vwpreds_test.txt" ,"r")
	for lines in fi:
		li = lines.strip().split()
		pred_label_test7.append(float(li[0]))
	pred_train = np.hstack(( pred_train, np.reshape(pred_label_train7,(-1,1)) ))
	pred_test = np.hstack(( pred_test, np.reshape(pred_label_test7,(-1,1)) ))
	fi.close()
	#blend
	#print pred_train234

	clf = GradientBoostingClassifier(n_estimators=25, min_samples_split=10)
	clf.fit(pred_train, train_label2)
	pred_label_test = clf.predict_proba(pred_test)[:,1]
	'''
	dtrain2 = xgb.DMatrix(pred_train, label=train_label2.values)
	dtest = xgb.DMatrix( pred_test )
	
	print "training blend : xgb trees booster logistic regression, max depth 2"
	param = {'bst:max_depth':2, 'bst:eta':0.1, 'silent':1, 'objective':'binary:logistic', 'nthread' : 8, 'eval_metric':'auc' }
	num_round = 50
	bst = xgb.train( param, dtrain2, num_round)

	pred_label1 = bst.predict( dtest )
	
	print "training blend : xgb linear booster logistic regression"
	param = {'booster_type':1, 'bst:lambda':0, 'bst:alpha':0, 'bst:lambda_bias':0, 'silent':1, 'objective':'binary:logistic', 'nthread' : 8, 'eval_metric':'auc' }
	num_round = 25
	bst = xgb.train( param, dtrain2, num_round)
	pred_label2 = bst.predict( dtest )
	'''
	predictions[r]=pred_label_test
	#mean_pred = (pred_label1 + pred_label2)/2.
mean_pred = (predictions[0]+predictions[1]+predictions[2]+predictions[3]+predictions[4]+predictions[5]+predictions[6]+predictions[7]+predictions[8]+predictions[9]+predictions[10]+predictions[11]+predictions[12]+predictions[13]+predictions[14]+predictions[15]+predictions[16]+predictions[17]+predictions[18]+predictions[19]+predictions[20]+predictions[21]+predictions[22]+predictions[23]+predictions[24]+predictions[25]+predictions[26]+predictions[27]+predictions[28]+predictions[29]+predictions[30]+predictions[31]+predictions[32]+predictions[33]+predictions[34]+predictions[35]+predictions[36]+predictions[37]+predictions[38]+predictions[39])/40.
#mean_pred = (predictions[0]+predictions[1]+predictions[2])/3.

of = open("submission.csv","w")
of.write("user_id#merchant_id,prob\n")
for i in range(len(pred_label_test)):
	of.write( str(test_user[i])+'#'+str(test_merchant[i])+','+str(mean_pred[i])+'\n' )


