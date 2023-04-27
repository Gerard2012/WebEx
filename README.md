# WebEx

## Using the Script  


Drop a CSV file into same directory as user_admin.py script using WinSCP.

CSV file should have a single header, "email", and user emails listed beneath this as seen in example below:

email,  
gerard.rambo@acme.com,  
james.fluffer@acme.com,  
barry.humphries@acme.com,  
<br/><br/>


You will asked for the file name when running the script as well as the Service App Bearer token.
See example below:

```
root@server:~/linux_repos/WebEx$ python3 user_admin.py  
SERVICE APP TOKEN: ZjkwNDdkZGQtMDk3Zi00ZTdmLThlMDMtMGVjZTFkZDk2ZDkzYjFmYmRhOTctMjMx_PE93_d348f36a-b4f4-4ae3-9978-9549b1d5db95  
INPUT CSV FILE: test_users.csv  
ERROR FILE CREATED: ERROR-LOG-14:33:55_test_users.csv  
```
<br/><br/>



An error file is created into which details of any failed API runs will be written. This error file is also in CSV format:

email,error  
james.fluffer@acme.com,get_auth_id(401)  
barry.humphries@acme.com,get_person_id(200: User not found)  
