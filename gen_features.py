

from datetime import datetime, date
from collections import defaultdict
loc_log = "data/user_log.csv"
loc_train = "data/train_label.csv"
loc_test = "data/test_label.csv"
loc_user="data/user_info.csv"

#loc_reduced = "data/reduced.csv"
loc_out_trainold = "data/trainold.vw"
loc_out_testold = "data/testold.vw"
loc_out_train = "data/train.csv"
loc_out_test = "data/test.csv"

def generate_features(loc_train, loc_test, loc_user, loc_log, loc_out_trainold, loc_out_testold,loc_out_train, loc_out_test):
	#keep a dictionary with the offerdata

	users_train = {}
	users_test={}
	users_info={}
	cats={}
	brands={}
	items={}
	users_log={}
	merchants_log={}
	#a=True
	for e, line in enumerate( open(loc_train) ):
		#a=False
		if e%100000==0:
			print 'loc_train',e
		if e == 0: 
			continue
		row = line.strip().split(",")
		people=row[0].split("#")
		if people[0] not in users_train:
			users_train[people[0]]={}
		if people[0] not in users_log:
			users_log[people[0]]=defaultdict(int)
			users_log[people[0]]['cats']=set()
			users_log[people[0]]['brands']=set()
			users_log[people[0]]['times']=set()
			users_log[people[0]]['items']=set()
		if people[1] not in merchants_log:
			merchants_log[people[1]]=defaultdict(int)
			merchants_log[people[1]]['cats']=set()
			merchants_log[people[1]]['brands']=set()
			merchants_log[people[1]]['times']=set()
			merchants_log[people[1]]['items']=set()
		if people[1] not in users_train[people[0]]:
			users_train[people[0]][people[1]]=defaultdict(int)
			users_train[people[0]][people[1]]['cats']=defaultdict(int)
			users_train[people[0]][people[1]]['brands']=defaultdict(int)
			users_train[people[0]][people[1]]['times']=set()
			users_train[people[0]][people[1]]['items']=defaultdict(int)
			users_train[people[0]][people[1]]['label']='1'if row[1]=='1' else '-1'
	
	for e, line in enumerate( open(loc_test) ):
		#if !a:print "too!\n"
		if e%100000==0:
			print 'loc_test',e
		if e == 0: 
			continue
		row = line.strip().split(",")
		people=row[0].split("#")
		if people[0] not in users_test:
			users_test[people[0]]={}
		if people[0] not in users_log:
			users_log[people[0]]=defaultdict(int)
			users_log[people[0]]['cats']=set()
			users_log[people[0]]['brands']=set()
			users_log[people[0]]['times']=set()
			users_log[people[0]]['items']=set()
		if people[1] not in merchants_log:
			merchants_log[people[1]]=defaultdict(int)
			merchants_log[people[1]]['cats']=set()
			merchants_log[people[1]]['brands']=set()
			merchants_log[people[1]]['times']=set()
			merchants_log[people[1]]['items']=set()
		if people[1] not in users_test[people[0]]:
			users_test[people[0]][people[1]]=defaultdict(int)
			users_test[people[0]][people[1]]['cats']=defaultdict(int)
			users_test[people[0]][people[1]]['brands']=defaultdict(int)
			users_test[people[0]][people[1]]['times']=set()
			users_test[people[0]][people[1]]['items']=defaultdict(int)
	for e, line in enumerate(open(loc_user)):
		if e%100000==0:
			print 'loc_user',e
		if e==0:
			continue
		row=line.strip().split(",")
		users_info[row[0]]={}
		users_info[row[0]]['age_range']=row[1]
		users_info[row[0]]['gender']=row[2]
	#in users_log:{id:{appear:n, action type 1234 num, itemid num, catnum, brandnum }}
	#in merchants_log:{}
	
	#open two output files
	with open(loc_out_trainold, "wb") as out_trainold, open(loc_out_testold, "wb") as out_testold, open(loc_out_train, "wb") as out_train, open(loc_out_test, "wb") as out_test:
		#iterate through reduced dataset 
		#last_id = 0
		#features = defaultdict(float)
		for e, line in enumerate( open(loc_log) ):


			if(e%100000==0):
				print 'saving',e
			if e > 0: #skip header
				#poor man's csv reader
				row = line.strip().split(",")


				if row[4] not in brands:
					brands[row[4]]=defaultdict(int)
				brands[row[4]]['total']+=1
				brands[row[4]][row[0]]+=1
				brands[row[4]][row[3]]+=1

				if row[2] not in cats:
					cats[row[2]]=defaultdict(int)
				cats[row[2]]['total']+=1
				cats[row[2]][row[0]]+=1
				cats[row[2]][row[3]]+=1

				if row[1] not in items:
					items[row[1]]=defaultdict(int)
				items[row[1]]['total']+=1
				items[row[1]][row[0]]+=1
				items[row[1]][row[3]]+=1



				#a=False
				if row[0] in users_log:
					users_log[row[0]]['appear']+=1
					users_log[row[0]]['items'].add(row[1])
					users_log[row[0]]['cats'].add(row[2])
					users_log[row[0]]['brands'].add(row[4])
					users_log[row[0]]['times'].add(row[5])
					users_log[row[0]][row[6]]+=1


				if row[0] in merchants_log:
					merchants_log[row[0]]['appear']+=1
					merchants_log[row[0]]['items'].add(row[1])
					merchants_log[row[0]]['cats'].add(row[2])
					merchants_log[row[0]]['brands'].add(row[4])
					merchants_log[row[0]]['times'].add(row[5])
					merchants_log[row[0]][row[6]]+=1


				if row[0] in users_train and row[3] in users_train[row[0]]:
					#a=True


					if row[6]=='3':
						users_train[row[0]][row[3]]['fourth']+=1
						users_train[row[0]][row[3]]['second']+=1
						users_train[row[0]][row[3]]['third']+=1
						users_train[row[0]][row[3]]['fourth']+=1
					if row[6]=='2':
						users_train[row[0]][row[3]]['first']+=1
						users_train[row[0]][row[3]]['second']+=1
						users_train[row[0]][row[3]]['third']+=1
					if row[6]=='1':
						users_train[row[0]][row[3]]['first']+=1
						users_train[row[0]][row[3]]['second']+=1
					if row[6]=='0':
						users_train[row[0]][row[3]]['first']+=1

					users_train[row[0]][row[3]][row[6]]+=1
					users_train[row[0]][row[3]]['cats'][row[2]]+=1

					users_train[row[0]][row[3]]['brands'][row[4]]+=1
					users_train[row[0]][row[3]]['times'].add(row[5])
					users_train[row[0]][row[3]]['items'][row[1]]+=1

				if row[0] in users_test and row[3] in users_test[row[0]]:

					#if a==True:print "too!\n"
					if row[6]=='3':
						users_test[row[0]][row[3]]['first']+=1
						users_test[row[0]][row[3]]['second']+=1
						users_test[row[0]][row[3]]['third']+=1
						users_test[row[0]][row[3]]['fourth']+=1
					if row[6]=='2':
						users_test[row[0]][row[3]]['first']+=1
						users_test[row[0]][row[3]]['second']+=1
						users_test[row[0]][row[3]]['third']+=1
					if row[6]=='1':
						users_test[row[0]][row[3]]['first']+=1
						users_test[row[0]][row[3]]['second']+=1
					if row[6]=='0':
						users_test[row[0]][row[3]]['first']+=1

					users_test[row[0]][row[3]][row[6]]+=1				
					users_test[row[0]][row[3]]['cats'][row[2]]+=1
					users_test[row[0]][row[3]]['brands'][row[4]]+=1
					users_test[row[0]][row[3]]['times'].add(row[5])
					users_test[row[0]][row[3]]['items'][row[1]]+=1




				#cat_id.add(row[2])
				#brand_id.add(row[4])
				#time_stamp.add(int(row[5]))
		outline = ""
		'''
		for user in users_train:
			user_list=users_train[user]
			for merchant in user_list:
				detail=user_list[merchant]
				if users_log[user]['1']+users_log[user]['2']+users_log[user]['3']==0:
					secondrate=0
				else:
					secondrate=float(detail['1']+detail['2']+detail['3'])/(users_log[user]['1']+users_log[user]['2']+users_log[user]['3'])
				if users_log[user]['2']+users_log[user]['3']==0:
					thirdrate=0
				else:
					thirdrate=float(detail['2']+detail['3'])/(users_log[user]['2']+users_log[user]['3'])
				if users_log[user]['3']==0:
					fourthrate=0
				else:
					fourthrate=float(detail['3'])/(users_log[user]['3'])
				outline=str(detail['label'])+" '"+user+'#'+merchant+" |f"\
				+" gender:"+str(users_info[user]['gender'])\
				+" age_range:"+str(users_info[user]['age_range'])\
				+" action0:"+str(detail['0'])\
				+" action1:"+str(detail['1'])\
				+" action2:"+str(detail['2'])\
				+" action3:"+str(detail['3'])\
				+" first:"+str(detail['first'])\
				+" second:"+str(detail['second'])\
				+" third:"+str(detail['third'])\
				+" fourth:"+str(detail['fourth'])\
				+" firstrate:"+str(float(detail['0']+detail['1']+detail['2']+detail['3'])/(users_log[user]['0']+users_log[user]['1']+users_log[user]['2']+users_log[user]['3']))\
				+" secondrate:"+str(secondrate)\
				+" thirdrate:"+str(thirdrate)\
				+" fourthrate:"+str(fourthrate)\
				+" total_cat:"+str(len(detail['cats']))\
				+" total_brand:"+str(len(detail['brands']))\
				+" total_time:"+str(len(detail['times']))\
				+" total_items:"+str(len(detail['items']))\
				+" users_appear:"+str(users_log[user]['appear'])\
				+" users_items:"+str(len(users_log[user]['items']))\
				+" users_cats:"+str(len(users_log[user]['cats']))\
				+" users_brands:"+str(len(users_log[user]['brands']))\
				+" users_times:"+str(len(users_log[user]['times']))\
				+" users_action0:"+str(users_log[user]['0'])\
				+" users_action1:"+str(users_log[user]['1'])\
				+" users_action2:"+str(users_log[user]['2'])\
				+" users_action3:"+str(users_log[user]['3'])\
				+" merchants_appear:"+str(merchants_log[merchant]['appear'])\
				+" merchants_items:"+str(len(merchants_log[merchant]['items']))\
				+" merchants_cats:"+str(len(merchants_log[merchant]['cats']))\
				+" merchants_brands:"+str(len(merchants_log[merchant]['brands']))\
				+" merchants_times:"+str(len(merchants_log[merchant]['times']))\
				+" merchants_action0:"+str(merchants_log[merchant]['0'])\
				+" merchants_action1:"+str(merchants_log[merchant]['1'])\
				+" merchants_action2:"+str(merchants_log[merchant]['2'])\
				+" merchants_action3:"+str(merchants_log[merchant]['3'])\
				+'\n'
				out_trainold.write(outline)
		for user in users_test:
			user_list=users_test[user]
			for merchant in user_list:
				detail=user_list[merchant]
				if users_log[user]['1']+users_log[user]['2']+users_log[user]['3']==0:
					secondrate=0
				else:
					secondrate=float(detail['1']+detail['2']+detail['3'])/(users_log[user]['1']+users_log[user]['2']+users_log[user]['3'])
				if users_log[user]['2']+users_log[user]['3']==0:
					thirdrate=0
				else:
					thirdrate=float(detail['2']+detail['3'])/(users_log[user]['2']+users_log[user]['3'])
				if users_log[user]['3']==0:
					fourthrate=0
				else:
					fourthrate=float(detail['3'])/(users_log[user]['3'])
				outline="1 '"+user+'#'+merchant+" |f"\
				+" gender:"+str(users_info[user]['gender'])\
				+" age_range:"+str(users_info[user]['age_range'])\
				+" action0:"+str(detail['0'])\
				+" action1:"+str(detail['1'])\
				+" action2:"+str(detail['2'])\
				+" action3:"+str(detail['3'])\
				+" first:"+str(detail['first'])\
				+" second:"+str(detail['second'])\
				+" third:"+str(detail['third'])\
				+" fourth:"+str(detail['fourth'])\
				+" firstrate:"+str(float(detail['0']+detail['1']+detail['2']+detail['3'])/(users_log[user]['0']+users_log[user]['1']+users_log[user]['2']+users_log[user]['3']))\
				+" secondrate:"+str(secondrate)\
				+" thirdrate:"+str(thirdrate)\
				+" fourthrate:"+str(fourthrate)\
				+" total_cat:"+str(len(detail['cats']))\
				+" total_brand:"+str(len(detail['brands']))\
				+" total_time:"+str(len(detail['times']))\
				+" total_items:"+str(len(detail['items']))\
				+" users_appear:"+str(users_log[user]['appear'])\
				+" users_items:"+str(len(users_log[user]['items']))\
				+" users_cats:"+str(len(users_log[user]['cats']))\
				+" users_brands:"+str(len(users_log[user]['brands']))\
				+" users_times:"+str(len(users_log[user]['times']))\
				+" users_action0:"+str(users_log[user]['0'])\
				+" users_action1:"+str(users_log[user]['1'])\
				+" users_action2:"+str(users_log[user]['2'])\
				+" users_action3:"+str(users_log[user]['3'])\
				+" merchants_appear:"+str(merchants_log[merchant]['appear'])\
				+" merchants_items:"+str(len(merchants_log[merchant]['items']))\
				+" merchants_cats:"+str(len(merchants_log[merchant]['cats']))\
				+" merchants_brands:"+str(len(merchants_log[merchant]['brands']))\
				+" merchants_times:"+str(len(merchants_log[merchant]['times']))\
				+" merchants_action0:"+str(merchants_log[merchant]['0'])\
				+" merchants_action1:"+str(merchants_log[merchant]['1'])\
				+" merchants_action2:"+str(merchants_log[merchant]['2'])\
				+" merchants_action3:"+str(merchants_log[merchant]['3'])\
				+'\n'
				out_testold.write(outline)
		
		'''

		out_train.write("label,gender,age_range,action0,action1,action2,action3,first,second,third,fourth,total_cat,total_brand,total_time,total_items,users_appear,users_items,users_cats,users_brands,users_times,users_action0,users_action1,users_action2,users_action3,merchants_appear,merchants_items,merchants_cats,merchants_brands,merchants_times,merchants_action0,merchants_action1,merchants_action2,merchants_action3,mer_brandrate,mer_catrate,cus_brandrate,cus_catrate\n")
		
		for user in users_train:
			user_list=users_train[user]
			for merchant in user_list:
				detail=user_list[merchant]
				if users_log[user]['1']+users_log[user]['2']+users_log[user]['3']==0:
					secondrate=0
				else:
					secondrate=float(detail['1']+detail['2']+detail['3'])/(users_log[user]['1']+users_log[user]['2']+users_log[user]['3'])
				if users_log[user]['2']+users_log[user]['3']==0:
					thirdrate=0
				else:
					thirdrate=float(detail['2']+detail['3'])/(users_log[user]['2']+users_log[user]['3'])
				if users_log[user]['3']==0:
					fourthrate=0
				else:
					fourthrate=float(detail['3'])/(users_log[user]['3'])

				allbrand=0
				thisbrand=0
				for brand in detail['brands']:
					allbrand+=brands[brand]['total']
					thisbrand+=brands[brand][merchant]
				mer_brandrate=float(thisbrand)/allbrand
				if mer_brandrate<0.0001:
					mer_brandrate=0

				allcat=0
				thiscat=0
				for cat in detail['cats']:
					allcat+=cats[cat]['total']
					thiscat+=cats[cat][merchant]
				mer_catrate=float(thiscat)/allcat
				if mer_catrate<0.0001:
					mer_catrate=0

				allbrand=0
				thisbrand=0
				for brand in detail['brands']:
					allbrand+=brands[brand][user]
					thisbrand+=detail['brands'][brand]
				cus_brandrate=float(thisbrand)/allbrand
				if cus_brandrate<0.0001:
					cus_brandrate=0

				allcat=0
				thiscat=0
				for cat in detail['cats']:
					allcat+=cats[cat][user]
					thiscat+=detail['cats'][cat]
				cus_catrate=float(thiscat)/allcat
				if cus_catrate<0.0001:
					cus_catrate=0


				allbrand=0
				thisbrand=0
				for brand in detail['brands']:
					allbrand+=brands[brand][merchant]
					thisbrand+=detail['brands'][brand]
				cus2_brandrate=float(thisbrand)/allbrand
				if cus2_brandrate<0.0001:
					cus2_brandrate=0

				allcat=0
				thiscat=0
				for cat in detail['cats']:
					allcat+=cats[cat][merchant]
					thiscat+=detail['cats'][cat]
				cus2_catrate=float(thiscat)/allcat
				if cus2_catrate<0.0001:
					cus2_catrate=0



				outline=str((int(detail['label'])+1)/2)+","\
				+str(users_info[user]['gender'])+","\
				+str(users_info[user]['age_range'])+","\
				+str(detail['0'])+","\
				+str(detail['1'])+","\
				+str(detail['2'])+","\
				+str(detail['3'])+","\
				+str(detail['first'])+","\
				+str(detail['second'])+","\
				+str(detail['third'])+","\
				+str(detail['fourth'])+","\
				+str(len(detail['cats']))+","\
				+str(len(detail['brands']))+","\
				+str(len(detail['times']))+","\
				+str(len(detail['items']))+","\
				+str(users_log[user]['appear'])+","\
				+str(len(users_log[user]['items']))+","\
				+str(len(users_log[user]['cats']))+","\
				+str(len(users_log[user]['brands']))+","\
				+str(len(users_log[user]['times']))+","\
				+str(users_log[user]['0'])+","\
				+str(users_log[user]['1'])+","\
				+str(users_log[user]['2'])+","\
				+str(users_log[user]['3'])+","\
				+str(merchants_log[merchant]['appear'])+","\
				+str(len(merchants_log[merchant]['items']))+","\
				+str(len(merchants_log[merchant]['cats']))+","\
				+str(len(merchants_log[merchant]['brands']))+","\
				+str(len(merchants_log[merchant]['times']))+","\
				+str(merchants_log[merchant]['0'])+","\
				+str(merchants_log[merchant]['1'])+","\
				+str(merchants_log[merchant]['2'])+","\
				+str(merchants_log[merchant]['3'])+","\
				+str(mer_brandrate)+","\
				+str(mer_catrate)+","\
				+str(cus_brandrate)+","\
				+str(cus_catrate)\
				+'\n'
				
				out_train.write(outline)

		out_test.write("label,user,merchant,gender,age_range,action0,action1,action2,action3,first,second,third,fourth,total_cat,total_brand,total_time,total_items,users_appear,users_items,users_cats,users_brands,users_times,users_action0,users_action1,users_action2,users_action3,merchants_appear,merchants_items,merchants_cats,merchants_brands,merchants_times,merchants_action0,merchants_action1,merchants_action2,merchants_action3,mer_brandrate,mer_catrate,cus_brandrate,cus_catrate\n")
		for user in users_test:
			user_list=users_test[user]
			for merchant in user_list:
				detail=user_list[merchant]
				if users_log[user]['1']+users_log[user]['2']+users_log[user]['3']==0:
					secondrate=0
				else:
					secondrate=float(detail['1']+detail['2']+detail['3'])/(users_log[user]['1']+users_log[user]['2']+users_log[user]['3'])
				if users_log[user]['2']+users_log[user]['3']==0:
					thirdrate=0
				else:
					thirdrate=float(detail['2']+detail['3'])/(users_log[user]['2']+users_log[user]['3'])
				if users_log[user]['3']==0:
					fourthrate=0
				else:
					fourthrate=float(detail['3'])/(users_log[user]['3'])



				allbrand=0
				thisbrand=0
				for brand in detail['brands']:
					allbrand+=brands[brand]['total']
					thisbrand+=brands[brand][merchant]
				mer_brandrate=float(thisbrand)/allbrand
				if mer_brandrate<0.0001:
					mer_brandrate=0

				allcat=0
				thiscat=0
				for cat in detail['cats']:
					allcat+=cats[cat]['total']
					thiscat+=cats[cat][merchant]
				mer_catrate=float(thiscat)/allcat
				if mer_catrate<0.0001:
					mer_catrate=0

				allbrand=0
				thisbrand=0
				for brand in detail['brands']:
					allbrand+=brands[brand][user]
					thisbrand+=detail['brands'][brand]
				cus_brandrate=float(thisbrand)/allbrand
				if cus_brandrate<0.0001:
					cus_brandrate=0

				allcat=0
				thiscat=0
				for cat in detail['cats']:
					allcat+=cats[cat][user]
					thiscat+=detail['cats'][cat]
				cus_catrate=float(thiscat)/allcat
				if cus_catrate<0.0001:
					cus_catrate=0


				allbrand=0
				thisbrand=0
				for brand in detail['brands']:
					allbrand+=brands[brand][merchant]
					thisbrand+=detail['brands'][brand]
				cus2_brandrate=float(thisbrand)/allbrand
				if cus2_brandrate<0.0001:
					cus2_brandrate=0

				allcat=0
				thiscat=0
				for cat in detail['cats']:
					allcat+=cats[cat][merchant]
					thiscat+=detail['cats'][cat]
				cus2_catrate=float(thiscat)/allcat
				if cus2_catrate<0.0001:
					cus2_catrate=0



				outline=str(1)+","\
				+user+","\
				+merchant+","\
				+str(users_info[user]['gender'])+","\
				+str(users_info[user]['age_range'])+","\
				+str(detail['0'])+","\
				+str(detail['1'])+","\
				+str(detail['2'])+","\
				+str(detail['3'])+","\
				+str(detail['first'])+","\
				+str(detail['second'])+","\
				+str(detail['third'])+","\
				+str(detail['fourth'])+","\
				+str(len(detail['cats']))+","\
				+str(len(detail['brands']))+","\
				+str(len(detail['times']))+","\
				+str(len(detail['items']))+","\
				+str(users_log[user]['appear'])+","\
				+str(len(users_log[user]['items']))+","\
				+str(len(users_log[user]['cats']))+","\
				+str(len(users_log[user]['brands']))+","\
				+str(len(users_log[user]['times']))+","\
				+str(users_log[user]['0'])+","\
				+str(users_log[user]['1'])+","\
				+str(users_log[user]['2'])+","\
				+str(users_log[user]['3'])+","\
				+str(merchants_log[merchant]['appear'])+","\
				+str(len(merchants_log[merchant]['items']))+","\
				+str(len(merchants_log[merchant]['cats']))+","\
				+str(len(merchants_log[merchant]['brands']))+","\
				+str(len(merchants_log[merchant]['times']))+","\
				+str(merchants_log[merchant]['0'])+","\
				+str(merchants_log[merchant]['1'])+","\
				+str(merchants_log[merchant]['2'])+","\
				+str(merchants_log[merchant]['3'])+","\
				+str(mer_brandrate)+","\
				+str(mer_catrate)+","\
				+str(cus_brandrate)+","\
				+str(cus_catrate)\
				+'\n'
				
				out_test.write(outline)
		
	#print min(time_stamp),max(time_stamp)


					
#generate_features(loc_train, loc_test, loc_transactions, loc_out_train, loc_out_test)


if __name__ == '__main__':
	#reduce_data(loc_offers, loc_transactions, loc_reduced)
	generate_features(loc_train, loc_test, loc_user, loc_log, loc_out_trainold, loc_out_testold,loc_out_train,loc_out_test)

	
	
