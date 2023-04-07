import re
import datetime

from bs4 import BeautifulSoup
from httpx import AsyncClient
from auth.config import bucket
from lxml import etree
import httpx

import imgkit



def extract_object_name(url: str) -> str:
    pattern = r"https://storage.googleapis.com/[^/]+/(.+)"
    match = re.search(pattern, url)
    return match.group(1) if match else None


async def insert_qr_code_into_svg_template(svg_template_content, qr_code_url):
    # Download the QR code SVG content
    async with httpx.AsyncClient() as client:
        response = await client.get(qr_code_url)
        qr_code_svg_content = response.text

    # Parse the QR code SVG
    qr_code_svg_root = etree.fromstring(qr_code_svg_content.encode("utf-8"))

    # Parse the template SVG content
    parser = etree.XMLParser(recover=True, encoding='utf-8')
    svg_root = etree.fromstring(svg_template_content.encode("utf-8"), parser=parser)
    svg_root.set("width", "141px")
    svg_root.set("height", "226px")

    # Find the placeholder element
    qr_code_placeholder = svg_root.find('.//g', namespaces=svg_root.nsmap)

    if qr_code_placeholder is not None:
        # Insert the QR code SVG into the placeholder element
        for elem in qr_code_svg_root:
            elem.set("transform",
                     "translate(15, 50) scale(0.70, 0.70)")  # Add a 50-pixel vertical translation to the QR code
            qr_code_placeholder.append(elem)

    # Serialize the modified SVG content
    modified_svg_content = etree.tostring(svg_root, encoding="utf-8").decode("utf-8")

    return modified_svg_content


async def generate_svg(user_data_list, customer):
    customer = customer.replace(" ", "_")
    async with AsyncClient() as client:
        html_template = '''
            <html>
                <head>
                    <meta charset="utf-8">
                    <style>
                        body{{
                            width: 875.91px;
                            height: 1258.58px;
                            margin: 0;
                            position: relative;
                        }}
                        .qr-code {{
                            display: inline-block;
                            padding: 14px;
                        }}
                    </style>
                </head>
                <body>
                    {}
                </body>
            </html>
        '''

        svg_elements = []

        for user_data in user_data_list:
            object_name = extract_object_name(user_data["qr_code_file"])
            blob = bucket.blob(object_name)
            signed_url = blob.generate_signed_url(datetime.timedelta(minutes=10), method="GET")
            response = await client.get("https://storage.googleapis.com/daglarapp/montajs%C4%B1z.svg")
            svg_template_content = response.text
            modified_svg_content = await insert_qr_code_into_svg_template(svg_template_content, signed_url)
            svg_elements.append(f'<div class="qr-code">{modified_svg_content}</div>')

        combined_html = html_template.format("".join(svg_elements))


        soup = BeautifulSoup(combined_html, "html.parser")

        # Extract all the SVG elements
        svgs = soup.find_all("svg")

        combined_svg = BeautifulSoup(
            '<svg width="875.91px" height="1558.58px" xmlns="http://www.w3.org/2000/svg"></svg>',
            "html.parser"
        )

        # Insert all the extracted SVG elements into the combined SVG
        x_offset = 0
        y_offset = 0
        padding = 14
        items_per_line = 5
        max_rows = 6
        for i, svg in enumerate(svgs):
            # Create a group element and set its transform attribute using x and y offsets
            group = combined_svg.new_tag("g", transform=f"translate({x_offset}, {y_offset})")

            # Append the current SVG element to the group
            group.append(svg)

            # Append the group to the combined SVG
            combined_svg.svg.append(group)

            # Update the x and y offsets
            x_offset += int(svg['width'].rstrip("px")) + padding
            if (i + 1) % items_per_line == 0:
                x_offset = 0
                y_offset += int(svg['height'].rstrip("px")) + padding
                if (i + 1) % (items_per_line * max_rows) == 0:
                    y_offset = 0

        blob = bucket.blob(f"catalogs/{customer}_catalog.svg")
        blob.upload_from_string(str(combined_svg), content_type="image/svg+xml", predefined_acl="publicRead")
        svg_url = blob.public_url

        return svg_url
