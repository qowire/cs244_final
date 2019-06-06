import collections
import json
import os
import pickle

total_ips = 0
rsa_chain_count = 0
other_counts = collections.defaultdict(int)
handshake_successful = set()
keys = {}
algorithms = set()
additional_keys = set()
folder = './outputs'
handshake_successful_filename = 'successful_handshakes'
keys_filename = 'ip2keys'
add_keys_filename = 'additional_keys'

def tupleize_key(key):
    return (key['exponent'], key['modulus'], key['length'])

def get_key(handshake):
    global rsa_chain_count
    if handshake['data']['tls']['status'] != 'success':
        return
    handshake_successful.add(handshake['ip'])
    certs = handshake['data']['tls']['result']['handshake_log']['server_certificates']
    if 'certificate' in certs:
        key_info = certs['certificate']['parsed']['subject_key_info']
        algorithms.add(key_info['key_algorithm']['name'])
        if key_info['key_algorithm']['name'] == 'RSA':
            keys[handshake['ip']] = tupleize_key(key_info['rsa_public_key'])
        else:
            other_counts[key_info['key_algorithm']['name']] += 1
    if 'chain' in certs:
        for cert in certs['chain']:
            key_info = cert['parsed']['subject_key_info']
            if key_info['key_algorithm']['name'] == 'RSA':
                additional_keys.add(tupleize_key(key_info['rsa_public_key']))
                rsa_chain_count += 1

def parse_file(file):
    print('parsing {}'.format(file))
    if 'lost+found' in file or '.DS_Store' in file:
        return
    global total_ips
    handshake_old = len(handshake_successful)
    keys_old = len(keys)
    add_old = len(additional_keys)
    with open(file, 'r') as f:
        line = f.readline()
        cnt = 0
        while line:
            cnt += 1
            handshake = json.loads(line)
            get_key(handshake)
            line = f.readline()

    total_ips += cnt
    print('--------------------------')
    print('File: {}'.format(file))
    print('Num IPs: {}'.format(cnt))
    print('Successful handshakes: {}'.format(len(handshake_successful) - handshake_old))
    print('IPs with RSA keys: {}'.format(len(keys) - keys_old))
    print('Num additional RSA keys: {}'.format(len(additional_keys) - add_old))

def main():
    directory = os.fsencode(folder)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        parse_file('{}/{}'.format(folder, filename))
    with open(handshake_successful_filename, 'wb') as hs_file:
        pickle.dump(handshake_successful, hs_file)
    with open(add_keys_filename, 'wb') as add_keys_file:
        pickle.dump(additional_keys, add_keys_file)
    with open(keys_filename, 'wb') as add_keys_file:
        pickle.dump(keys, add_keys_file)

    print('###############################')
    print('Total IPs: {}'.format(total_ips))
    print('Algorithms:')
    print(algorithms)
    print('Total successful handshakes: {}'.format(len(handshake_successful)))
    print('Total IPs with RSA keys: {}'.format(len(keys)))
    print('Total additional RSA keys: {}'.format(len(additional_keys)))
    print(rsa_chain_count)
    print(other_counts)

if __name__ == '__main__':
    main()