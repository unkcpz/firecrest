response = requests.get(
    url=f'{FIRECREST_IP}/tasks/',
    headers={'Authorization': f'Bearer {TOKEN}'}
)

handle_response(response)
