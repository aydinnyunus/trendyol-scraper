import pymongo
import requests
import json

i = 1
offset = 0
cat_id = -1


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["ai_project"]
mycol = mydb["trendyol"]

product_urls = ["erkek-gomlek-x-g2-c75","kadin-gomlek-x-g1-c75", "erkek-t-shirt-x-g2-c73", "kadin-t-shirt-x-g1-c73", "erkek-pantolon-x-g2-c70", "kadin-pantolon-x-g1-c70", "erkek-ceket-x-g2-c1030", "kadin-ceket-x-g1-c1030",
				"erkek-mont-x-g2-c118", "kadin-mont-x-g1-c118", "erkek-sort-x-g2-c119", "erkek-saat-x-g2-c34", "kadin-saat-x-g1-c34",  "erkek-gunes-gozlugu-x-g2-c105", "erkek-cuzdan-x-g2-c1032", "kadin-cuzdan-x-g1-c1032",
				"erkek-kemer-x-g2-c1093", "erkek-sapka-x-g2-c1181",  "kadin-sapka-x-g1-c1181", "erkek-boxer-x-g2-c61", "erkek-corap-x-g2-c1038", "kadin-corap-x-g1-c1038",
				"elbise-x-c56", "etek-x-c69", "kadin-spor-tayt-x-g1-c101460",
				"laptop-x-c103108", "cep-telefonu-x-c103498", "televizyon-x-c104156" ]
categories = ["gomlek", "gomlek", "tisort", "tisort", "pantolon", "pantolon", "ceket","ceket", "mont","mont","sort", "saat", "saat", "gozluk", "cuzdan","cuzdan", "kemer", "sapka", "sapka", "boxer", "corap","corap", "elbise", "etek", "tayt", "laptop", "cep telefonu", "televizyon"]


for urls in product_urls:
	cat_id += 1
	offset = 0
	i = 1
	while(True):
		url = "https://public.trendyol.com:443/discovery-web-searchgw-service/v2/api/infinite-scroll/"+urls+"?pi="+str(i)+"&culture=tr-TR&userGenderId=1&pId=0&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&fixSlotProductAdsIncluded=true&searchAbDecider=%2CSuggestion_A%2CRelevancy_1%2CFilterRelevancy_1%2CListingScoringAlgorithmId_1%2CSmartlisting_2%2CFlashSales_1%2CSuggestionBadges_B%2CProductGroupTopPerformer_A&offset="+str(offset)
		headers = {"Sec-Ch-Ua": "\"Brave\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"", "Accept": "application/json, text/plain, */*", "Sec-Ch-Ua-Mobile": "?0", "Authorization": "Bearer", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Linux\"", "Sec-Gpc": "1", "Accept-Language": "en-US,en;q=0.6", "Origin": "https://www.trendyol.com", "Sec-Fetch-Site": "same-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Accept-Encoding": "gzip, deflate", "If-None-Match": "W/\"eab6-/qcoADqQInHXa0DL+l016zCl4Zc\""}
		r = requests.get(url, headers=headers)
		#print(url)
		try:
			y = json.loads(r.text)
			t = y["result"]["products"]
		except:
			break

		for variants in y["result"]["products"]:
			mydict = { "name": categories[cat_id], "price": variants["price"]["sellingPrice"], "brand": variants["brand"]["name"]}
			
			for var in variants["variants"]:
				mydict["size"] = var["attributeValue"]
			
			if "ratingScore" in variants:
					mydict["ratingScore"] = variants["ratingScore"]["averageRating"]
			else:
					mydict["ratingScore"] = "NULL"
				

			x = mycol.insert_one(mydict)
			print(mydict)

		i += 1
		if i % 2 == 0:
			offset += 17
		else:
			offset += 16



