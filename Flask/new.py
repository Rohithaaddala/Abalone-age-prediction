import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "WUzKWUPzFMMiKG8MxA1E0WY7ivhdPWH1zu8dEeqgcCyl"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field": [["Sex","Length","Height","Whole weight","Shucked weight","Viscera weight","Shell weight"]], 
                                   "values": [[2,0.455,0.365,0.095,0.514,0.2254,0.101,0.15]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/095fd9ce-8575-417f-b4e4-2db7d9d50dba/predictions?version=2022-08-07', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
predictions=response_scoring.json()
pred=predictions['predictions'][0]['values'][0][0]
if(pred==1):
    print("it will not get exited")
else:
    print("it gets exited")