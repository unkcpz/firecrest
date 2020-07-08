response = requests.get(
    url=f'{FIRECREST_IP}/tasks/',
    headers={'Authorization': f'Bearer {TOKEN}'}
)

tutorial.handle_response(response)
