all_tasks_response = requests.get(
    url=f'{FIRECREST_IP}/tasks/',
    headers={'Authorization': f'Bearer {TOKEN}'}
)

tutorial.handle_response(all_tasks_response)
