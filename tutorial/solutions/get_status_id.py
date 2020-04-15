# Solution: While the transfer is still ongoing we will get a status
# code `113` and as soon as it finishes we will get `114`.

taskid = response.json()['task_id']

response = requests.get(
    url=f'{FIRECREST_IP}/tasks/{taskid}',
    headers={'Authorization': f'Bearer {TOKEN}'}
)

handle_response(response)
