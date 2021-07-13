
# Some interesting functions for a plain pdf text

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from fuzzywuzzy import process,fuzz 
from datetime import datetime

def convert_pdf_to_string(file_path):

	output_string = StringIO()
	with open(file_path, 'rb') as in_file:
	    parser = PDFParser(in_file)
	    doc = PDFDocument(parser)
	    rsrcmgr = PDFResourceManager()
	    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
	    interpreter = PDFPageInterpreter(rsrcmgr, device)
	    for page in PDFPage.create_pages(doc):
	        interpreter.process_page(page)

	return(output_string.getvalue())

                
def convert_title_to_filename(title):
    filename = title.lower()
    filename = filename.replace(' ', '_')
    return filename


def split_to_title_and_pagenum(table_of_contents_entry):
    title_and_pagenum = table_of_contents_entry.strip()
    
    title = None
    pagenum = None
    
    if len(title_and_pagenum) > 0:
        if title_and_pagenum[-1].isdigit():
            i = -2
            while title_and_pagenum[i].isdigit():
                i -= 1

            title = title_and_pagenum[:i].strip()
            pagenum = int(title_and_pagenum[i:].strip())
        
    return title, pagenum
  
def split_consultas_date(texto):
	'''
	texto(str): string from the EHR to be splitted 
	'''
    consultas=texto.split(sep='Resumen de consulta')# depending of the EHR this may vary 
    return consultas

  
def fecha_nacimiento(texto):
    # initializing substrings that lay next to the interesting string
    sub1 = "nacimiento:"
    sub2 = "Celular"

    # getting index of substrings
    idx1 = texto.index(sub1)
    idx2 = texto.index(sub2)

    res = ''
    # getting elements in between
    for idx in range(idx1 + len(sub1) + 1, idx2):
        res = res + texto[idx]
    
    res=res.replace('\n','')
    fecha = datetime.strptime(res, '%d/%m/%Y').date()
    
    # printing result
    return fecha

 def nombre_paciente(texto): 
    # initializing substrings
    sub1 = "paciente:"
    sub2 = "Género"

    # getting index of substrings
    idx1 = texto.index(sub1)
    idx2 = texto.index(sub2)

    res = ''
    # getting elements in between
    for idx in range(idx1 + len(sub1) + 1, idx2):
        res = res + texto[idx]
    
    res=res.replace('\n','')
    
    
    # printing result
   
    return res

def fecha_consulta(texto):
    # initializing substrings
    sub1 = "consulta:"
    sub2 = "Nota"

    # getting index of substrings
    idx1 = texto.index(sub1)
    idx2 = texto.index(sub2)

    res = ''
    # getting elements in between
    for idx in range(idx1 + len(sub1) + 1, idx2):
        res = res + texto[idx]
    
    res=res.replace('\n','')
    fecha = datetime.strptime(res, '%d/%m/%Y').date()
    
    # printing result
    return fecha
def medicacion_consulta(texto):
    # initializing substrings
    try:
        sub1 = "Medicamentos"

        sub2 = 'Estudios Requeridos' if 'Estudios Requeridos' in texto else 'Plan o Notas'

        # getting index of substrings
        idx1 = texto.index(sub1)
        idx2 = texto.index(sub2)

        res = ''
        # getting elements in between
        for idx in range(idx1 + len(sub1) + 1, idx2):
            res = res + texto[idx]

        res=res.split('\n')
        while '' in res:
            res.remove('')

        n=len(res)
        for i in range(0,n):
            res[i]=str(res[i]).split()[0]
        return res
    except:#sometimes there is no more fields and directly appears the name of the medician. 
        
        sub2 = 'Ivan'

        # getting index of substrings
        idx1 = texto.index(sub1)
        idx2 = texto.index(sub2)

        res = ''
        # getting elements in between
        for idx in range(idx1 + len(sub1) + 1, idx2):
            res = res + texto[idx]

        res=res.split('\n')
        while '' in res:
            res.remove('')

        n=len(res)
        for i in range(0,n):
            res[i]=str(res[i]).split()[0]
        return res
      

def standardize_list(init_list,standard_list):
    no_includ=[]
    for i in range(len(init_list)):
        
        Variable = init_list[i] 
        Variable_final=process.extract(Variable,standard_list, scorer=fuzz.token_sort_ratio)[0]

        print('The closest variable is: '+ str(Variable_final[0])+'\n ¿Is it like '+Variable+'?')
        if Variable_final[1]>80:#If the similitudes are bigger than a 80% the variable is standardized according to the list provided
            init_list[i]=Variable_final[0]
            print('Ambas variables son equivalentes')
        else:
            no_includ.append(Variable)
        
            
    return init_list,no_includ
