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

def show_utilities():
    def show_figure(step):
        return display(
            Image(
                filename=f"images/utilities_upload/utilities_upload {step}.jpeg", width="100%"
            )
        )

    def markdown_explanation(step):
        markdown_str = (
            "- This is a `POST` request.\n"
            "- The file has to be smaller than **5MB**.\n"
            "- The request is blocking, FirecREST will reply to the client when the upload is finished.\n"
        )

        return display(Markdown(markdown_str))

    slider = wg.IntSlider(min=1, max=3, step=len(glob.glob('images/utilities_upload/')), layout=wg.Layout(width="100%"))
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


def show_compute_sbatch():
    def show_figure(step):
        return display(
            Image(filename=f"images/compute_sbatch/compute_sbatch {step}.jpeg", width="100%")
        )

    def markdown_explanation(step):
        markdown_table_str = "Status Code | Description\n" ":---: | :---\n"
        status = ["100", "101", "200", "400"]
        descriptions = ["QUEUED", "PROGRESS", "SUCCESS", "ERROR"]
        bold_status = [[3, 4, 5], [6, 7], [8, 9, 10], [], [], []]

        for i in range(len(status)):
            if step in bold_status[i]:
                markdown_table_str += f"**{status[i]}** | **{descriptions[i]}**\n"
            else:
                markdown_table_str += f"{status[i]} | {descriptions[i]}\n"

        markdown_1 = [
            ("The goal of this section is to learn how to perform the following actions through FirecREST:\n"
             "1. Submit a job successfully\n"
             "2. Check the status of the job on the scheduler\n"),
        ]
        markdown_2 = [
            ("**Slurm's job ID**\n"
             "- unique identifier of a slurm job\n"
             "- it is created by Slurm when the job is submitted\n"
             "- it can be used to track the state of the job with calls like `squeue` or `sacct`\n"
             "\n"
             "**FirecREST's task ID**\n"
             "- unique identifier of a FirecREST task\n"
             "- it is created and updated by FirecREST when the first call regarding this task is created\n"
             "- it can be used to track the state of the task with the API call we will see later in this section\n"
             "\n"
             "FirecREST creates a task for every operation with the scheduler.\n")
        ]
        markdown_3 = [
            ("**Task 1**: `sbatch script.sh`\n"
             "\n"
             "**A. We make a request to FirecREST to submit the job.**\n"),
            ("\n" "This will create a FirecREST task.\n\n" + markdown_table_str),
            ("\n"
             "We will only get the task ID from the response.\n\n"
             "To find out if the job was actually submitted to Slurm we have to make another request.\n"),
            ("\n"
             "**B. We check the status of the task and make sure we got status code 200.**\n")
        ]
        markdown_3_steps = [2, 3, 4, 8]

        if step in [1]:
            markdown_str = markdown_1[0]
        elif step in [2]:
            markdown_str = markdown_2[0]
        elif step in range(3, 11):
            lim = markdown_3_steps.index(max([x for x in markdown_3_steps if x <= step]))
            markdown_str = "".join(markdown_3[:lim])
        else:
            markdown_str = ""

        return display(Markdown(markdown_str))

    slider = wg.IntSlider(min=1, max=len(glob.glob("images/compute_sbatch/*")), step=1, layout=wg.Layout(width="100%"))
    slideshow = wg.Box(
        [wg.interactive_output(show_figure, {"step": slider})],
        layout=wg.Layout(width="70%"),
    )
    description = wg.Box(
        [wg.interactive_output(markdown_explanation, {"step": slider})],
        layout=wg.Layout(width="30%", justify_content="center"),
    )
    ui = wg.Box([slideshow, description])

    display(slider, ui)

