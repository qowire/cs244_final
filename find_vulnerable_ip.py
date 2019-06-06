import base64
import collections
import json
import os
import pickle

ip_dir = './ip_keys'
vuln_ip_file = 'vulnerable/vulnerable_{}'
vulnerable_file = 'fastgcd-output/vulnerable_moduli'
exponent = 65537

def find_vulnerable_ips(file, vulnerable):
    if '.DS_Store' in file:
        return
    with open(file, 'rb') as f:
        ip_keys_dict = pickle.load(f)

    vulnerable_ips = [k for k, v in ip_keys_dict.items() \
                      if v[0] == exponent and v[1] in vulnerable]
    print('Found {} vulnerable IPs in {}'.format(len(vulnerable_ips), file))
    filename = file[file.rfind('/')+1:]
    with open(vuln_ip_file.format(filename), 'w') as f:
        for ip in vulnerable_ips:
            f.write(ip + '\n')

def base64tohex(base64str):
    return base64.b64decode(base64str).hex()

def hextobase64(hexstr):
    return base64.b64encode(bytes.fromhex(hexstr)).decode('utf-8')

def main():
    with open(vulnerable_file, 'r') as f:
        vulnerable_hex = [line[:-1] for line in f.readlines()]
    # for v in vulnerable:
    #     print(v)
    #     print(len(v))
    #     print(hextobase64(v))
    vulnerable = set([hextobase64(vuln) for vuln in vulnerable_hex])
    print('Found {} vulnerable keys'.format(len(vulnerable)))
    ip_directory = os.fsencode(ip_dir)
    for ip_file in os.listdir(ip_directory):
        ip_filename = os.fsdecode(ip_file)
        print('Finding vulnerable IPs in {}'.format(ip_filename))
        find_vulnerable_ips('{}/{}'.format(ip_dir, ip_filename), vulnerable)

if __name__ == '__main__':
    main()
