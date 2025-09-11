from pathlib import Path

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TesseractCliOcrOptions

def pdf_to_html(src_pdf: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_html = out_dir / f"{src_pdf.stem}.html"

    pipeline_options = PdfPipelineOptions(
        # OCR 관련 설정
        do_ocr=True,
        force_full_page_ocr=True,
        ocr_image_dpi=300,  # <<<--- 1. OCR을 위한 이미지 해상도를 300 DPI로 설정

        ocr_options=TesseractCliOcrOptions(
            lang=["auto"],
            # <<<--- 2. Tesseract에 직접 옵션 전달 (페이지 분석 모드 최적화)
            user_defined_options=["--psm 1"] 
        ),
        
        # 테이블 구조 추출
        do_table_structure=True
    )

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    result = converter.convert(src_pdf)
    doc = result.document
    doc.save_as_html(out_html)
    return out_html

if __name__ == "__main__":
    src = Path("asset") / "science.pdf"
    dst = Path("asset") / "html"
    out_path = pdf_to_html(src, dst)
    print(f"HTML 저장 완료: {out_path.resolve()}")