def show_compute_squeue():
    def show_figure(step):
        return display(
            Image(filename=f"images/compute/tutorial_{step}.jpeg", width="100%")
        )

    def markdown_explanation(step):
        markdown_table_str = "Status Code | Description\n" ":---: | :---\n"
        status = ["100", "101", "200", "300", "301", "400"]
        descriptions = ["QUEUED", "PROGRESS", "SUCCESS", "DELETED", "EXPIRED", "ERROR"]
        bold_status = [[2, 3, 4, 11, 12], [5, 6, 13], [7, 8, 9, 14, 15, 16], [], [], []]

        for i in range(len(status)):
            if step in bold_status[i]:
                markdown_table_str += f"**{status[i]}** | **{descriptions[i]}**\n"
            else:
                markdown_table_str += f"{status[i]} | {descriptions[i]}\n"

        markdown_1 = (
            "The goal of this section is to learn how to perform the following actions through FirecREST:\n"
            "1. Submit a job successfully\n"
            "2. Check the status of the job on the scheduler\n"
        )
        markdown_2 = (
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
        )
        markdown_3 = (
            "**Task 1**: `sbatch script.sh`\n"
            "\n"
            "**A. We make a request to FirecREST to submit the job.**\n"
        )
        if step > 2:
            markdown_3 += "\n" "This will create a FirecREST task.\n\n"
            markdown_3 += markdown_table_str

        if step > 3:
            markdown_3 += (
                "\n"
                "We will only get the task ID from the response.\n\n"
                "To find out if the job was actually submitted to Slurm we have to make another request.\n"
            )
        if step > 7:
            markdown_3 += (
                "\n"
                "**B. We check the status of the task and make sure we got status code 200.**\n"
            )

        markdown_4 = (
            "Task 1: `sbatch script.sh`\n" "\n" "**Task 2**: `squeue -j <job_id>`\n\n"
        )
        if step > 9:
            markdown_4 += "**A. We make a request to FirecREST to check the status that job.**\n\n"

        if step > 10:
            markdown_4 += "\n" "A new FirecREST task will be created.\n\n"
            markdown_4 += markdown_table_str

        # if step > 13:
        #     markdown_4 += "This task will keep a snapshot from the scheduler. It will not update the \n"

        if step > 14:
            markdown_4 += (
                "\n"
                "**B. We retrieve the scheduler's information.**\n"
                "The data of this task is just a snapshot of the scheduler, it will not be updated.\n"
            )

        if step in [0]:
            markdown_str = markdown_1
        elif step in [1]:
            markdown_str = markdown_2
        elif step in range(2, 10):
            markdown_str = markdown_3
        elif step in range(10, 17):
            markdown_str = markdown_4
        else:
            markdown_str = ""

        return display(Markdown(markdown_str))

    slider = wg.IntSlider(min=0, max=16, step=1, layout=wg.Layout(width="100%"))
    slideshow = wg.Box(
        [wg.interactive_output(show_figure, {"step": slider})],
        layout=wg.Layout(width="70%"),
    )
    description = wg.Box(
        [wg.interactive_output(markdown_explanation, {"step": slider})],
        layout=wg.Layout(width="30%", justify_content="center"),
    )
    ui = wg.Box([slideshow, description])

    display(slider, ui)


def show_external_upload():
    def show_figure(step):
        return display(
            Image(filename=f"images/external_upload/external_upload {step}.jpeg", width="100%")
        )

    def markdown_explanation(step):
        markdown_str = (
            "* For files >5MB we have to use the Storage Microservice.\n"
            "* We will upload the file through a staging area (more information [here](https://user.cscs.ch/storage/object_storage/)).\n"
            "* We keep track of the task through a FirecREST task and its status:\n\n"
        )

        markdown_str += "Status Code | Description\n" ":---: | :---\n"
        status = ["110", "111", "112", "113", "114", "115"]
        descriptions = [
            "Waiting for Form URL from Object Storage to be retrieved",
            "Form URL from Object Storage received",
            "Object Storage confirms that upload to Object Storage has finished",
            "Download from Object Storage to server has started",
            "Download from Object Storage to server has finished",
            "Download from Object Storage error",
        ]
        bold_status = [[4], [5, 6, 7, 8, 9], [10], [11], [12, 13], []]

        for i in range(len(status)):
            if step in bold_status[i]:
                markdown_str += f"**{status[i]}** | **{descriptions[i]}**\n"
            else:
                markdown_str += f"{status[i]} | {descriptions[i]}\n"

        return display(Markdown(markdown_str))

    slider = wg.IntSlider(min=1, max=15, step=1, layout=wg.Layout(width="100%"))
    slideshow = wg.Box(
        [wg.interactive_output(show_figure, {"step": slider})],
        layout=wg.Layout(width="70%"),
    )
    description = wg.Box(
        [wg.interactive_output(markdown_explanation, {"step": slider})],
        layout=wg.Layout(width="30%", justify_content="center"),
    )
    ui = wg.Box([slideshow, description])

    display(slider, ui)


def show_external_download():
    def show_figure(step):
        return display(
            Image(
                filename=f"images/external_download/tutorial_{step}.jpeg", width="100%"
            )
        )

    def markdown_explanation(step):
        markdown_str = (
            "* For files >5MB we have to use the Storage Microservice.\n"
            "* We will download the file through a staging area.\n"
            "* We keep track of the task through a FirecREST task and its status:\n\n"
        )

        markdown_str += "Status Code | Description\n" ":---: | :---\n"
        status = ["116", "117", "118"]
        descriptions = [
            "Started upload from filesystem to Object Storage",
            "Upload from filesystem to Object Storage has finished succesfully",
            "Upload from filesystem to Object Storage has finished with errors",
        ]
        bold_status = [[4], [5, 6, 7], []]

        for i in range(len(status)):
            if step in bold_status[i]:
                markdown_str += f"**{status[i]}** | **{descriptions[i]}**\n"
            else:
                markdown_str += f"{status[i]} | {descriptions[i]}\n"

        return display(Markdown(markdown_str))

    slider = wg.IntSlider(min=0, max=7, step=1, layout=wg.Layout(width="100%"))
    slideshow = wg.Box(
        [wg.interactive_output(show_figure, {"step": slider})],
        layout=wg.Layout(width="70%"),
    )
    description = wg.Box(
        [wg.interactive_output(markdown_explanation, {"step": slider})],
        layout=wg.Layout(width="30%", justify_content="center"),
    )
    ui = wg.Box([slideshow, description])

    display(slider, ui)
