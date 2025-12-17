import pymupdf4llm
import pathlib

md_text = pymupdf4llm.to_markdown("안양대_pdf/안양대_2021.pdf")

pathlib.Path("안양대_2021.md").write_bytes(md_text.encode())