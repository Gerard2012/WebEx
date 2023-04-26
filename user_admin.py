##############################################################################################
# modules
##############################################################################################

import requests
import json
import csv
import time


##############################################################################################
# Global Variables & Config
##############################################################################################

token = input('SERVICE APP TOKEN: ')
input_file = input('INPUT CSV FILE: ')
error_file = f'ERROR-LOG-{time.strftime("%X")}_' + input_file

with open(error_file, 'a') as f:
    f.write('email,error\n')
    print(f'ERROR FILE CREATED: {error_file}')

base_url = 'https://webexapis.com/v1/'
payload = {}
headers = {'Authorization': f'Bearer {token}'}


##############################################################################################
# Functions
##############################################################################################

def get_person_id(email):

    url = base_url + f'people?email={email}'

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.ok:
        if json.loads(response.text)['items']:
            person_id =  json.loads(response.text)['items'][0]['id']
            return email, person_id
        else:
            with open(error_file, 'a') as f:
                f.write(f'{email},get_person_id({response.status_code}: User not found)\n')
            return email, False
    else:
        with open(error_file, 'a') as f:
            f.write(f'{email},get_person_id({response.status_code})\n')
        return


##############################################################################################

def get_auth_id(user_tuple):

    if not user_tuple:
        
        pass

    elif not user_tuple[1]:

        pass

    else:

        auth_ids = []

        url = base_url + f'authorizations?personId={user_tuple[1]}'

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.ok:

            if 'items' in json.loads(response.text):
                
                for item in json.loads(response.text)['items']:
                    if item['applicationName'] == 'Webex Teams Desktop Client for Windows':
                        auth_ids.append((user_tuple[0], item['id']))

        else:
            with open(error_file, 'a') as f:
                f.write(f'{user_tuple[0]},get_auth_id({response.status_code})\n')


        return auth_ids


##############################################################################################

def delete_auth_id(auth_ids):

    if not auth_ids:
        pass

    else:

        list(auth_ids)

        for auth_id in auth_ids:
            
            url = base_url + f'authorizations/{auth_id[1]}'

            response = requests.request("DELETE", url, headers=headers, data=payload)

            if not response.ok:
                with open(error_file, 'a') as f:
                    f.write(f'{auth_id[0]},delete_auth_id({response.status_code})\n')

        print(f'<<<< {auth_id[0]}: {len(auth_ids)} X AUTH IDS DELETED >>>>')


##############################################################################################
# Run
##############################################################################################


if __name__ == '__main__':

    with open(input_file) as f:
        user_emails = [row['email'] for row in csv.DictReader(f)]

    start = time.perf_counter()

    print(f'<<<< SCRIPT STARTED: @ {time.strftime("%X")} >>>>\n')

    try:

        for email in user_emails:
            delete_auth_id(get_auth_id(get_person_id(email)))

        finish = time.perf_counter()
        print(f'<<<< SCRIPT COMPLETE: @ {time.strftime("%X")} IN {round(finish-start, 2)} SECONDS >>>>\n')

    except KeyboardInterrupt:
        print('<<<< QUITTING SCRIPT !!! >>>>')