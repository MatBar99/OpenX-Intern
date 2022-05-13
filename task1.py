import urllib.request
import json 
import ssl

''' 
The main idea behind this program is to visit every 'sellers.json' page that can be 
opened by using urllib library. The next step after visiting page is to collect 
all domain names that have certain "seller_type" value.   
'''
ssl._create_default_https_context = ssl._create_unverified_context 

def check_address(domain_name): 
    url_address = f"https://{domain_name}/sellers.json"
    req = urllib.request.Request(url_address)
    try:
        response = urllib.request.urlopen(req, timeout=1)
    except Exception as e:
        print(e)
    else:
        return url_address

def load_file(domain_name):
    url_adress = check_address(domain_name)
    if (url_adress):
        try:
            with urllib.request.urlopen(url_adress, timeout=1) as url:
                data = json.loads(url.read())
        except Exception as e:
            print(e)
        else:
            return data 

def find_sellers(data):
    sellers_list = []
    if (data is not None and "sellers" in data):
        for seller in data["sellers"]:
            if (seller["seller_type"] == "INTERMEDIARY" or seller["seller_type"] == "BOTH"):
                try:
                    sellers_list.append(seller['domain'])
                except Exception as e:
                    print(e)
                    continue
            sellers_list = list(dict.fromkeys(sellers_list)) #clearing empty lists
        return sellers_list
    else:
        return []

def create_chain_tree(data, start_path, results, file):
    datas = load_file(data)
    direct_sellers = find_sellers(datas)
    if len(direct_sellers) > 20:
            direct_sellers = direct_sellers[:20] # reduction used to show that method works without finding all parameters
    if len(direct_sellers) > 0:
        for i in direct_sellers:
            if i in start_path: # quick fix for problems with infinite looping
                break
            path = f"{start_path}|{i}"
            results.append(path)
            file.write(path + '\n')
            create_chain_tree(i, path, results, file)

    return results    


if __name__ == "__main__":
    results = []

    with open('paths.txt', 'w') as file:
        tree = create_chain_tree("openx.com", "OpenX.com --> ", results, file)
        print(tree)
