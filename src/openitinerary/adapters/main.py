import argparse
import asyncio
import logging
from collections.abc import Sequence
from pathlib import Path

from openitinerary.adapters import Adapter, InputContent
from openitinerary.adapters.email_adapter import EmailAdapter
from openitinerary.adapters.html_adapter import HtmlAdapter
from openitinerary.adapters.pdf import PdfAdapter

logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


def _parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="PDF, HTML, or EML travel document to convert")
    parser.add_argument(
        "-o",
        "--output-folder",
        type=Path,
        default=Path("converted"),
        help="Directory for converted segment JSON files (default: ./converted)",
    )

    return parser.parse_args(args)


async def _adapt(input_path: Path, output_folder: Path) -> None:
    file_type = input_path.suffix.lower()

    content_type: str
    adapter: Adapter

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

    logger.info("reading %s", input_path)
    data = await asyncio.to_thread(input_path.read_bytes)

    logger.info("adapting content")
    content = InputContent(data, content_type)
    result = await adapter.load(content)

    output_folder.mkdir(parents=True, exist_ok=True)

    for index, current_result in enumerate(result):
        obj = current_result.model_dump_json(indent=4)

        output_file = output_folder / f"{input_path.name}_{index}.json"

        logger.info("dumping result %s to %s", index, output_file)
        await asyncio.to_thread(output_file.write_text, obj, encoding="utf-8")


def main() -> None:
    args = _parse_args()
    asyncio.run(_adapt(args.input, args.output_folder))


if __name__ == "__main__":
    main()
