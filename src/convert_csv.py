import pickle
import csv

keys = pickle.load(open('d_chain_keys.pkl', 'rb'))
print(len(keys))
with open('d_chain_keys.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(['Exponent', 'Modulus', 'Length'])
    for key in keys:
        csvwriter.writerow(key)