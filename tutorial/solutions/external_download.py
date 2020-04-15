sourcePath = '/home/llama/res.txt'

response = requests.post(
    url=f'{FIRECREST_IP}/storage/xfer-external/download',
    headers={'Authorization': f'Bearer {TOKEN}'},
    data={'sourcePath': sourcePath}
)

handle_response(response)
