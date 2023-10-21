import requests
import re
import yaml

def load_ordered_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data

def dump_ordered_yaml(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True, sort_keys=False)

# Đọc tệp YAML với bảo toàn thứ tự
config = load_ordered_yaml('config.yaml')

# Cập nhật các domain thành địa chỉ IP
for proxy in config['proxies']:
    domain_name = proxy['server']
    try:
        print(domain_name)
        response = requests.get(f"https://checkip.com.vn/locator?host={domain_name}")
        content = response.text
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', content)
        
        try:
            proxy['server'] = ip[1]
            print(proxy['server'])
        except IndexError:
            print(f"Insufficient IP addresses found for {domain_name}")
    except requests.exceptions.RequestException:
        pass

# Ghi lại tệp config đã cập nhật
dump_ordered_yaml(config, 'config.yaml')

