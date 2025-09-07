# pip install -U docling docling-ibm-models
# (스캔 PDF인 경우) 시스템에 tesseract가 설치되어 있어야 합니다.
#   mac: brew install tesseract
#   ubuntu/debian: sudo apt-get install tesseract-ocr tesseract-ocr-kor

from pathlib import Path

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TesseractCliOcrOptions

def pdf_to_html(src_pdf: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_html = out_dir / f"{src_pdf.stem}.html"

    # 스캔 여부에 따라 OCR 사용 결정
    # - 디지털(텍스트 내장) PDF면 do_ocr=False 권장
    # - 스캔/이미지 기반 PDF면 do_ocr=True, 언어를 자동/한국어로 설정
    pipeline_options = PdfPipelineOptions(
        do_ocr=False,                      # 스캔 문서라면 True
        force_full_page_ocr=False,        # 전면 OCR이 필요하면 True
        ocr_options=TesseractCliOcrOptions(
            # 한국어 전용: ["kor"], 자동 감지: ["auto"]
            lang=["kor"]
        ),
        do_table_structure=True           # 표 구조 추출
    )

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    result = converter.convert(src_pdf)
    doc = result.document

    # 파일로 저장 (문자열이 필요하면 doc.export_to_html())
    doc.save_as_html(out_html)

    return out_html

if __name__ == "__main__":
    src = Path("asset") / "국어.pdf"
    dst = Path("asset") / "html"
    out_path = pdf_to_html(src, dst)
    print(f"HTML 저장 완료: {out_path.resolve()}")
