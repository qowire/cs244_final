import base64
import collections
import json
import os
import pickle

ip_dir = './ip_keys'
add_dir = './additional'
moduli_file = 'exp-{}-moduli'

def add_ip_keys(file, keys):
    if '.DS_Store' in file:
        return
    with open(file, 'rb') as f:
        ip_keys_dict = pickle.load(f)
    ip_keys_ls = [v for k, v in ip_keys_dict.items()]
    keys.update(ip_keys_ls)

def add_add_keys(file, keys):
    if '.DS_Store' in file:
        return
    with open(file, 'rb') as f:
        add_keys_set = pickle.load(f)
    keys.update(add_keys_set)

def base64tohex(base64str):
    return base64.b64decode(base64str).hex()

def main():
    keys = set()
    ip_directory = os.fsencode(ip_dir)
    for ip_file in os.listdir(ip_directory):
        ip_filename = os.fsdecode(ip_file)
        print('add ips for {}'.format(ip_filename))
        add_ip_keys('{}/{}'.format(ip_dir, ip_filename), keys)
    add_directory = os.fsencode(add_dir)
    for add_file in os.listdir(add_directory):
        add_filename = os.fsdecode(add_file)
        print('add additional for {}'.format(add_filename))
        add_add_keys('{}/{}'.format(add_dir, add_filename), keys)

    print('Number of keys: {}'.format(len(keys)))
    keys = list(keys)
    lengths = collections.defaultdict(set)
    moduli = collections.defaultdict(set)
    for key in keys:
        exp, mod, leng = key
        lengths[exp].add(leng)
        moduli[exp].add(mod)
    for exp in moduli:
        print('--------------------')
        print('Exponent {}'.format(exp))
        print('Moduli lengths: {}'.format(lengths[exp]))
        print('Num moduli: {}'.format(len(moduli[exp])))
        with open(moduli_file.format(exp), 'w') as f:
            for mod in moduli[exp]:
                f.write(base64tohex(mod) + '\n')

if __name__ == '__main__':
    main()