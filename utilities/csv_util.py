'''
Created on May 31, 2018

@author: Natty
'''
import csv

#takes a two column csv and puts it into a {col1: col2} dict 
def read_csv_to_dict (filename):
    '''
    '''
    access_dict = {}
    with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for rows in reader:
                access_dict[rows[0]] = rows[1]
    return access_dict
    
# Take a dictionary and writes it out to a csv file with col1=key, col2=value    
def write_dict_to_csv (dictionary, filename):
    '''
    '''
    with open(filename, 'wb') as csvfile:
            #fieldnames = ['key', 'value']
            
            #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer = csv.writer(csvfile)
            for key, value in dictionary.iteritems():
                writer.writerow([key, value])

if __name__ == '__main__':
    pass