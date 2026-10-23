"""Obtiene la muestra oficial para procesamiento local; no redistribuye la novela."""
from pathlib import Path
import argparse, re, urllib.request
from pypdf import PdfReader

URL='https://proassetspdlcom.cdnstatics2.com/usuaris/libros_contenido/arxius/53/52201_Neuromante.pdf'
ROOT=Path(__file__).resolve().parent

def extraer(pdf):
    reader=PdfReader(pdf)
    # La muestra tiene cubierta, portada y créditos en las tres primeras páginas.
    texts=[]
    for page in reader.pages[3:]:
        lines=(page.extract_text() or '').splitlines()
        lines=[line for line in lines if 'Neuromante.indd' not in line
               and not re.fullmatch(r'\s*\d+\s*',line)
               and not re.match(r'^\d{1,2}/\d{1,2}/\d{2}',line.strip())]
        block='\n'.join(lines)
        block=re.sub(r'(\w)\s*-\s*\n\s*(\w)',r'\1\2',block)
        texts.append(re.sub(r'\s+',' ',block).strip())
    return '\n\n'.join(texts)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--pdf',type=Path)
    args=parser.parse_args();data=ROOT/'data';data.mkdir(exist_ok=True)
    pdf=args.pdf or data/'muestra_editorial.pdf'
    if not pdf.exists():
        with urllib.request.urlopen(URL,timeout=45) as r:payload=r.read()
        if not payload.startswith(b'%PDF'):raise ValueError('La fuente no devolvió un PDF')
        pdf.write_bytes(payload)
    text=extraer(pdf)
    if len(text)<1000:raise ValueError('Extracción insuficiente; revisar el PDF')
    target=data/'neuromante_muestra.txt';target.write_text(text,encoding='utf-8')
    print(f'Texto local preparado: {len(text)} caracteres. Fuente: muestra editorial.')

if __name__=='__main__':main()
