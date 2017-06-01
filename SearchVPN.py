#!/usr/bin/python3
import requests.sessions
import json
import sys


if len(sys.argv) == 3:
    # search_keyword could be VPN or IM SKU
    # eg. 1962SBCF200, DP2DVI2, CN6208
    search_keyword = str(sys.argv[1]).lower()
    if str(sys.argv[2]) == "True":
        exactly_search = True
    else:
        exactly_search = False

    url = 'http://us-new.ingrammicro.com/_layouts/CommerceServer/IM/search2.aspx'
    url2 = 'http://us-new.ingrammicro.com/_layouts/CommerceServer/IM/SearchService.svc/Search'
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'
    host = "us-new.ingrammicro.com"
    accept = "text/plain, */*; q=0.01"
    accept_language = "en-US,en;q=0.5"
    accept_encoding = "gzip, deflate"
    content_type = "application/json"
    x_requested_with = "XMLHttpRequest"
    referer = "http://us-new.ingrammicro.com/_layouts/CommerceServer/IM/search2.aspx"
    connection = "keep-alive"
    search_substring = 'Search=%7B%22CookieExpiryDays%22%3A365%2C%22SearchResultsPerPage%22%3A%22100%22%2C%22SearchResultsViewMode%22%3Anull%2C%22OpenedFacets%22%3A%22%22%2C%22CollapsedFacets%22%3A%22%22%2C%22SearchResultsSortBy%22%3A0%7D'
    headers = {'User-Agent': user_agent, 'Host': host, 'Accept':accept, 'Accept-Language': accept_language,
              'Accept-Encoding': accept_encoding, 'Content-Type': content_type, 'X-Requested-With':x_requested_with,
              'Referer': referer, 'Connection': connection}

    # Connect once with website to get an ASP.NET_SessionId
    s = requests.Session()
    s.get(url, headers=headers)
    #print(s.cookies)
    asp_session_id = requests.utils.dict_from_cookiejar(s.cookies).get('ASP.NET_SessionId')


    # Build A Request Cookie By Using existing Session ID
    request_cookie = {'ASP.NET_SessionId': asp_session_id,
                      'AnonymousContact': '43d0b458-eeb6-4640-bfe5-735894eee863',
                      'CMSPreferredCulture': 'en-US',
                      'ReqParam': 'ResellerId=&SalesOrganization=',
                      'CurrentContact': '43d0b458-eeb6-4640-bfe5-735894eee863',
                      'RecentlyViewedProductsGuest': 'PK6407,TH5615',
                      'InStockFilterInd': '',
                      'loadFromBrowserCache': 'false',
                      '_ga': 'GA1.3.552639285.1481595922',
                      '_dc_gtm_UA-57260983-4': '1',
                      'ContactId': 'c4b6bf05-8686-43a3-bc5a-256b4ec32556',
                      'ingrammicro.com': 'ffffffff0904574545525d5f4f58455e445a4a423660',
                      'WT_FPC': 'id=bca72b62-fcd9-4c81-9b98-4d8808867660:lv=1481688387283:ss=1481687753070',
                      'Search': '%7B%22CookieExpiryDays%22%3A365%2C%22SearchResultsPerPage%22%3A100%2C%22SearchResultsViewMode%22%3Anull%2C%22OpenedFacets%22%3A%22%22%2C%22CollapsedFacets%22%3A%22%22%2C%22SearchResultsSortBy%22%3A0%7D'
                      }

    # Build Request Payload
    request_payload = '{"request":{"Keywords":["' + search_keyword + '"],"Page":0,"PageLayout":0,"Mode":0,"Term":"' + search_keyword + '","ExchangeRate":null}}'

    #Build Request Header in Existing Session
    s.headers['Host'] = 'us-new.ingrammicro.com'
    s.headers['Connection'] = 'keep-alive'
    s.headers['Accept'] = 'text/plain, */*; q=0.01'
    s.headers['Origin'] = 'https://us-new.ingrammicro.com'
    s.headers['X-Requested-With'] = 'XMLHttpRequest'
    s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'
    s.headers['Content-Type'] = 'application/json'
    s.headers['Referer'] = 'https://us-new.ingrammicro.com/_layouts/CommerceServer/IM/search2.aspx'
    s.headers['Accept-Encoding'] = 'gzip, deflate, br'
    s.headers['Accept-Language'] = 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'

    # POST query and get feedback
    r = s.post(url2, data=request_payload, cookies=request_cookie)

    # Get Response Data
    response_obj = json.loads(r.content.decode('utf-8'))
    #print(response_obj)

    # Format and Print out the Result
    results_count = response_obj['SearchResult']['ProductSummary']['Data']['Total']

    product_array = response_obj['SearchResult']['ProductSummary']['Data']['Products']

    if results_count == 0:
        print("No Result found!")
    else:
        #print("Find " + str(results_count) + " related Product!")
        results_displayed = 0
        for product in product_array:
            if exactly_search == True:
                if product['Vpn'].lower() == search_keyword or product['SKU'].lower() == search_keyword:
                    print("=====PRODUCT INFO START======")
                    print("SKU: " + product['SKU'])
                    print("VPN: " + product['Vpn'])
                    print("Vendor Name: " + product['Vendor'])
                    print("Category: " + product['Category'])
                    print("SubCategory: " + product['SubCategory'])
                    print("Product Name: " + product['Title'])
                    print("Product Description: " + product['Description'])
                    print("Price: " + product['PriceDataListView']['RRPPrice'])
                    print("Stock Status: " + product['StockStatus'])
                    print("=====PRODUCT INFO END======\n\n")
                    results_displayed += 1
            else:
                if search_keyword in product['Vpn'].lower() or search_keyword in product['SKU'].lower():
                    print("=====PRODUCT INFO START======")
                    print("SKU: " + product['SKU'])
                    print("VPN: " + product['Vpn'])
                    print("Vendor Name: " + product['Vendor'])
                    print("Category: " + product['Category'])
                    print("SubCategory: " + product['SubCategory'])
                    print("Product Name: " + product['Title'])
                    print("Product Description: " + product['Description'])
                    print("Price: " + product['PriceDataListView']['RRPPrice'])
                    print("Stock Status: " + product['StockStatus'])
                    print("=====PRODUCT INFO END======\n\n")
                    results_displayed += 1
        print(str(results_displayed) + " products displayed!")

else:
    print("Please use below format to query the Ingram Micro part!")
    print("         eg.   SearchVPN.py DP2DVI2  <True | False>")
    print("         \"DP2DVI2\" is a VPN (Vendor Part Number) or IM SKU (Ingram Micro SKU) number.")
    print("         True|False means exactly PN search or similar PN search")





