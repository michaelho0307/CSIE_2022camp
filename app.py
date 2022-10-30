import streamlit as st
import requests
def getAllBookstore():
	url = 'https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=M' # 在這裡輸入目標 url
	headers = {"accept": "application/json"}
	response = requests.get(url, headers=headers)
	# 將 response 轉換成 json 格式
	res = response.json()
	# 回傳值
	return res
def getCountyOption(items):
# 創建一個空的 List 並命名為 optionList
	optionList = []
	for item in items:
		# 把 cityname 欄位中的縣市名稱擷取出來 並指定給變數 name
		# hint: 想辦法處理 item['cityName'] 的內容
		name = item['cityName'][0:3]
		# 如果 name 不在 optionList 之中，便把它放入 optionList
		# hint: 使用 if-else 來進行判斷 / 用 append 把東西放入 optionList
		if name not in optionList:
			optionList.append(name)
	return optionList
def getDistrictOption(items, target):
	optionList = []
	for item in items:
		name = item['cityName']
		# 如果 name 裡面不包含我們選取的縣市名稱(target) 則略過該次迭代
		# hint: 使用 if-else 判斷式並且用 continue 跳過
		if target not in name: continue
		name.strip()
		district = name[5:]
		if len(district) == 0: continue
		# 如果 district 不在 optionList 裡面，將 district 放入 optionList
		# hint: 使用 if-else 判斷式並使用 append 將內容放入 optionList
		if district not in optionList:
			optionList.append(district)
	return optionList
def getSpecificBookstore(items, county, districts):
	specificBookstoreList = []
	for item in items:
		name = item['cityName']
		# 如果 name 不是我們選取的 county 則跳過
		# hint: 用 if-else 判斷並用 continue 跳過
		if county not in name: continue
		# districts 是一個 list 結構，判斷 list 每個值是否出現在 name 之中
		# 判斷該項目是否已經出現在 specificBookstoreList 之中，沒有則放入
		# hint: 用 for-loop 進行迭代，用 if-else 判斷，用 append 放入
		for district in districts:
			if district not in name: continue
			specificBookstoreList.append(item)
	return specificBookstoreList
def getBookstoreInfo(items):
	expanderList = []
	for item in items:
		expander = st.expander(item['name'])
		expander.image(item['representImage'])
		expander.metric('hitRate', item['hitRate'])
		expander.subheader('Introduction')
		# 用 st.write 呈現書店的 Introduction
		expander.write(item['intro'])
		expander.subheader('Address')
		# 用 st.write 呈現書店的 Address
		expander.write(item['address'])
		expander.subheader('Open Time')
		# 用 st.write 呈現書店的 Open Time
		expander.write(item['openTime'])
		expander.subheader('Email')
		# 用 st.write 呈現書店的 Email
		expander.write(item['email'])
		# 將該 expander 放到 expanderList 中
		expanderList.append(expander)
	return expanderList
def app():
	# 呼叫 getAllBookstore 函式並將其賦值給變數 bookstoreList
	bookstoreList =  getAllBookstore()
	# 呼叫 getCountyOption 並將回傳值賦值給變數 countyOption
	countyOption = getCountyOption(bookstoreList)
	st.header('特色書店地圖')
	st.metric('Total bookstore', len(bookstoreList))
	county = st.selectbox('請選擇縣市', countyOption)
	# 呼叫 getDistrictOption 並將回傳值賦值給變數 districtOption
	districtOption = getDistrictOption(bookstoreList, county)
	district = st.multiselect('請選擇區域', districtOption)

	# 呼叫 getSpecificBookstore 並將回傳值賦值給變數 specificBookstore
	specificBookstore = getSpecificBookstore(bookstoreList, county, district)
	num = len(specificBookstore)
	# 用 st.write 將目標書店的總數量計算出來，格式：總共有3項結果
	st.write(f'總共有{num}項結果')
	#step 6 1 line
	specificBookstore.sort(key = lambda item: item['hitRate'], reverse=True)
	# 呼叫 getBookstoreInfo 並將回傳值賦值給變數 bookstoreInfo
	bookstoreInfo = getBookstoreInfo(specificBookstore)
if __name__ == '__main__':
    app()

# import requests
# url = 'https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=M'
# headers = {"accept":"application/json"}
# response = requests.get(url,headers=headers)
# res = response.json()
# #print(res)
# #print(response)
# print(type(res))