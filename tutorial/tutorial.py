import ipywidgets as wg
from IPython.display import display, Image, Markdown
import glob
import json


# This function is useful only to print the response in a nicer way
def handle_response(response):
    print("\nResponse status code:")
    print(response.status_code)
    print("\nResponse headers:")
    print(json.dumps(dict(response.headers), indent=4))
    print("\nResponse json:")
    try:
        print(json.dumps(response.json(), indent=4))
    except json.JSONDecodeError:
        print("-")


def external_upload_bold_markdown(index=-1):
    markdown_status_str = "Status Code | Description\n" ":---: | :---\n"
    status = ["100", "110", "111", "112", "113", "114", "115"]
    descriptions = [
        "Queued",
        "Waiting for Form URL from Object Storage to be retrieved",
        "Form URL from Object Storage received",
        "Object Storage confirms that upload to Object Storage has finished",
        "Download from Object Storage to server has started",
        "Download from Object Storage to server has finished",
        "Download from Object Storage error",
    ]

    for i, s in enumerate(status):
        if i == index:
            markdown_status_str += f"**{status[i]}** | **{descriptions[i]}**\n"
        else:
            markdown_status_str += f"{status[i]} | {descriptions[i]}\n"

    return markdown_status_str


def external_download_bold_markdown(index=-1):
    markdown_status_str = "Status Code | Description\n" ":---: | :---\n"
    status = ["100", "116", "117", "118"]
    descriptions = [
        "Queued",
        "Started upload from filesystem to Object Storage",
        "Upload from filesystem to Object Storage has finished succesfully",
        "Upload from filesystem to Object Storage has finished with errors",
    ]

    for i, s in enumerate(status):
        if i == index:
            markdown_status_str += f"**{status[i]}** | **{descriptions[i]}**\n"
        else:
            markdown_status_str += f"{status[i]} | {descriptions[i]}\n"

    return markdown_status_str


def compute_bold_markdown(index=-1):
    markdown_status_str = "Status Code | Description\n" ":---: | :---\n"
    status = ["100", "101", "200", "400"]
    descriptions = [
        "Queued",
        "In progress",
        "Finished successfully",
        "Finished with error",
    ]

    for i, s in enumerate(status):
        if i == index:
            markdown_status_str += f"**{status[i]}** | **{descriptions[i]}**\n"
        else:
            markdown_status_str += f"{status[i]} | {descriptions[i]}\n"

    return markdown_status_str


markdown_strs = {
    "utilities_upload": [
        "- This is a `POST` request.\n"
        "- The file has to be smaller than **5MB**.\n"
        "- The request is blocking, FirecREST will reply to the client when the upload is finished.\n"
    ],
    "external_upload": [
        "* For files >5MB we have to use the Storage Microservice.\n"
        "* We will upload the file through a staging area (more information [here](https://user.cscs.ch/storage/object_storage/)).\n"
        "* We keep track of the task through a FirecREST task and its status:\n\n",
        external_upload_bold_markdown(0),
        external_upload_bold_markdown(1),
        external_upload_bold_markdown(2),
        external_upload_bold_markdown(3),
        external_upload_bold_markdown(4),
        external_upload_bold_markdown(5),
        external_upload_bold_markdown(),
    ],
    "external_download": [
        "* For files >5MB we have to use the Storage Microservice.\n"
        "* We will dwonload the file through a staging area.\n"
        "* We keep track of the task through a FirecREST task and its status:\n\n",
        external_download_bold_markdown(0),
        external_download_bold_markdown(1),
        external_download_bold_markdown(2),
        external_download_bold_markdown(),
    ],
    "compute_sbatch": [
        (
            "The goal of this section is to learn how to perform the following actions through FirecREST:\n"
            "1. Submit a job successfully\n"
            "2. Check the status of the job on the scheduler\n"
        ),
        (
            "**Slurm's job ID**\n"
            "- unique identifier of a slurm job\n"
            "- it is created by Slurm when the job is submitted\n"
            "- it can be used to track the state of the job with calls like `squeue` or `sacct`\n"
            "\n"
            "**FirecREST's task ID**\n"
            "- unique identifier of a FirecREST task\n"
            "- it is created and updated by FirecREST when the first call regarding this task is created\n"
            "- it can be used to track the state of the task with the API call we will see later in this section\n"
            "\n"
            "FirecREST creates a task for every operation with the scheduler.\n"
        ),
        (
            "**Task 1**: `sbatch script.sh`\n"
            "\n"
            "**A. We make a request to FirecREST to submit the job.**\n"
        ),
        ("\n" "This will create a FirecREST task.\n\n"),
        compute_bold_markdown(0),
        compute_bold_markdown(1),
        compute_bold_markdown(2),
        (
            "\n"
            "We will only get the task ID from the response.\n\n"
            "To find out if the job was actually submitted to Slurm we have to make another request.\n"
        ),
        (
            "\n"
            "**B. We check the status of the task and make sure we got status code 200.**\n"
        ),
    ],
    "compute_squeue": [
        (
            "**Task 2**: `squeue -j <jobid>`\n"
            "\n"
            "**A. We make a request to FirecREST to poll for the job.**\n"
        ),
        ("\n" "This will create a FirecREST task.\n\n"),
        compute_bold_markdown(0),
        compute_bold_markdown(1),
        compute_bold_markdown(2),
        ("\n" "We will only get the task ID from the response.\n\n"),
        (
            "\n"
            "**B. Just like before, we have make a second request to get Slurm's response.**\n"
        ),
    ],
}

markdown_steps = {
    "utilities_upload": [[1, 2, 3, 4]],
    "external_upload": [
        list(range(1, 16)),
        [3, 4],
        [5],
        [6, 7, 8, 9, 10],
        [11],
        [12],
        [13, 14],
        [0, 1, 2, 15],
    ],
    "external_download": [list(range(1, 16)), [3, 4], [5], [6, 7, 8], [1, 2, 9]],
    "compute_sbatch": [
        [1],
        [2],
        [3, 4, 5, 6, 7, 8, 9, 10, 11],
        [4, 5, 6, 7, 8, 9, 10],
        [4, 5],
        [6, 7],
        [8, 9, 10],
        [8, 9, 10],
        [9, 10, 11],
    ],
    "compute_squeue": [
        [1, 2, 3, 4, 5, 6, 7, 8],
        [2, 3, 4, 5, 6, 7],
        [2, 3],
        [4],
        [5, 6, 7],
        [3, 4, 5, 6, 7],
        [6, 7, 8],
    ],
}


def show(x):
    def show_figure(step):
        return display(Image(filename=f"images/{x}/{x} {step}.jpeg", width="100%"))

    def markdown_explanation(step):
        markdown_str = ""
        for s, steps in zip(markdown_strs[x], markdown_steps[x]):
            if step in steps:
                markdown_str += s

        return display(Markdown(markdown_str))

    slider = wg.IntSlider(
        min=1, max=len(glob.glob(f"images/{x}/*")), layout=wg.Layout(width="100%")
    )
    slideshow = wg.Box(
        [wg.interactive_output(show_figure, {"step": slider})],
        layout=wg.Layout(width="70%"),
    )
    description = wg.Box(
        [wg.interactive_output(markdown_explanation, {"step": slider})],
        layout=wg.Layout(
            width="30%", justify_content="center", display="flex", align_items="stretch"
        ),
    )
    ui = wg.Box([slideshow, description])

    display(slider, ui)
