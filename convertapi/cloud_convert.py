import httpx

# Your CloudConvert API key
api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiYjMxNTlmMzg1ZTUzOWQ0NzUyMjhkNTc2ODM0MDE1MmQxOGM1NjkxMWY4YzlhYjQxODJiZGVmNmFmOWFlZjAwMjA5OGFlZTI5ZWNmNzk0ZjQiLCJpYXQiOjE2ODA2MzM3OTcuNzg3OTQ3LCJuYmYiOjE2ODA2MzM3OTcuNzg3OTQ4LCJleHAiOjQ4MzYzMDczOTcuNzc5OTQ0LCJzdWIiOiI2MjkxNjYyMSIsInNjb3BlcyI6WyJ1c2VyLnJlYWQiLCJ1c2VyLndyaXRlIiwidGFzay5yZWFkIiwidGFzay53cml0ZSIsIndlYmhvb2sucmVhZCIsIndlYmhvb2sud3JpdGUiLCJwcmVzZXQucmVhZCIsInByZXNldC53cml0ZSJdfQ.Y5XFX68IS4cBU9e0JB-T7KtwmiHwLSN6JGWWZx6FFCc4TqjSSK_NZliZhA-_zXIP6V0KOPmq08DRAb3J8XYnCGt6WnXk4arHhk9vEmB9ojH-_LA3asIrq0eyZYttYvdEnCUIqETVQqNB_gZDgnq5uo3SkxCVwSuDMEV3aaEGhNpA1A6I9QMP1bo9wLQ9aWIaOXrnAMV52B5MlJfT6NWw8sEZb1umc5Jbeyecu_YfPuAojbwpd4FkilsN2VPAPCUkIaTJKKJoqPhD-aj0XT7NoTvEoP4Z4U4B0rNRQQ3CyoBK61ns5Kk2Fnovo7SDmXeSdBSAivBrhE6BnRjUb7tphlU98V5HFdOieBvM2mAVNWuBfops0q-_QyKr449dYby5K9BglnKy8xoNU2a1-co-B93Aciiv-0pEZfMmC58lVLLoMpQ2SU9O2wLH-zvCOxDbIGMXKCnTY7yTzg3FS0DP2ARlY77iybTzjY7IeGxDK2CeoyzozR80y1PbPGjv4hYnokKwl3PaeDop-d9510Yo9w0a9RmA0Q3EhtRhyCa0QtZ30KWW9lqlmAcnNAfkflyA-NUYYn2CohFtQ2Stsoxxvp1z-PDggtk5RUMGe5L-y61uUONmlo4lX9dSK3dLKW26tt5mcfyjpJs3tR6nHtS-7b_agTQ1xQLbNNN-8vsOKKE"

# Convert HTML to PNG using CloudConvert API
async def convert_html_to_png(html_content):
    async with httpx.AsyncClient() as client:
        # Create a new CloudConvert task for HTML to PNG conversion
        response = await client.post(
            "https://api.cloudconvert.com/v2/tasks",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"operation": "convert", "input_format": "html", "output_format": "png"},
        )
        task_id = response.json()["id"]

        # Upload the HTML content
        response = await client.post(
            "https://api.cloudconvert.com/v2/import/string",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"task": task_id, "file": html_content, "filename": "input.html"},
        )
        import_task_id = response.json()["id"]

        # Execute the conversion task
        response = await client.post(
            "https://api.cloudconvert.com/v2/tasks/wait",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"tasks": [task_id, import_task_id]},
        )

        # Export the PNG file
        response = await client.post(
            "https://api.cloudconvert.com/v2/export/url",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"input": task_id},
        )
        export_task_id = response.json()["id"]

        # Wait for the export task to complete
        response = await client.post(
            "https://api.cloudconvert.com/v2/tasks/wait",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"tasks": [export_task_id]},
        )

        # Get the PNG file URL
        response = await client.get(
            f"https://api.cloudconvert.com/v2/tasks/{export_task_id}/result",
            headers={"Authorization": f"Bearer {api_key}"},
        )
        png_file_url = response.json()["files"][0]["url"]

        # Download the PNG file
        response = await client.get(png_file_url)
        with open("output.png", "wb") as png_file:
            png_file.write(response.content)




