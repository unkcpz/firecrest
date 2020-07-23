# Solution: While the transfer is still ongoing we will get a status
# code `113` and as soon as it finishes we will get `114`.

taskid = upload_response.json()['task']['hash_id']

upload_task_response = requests.get(
    url=f'{FIRECREST_IP}/tasks/{taskid}',
    headers={'Authorization': f'Bearer {TOKEN}'}
)

tutorial.handle_response(upload_task_response)
