import argparse
import asyncio
import logging
import os
from pathlib import Path

from open_itinerary.adapters import Adapter, InputContent
from open_itinerary.adapters.email_adapter import EmailAdapter
from open_itinerary.adapters.html_adapter import HtmlAdapter
from open_itinerary.adapters.pdf import PdfAdapter

logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default="./data/example_documents/HNL_MNL.pdf")
    parser.add_argument("-o", "--output-folder", dest="output_folder", default="./data/example_documents/converted/")

    args = parser.parse_args()

    file_type = Path(args.input).suffix

    content_type: str = None
    adapter: Adapter = None

    match file_type:
        case ".pdf":
            content_type = "application/pdf"
            adapter = PdfAdapter()
        case ".html":
            content_type = "text/html"
            adapter = HtmlAdapter()
        case ".eml":
            content_type = "message/rfc822"
            adapter = EmailAdapter()
        case _:
            raise NotImplementedError(f"{file_type} is not supported")

    logger.info("reading %s", args.input)
    data = await asyncio.to_thread(Path(args.input).read_bytes)

    logger.info("adapting content")
    content = InputContent(data, content_type)
    result = await adapter.load(content)

    os.makedirs(args.output_folder, exist_ok=True)

    for index, current_result in enumerate(result):
        obj = current_result.model_dump_json(indent=4)

        file_name = Path(args.input).name + f"_{index}.json"
        file_name = os.path.join(args.output_folder, file_name)

        logger.info("dumping result %s to %s", index, file_name)
        await asyncio.to_thread(Path(file_name).write_text, obj)


if __name__ == "__main__":
    asyncio.run(main())
