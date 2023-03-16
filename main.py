import pymongo
import requests
import json

i = 1
offset = 0

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["ai_project"]
mycol = mydb["trendyol"]

product_urls = []
while(True):
	url = "https://public.trendyol.com:443/discovery-web-searchgw-service/v2/api/infinite-scroll/erkek-t-shirt-x-g2-c73?pi="+str(i)+"&culture=tr-TR&userGenderId=1&pId=0&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&fixSlotProductAdsIncluded=true&searchAbDecider=%2CSuggestion_A%2CRelevancy_1%2CFilterRelevancy_1%2CListingScoringAlgorithmId_1%2CSmartlisting_2%2CFlashSales_1%2CSuggestionBadges_B%2CProductGroupTopPerformer_A&offset="+str(offset)
	headers = {"Sec-Ch-Ua": "\"Brave\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"", "Accept": "application/json, text/plain, */*", "Sec-Ch-Ua-Mobile": "?0", "Authorization": "Bearer", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Linux\"", "Sec-Gpc": "1", "Accept-Language": "en-US,en;q=0.6", "Origin": "https://www.trendyol.com", "Sec-Fetch-Site": "same-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Accept-Encoding": "gzip, deflate", "If-None-Match": "W/\"eab6-/qcoADqQInHXa0DL+l016zCl4Zc\""}
	r = requests.get(url, headers=headers)

	try:
		y = json.loads(r.text)
	except:
		break

	for variants in y["result"]["products"]:
		mydict = { "name": "tisort", "price": variants["price"]["sellingPrice"] }
		x = mycol.insert_one(mydict)

	i += 1
	if i % 2 == 0:
		offset += 17
	else:
		offset += 16