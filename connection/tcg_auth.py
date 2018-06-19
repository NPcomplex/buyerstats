'''
Created on May 26, 2018

@author: Natty
'''
import requests
import json
import time
from utilities import *

class TcgApiAuthenticator:

    public_key = None
    private_key = None
    access_token = None
    application_id = None
    base_url = None
    
    def __init__(self, auth_filename):
        auth_dict = self.populate_auth_data(auth_filename)
        self.public_key = auth_dict['public_key']
        self.private_key = auth_dict['private_key']
        self.access_token = auth_dict['access_token']
        self.application_id = auth_dict['application_id']
        self.base_url = auth_dict['base_url']
    
    def populate_auth_data(self, auth_filename):
        auth_dict = read_csv_to_dict (auth_filename)
        return auth_dict
        
    def authorize_application(self):
        
        head= {"Accept":"application/x-www-form-urlencoded",
                "Content-type": "application/x-www-form-urlencoded",
                "X-Tcg-Access-Token": self.access_token}
        data_binary = "grant_type=client_credentials&client_id=" + self.public_key + "&client_secret=" + self.private_key
        ret = requests.post(self.base_url + 'token', headers = head, data = data_binary)
        json_data = json.loads(ret.text)
        return json_data
    
    def get_access_data(self):
        access_dict = {}
        try:
            access_dict = read_csv_to_dict('access_data.csv')
        except:
            print 'Error reading access data file. Querying new access data.'
            
        expiriation_time = access_dict.get('expiration_time')
        
        #This could fail still on the time.time check since it might expire while we are processing later
        #That is ok since we can just make sure to re-authenticate if we fail a call on auth
        #I could use the .expires field instead of doing the math
        if (expiriation_time is None) or (int(expiriation_time) < int(time.time())): 
            access_dict = self.authorize_application()
            access_dict['expiration_time'] = access_dict['expires_in'] + int(time.time())
            write_dict_to_csv(access_dict, 'access_data.csv')
        
        return access_dict
        

if __name__ == "__main__":
    tcg_authenticator = TcgApiAuthenticator(r'C:\development\TCGPlayer_api\buyer_stats\tcg_auth.csv')
    print str(tcg_authenticator.get_access_data())      

'''
curl --include --request POST \
--header "application/x-www-form-urlencoded" \
--header "X-Tcg-Access-Token: 2DB5276D-4889-4B8E-8D2D-4CC16C2F18E1" \
--data-binary "grant_type=client_credentials&client_id=1CA06C84-6364-498B-9D7F-EB02F589704A&client_secret=D8209A97-B699-462C-9C87-7CA17AE4DF17" \
'''

