import requests
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
           'Chrome/51.0.2704.63 Safari/537.36'}
BASE_URL = "http://www.dmh8.com/"
for i in range(10):
    url = "http://www.dmh8.com/list/" +str(1+i)+"&dq=%B4%F3%C2%BD&pl=time"
    response = requests.get(url, headers=headers)
    print(response.encoding)
    response.encoding = "GBK"
    data = response.text
    pattern_href = re.compile(r'<a href="[^(http)](.+?)"[> ]')
    end_place = 0

    relative_urls = re.findall(pattern_href, data)
    for each in relative_urls:
        if not each.startswith("http"):
            place = data.find(each, end_place)
            new_url = BASE_URL+each
            data = data[:place-1] + new_url + data[place+len(each):]
            # 记录这个位置，之后的下一次替换从已经替换的位置之后开始
            end_place = place + len(new_url)
            # print(data[place:place+len(each)])
            print(f"{each}->{BASE_URL}{each}")

    file_path = "/Users/yekse/Desktop/bit/bit -大三上/big data analysis/webcrawler/樱花国漫第" + str(i + 1) + "页.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data)
