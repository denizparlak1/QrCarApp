import asyncio
import os

import httpx


async def convert_html_to_png_example(html_content):

    api_key = os.environ['CONVERT_API']

    # Convert HTML to PNG using CloudConvert API
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.cloudconvert.com/v2/jobs",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "tasks": {
                    "html_input": {
                        "operation": "import/raw",
                        "file": html_content,
                        "filename": "input.html",
                    },
                    "convert": {
                        "operation": "convert",
                        "input": "html_input",
                        "output_format": "png",
                        "width": 3639,
                        "height": 5217
                    },
                    "export_task": {
                        "operation": "export/url",
                        "input": "convert",
                        "inline": True,
                        "archive_multiple_files": False,
                    }
                },
            },
        )

    # Check for errors
    if response.status_code != 201:
        print(f"Error: {response.status_code}")
        print(f"Response content: {response.content}")
        return None

    # Get task ID
    task_id = response.json()["data"]["id"]

    # Wait for the conversion to finish
    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get(
                f"https://api.cloudconvert.com/v2/jobs/{task_id}",
                headers={"Authorization": f"Bearer {api_key}"},
            )
            status = response.json()["data"]["status"]

            if status == "finished":
                break
            elif status == "error":
                print("Error during conversion")
                return None
            else:
                await asyncio.sleep(5)

    # Get the download URL
    export_task_name = "export_task"

    download_url = response.json()["data"]["tasks"][0]["result"]["files"][0]["url"]

    # Download the PNG
    async with httpx.AsyncClient() as client:
        response = await client.get(download_url)

    # Save the PNG to a local file
    with open("output.png", "wb") as output_file:
        output_file.write(response.content)

    print("Conversion successful. Saved as output.png")
