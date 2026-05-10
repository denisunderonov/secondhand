# генератор PDF отчета о товарах (xhtml2pdf)

from io import BytesIO
from pathlib import Path

import xhtml2pdf.pisa as pisa
from django.http import HttpResponse
from django.template.loader import get_template

_FONTS_DIR = Path(__file__).resolve().parent / "fonts"
_DEJAVU = _FONTS_DIR / "DejaVuSans.ttf"
_ARIAL_MAC = Path("/System/Library/Fonts/Supplemental/Arial.ttf")


def _pdf_font_setup():
    """
    xhtml2pdf берёт родительский каталог base path как rootPath для url() в CSS.
    Поэтому path= должен указывать на файл внутри каталога со шрифтом, а не на сам каталог.
    """
    if _DEJAVU.is_file():
        return str(_DEJAVU.resolve()), "DejaVuSans.ttf"
    if _ARIAL_MAC.is_file():
        return str(_ARIAL_MAC.resolve()), "Arial.ttf"
    return str((_FONTS_DIR / "DejaVuSans.ttf").resolve()), "DejaVuSans.ttf"


def _link_callback(uri, basepath):
    """Если относительный путь к шрифту не находится — ищем в core/fonts/."""
    name = Path(str(uri)).name
    cand = _FONTS_DIR / name
    if cand.is_file():
        return str(cand.resolve())
    return uri


def pdf_response_from_template(template_src, context=None, filename="report.pdf"):
    context = dict(context or {})
    base_file, font_filename = _pdf_font_setup()
    context["pdf_body_font"] = "DocSans"
    context["pdf_font_file"] = font_filename

    template = get_template(template_src)
    html = template.render(context)
    buf = BytesIO(html.encode("utf-8"))
    result = BytesIO()
    pdf = pisa.CreatePDF(
        buf,
        result,
        encoding="utf-8",
        path=base_file,
        link_callback=_link_callback,
    )
    if getattr(pdf, "err", False):
        return HttpResponse(
            "Ошибка при создании PDF",
            status=500,
            content_type="text/plain; charset=utf-8",
        )
    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
