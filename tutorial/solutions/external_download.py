sourcePath = f'/scratch/snx3000/{USER}/{DIR}/small_file.txt'

response = requests.post(
    url=f'{FIRECREST_IP}/storage/xfer-external/download',
    headers={'Authorization': f'Bearer {TOKEN}'},
    data={'sourcePath': sourcePath}
)

tutorial.handle_response(response)
