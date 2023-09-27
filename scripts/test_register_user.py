import requests

api_url = 'http://localhost:8000/api/register_user/'  # Replace with your server's URL

data = {
    'aadhar_id': '123456789012',  
    'name': 'John Doe',
    'email': 'john@example.com',
    'annual_income': 50000
}

response = requests.post(api_url, json=data)

if response.status_code == 200:
    print('User registration successful.')
else:
    print('User registration failed.')
    print('Response:', response.status_code, response.json())
