import requests
import pdfkit
import os
from pypdf import PdfWriter
import time
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
# REMPLACEZ l'ID DANS l'URL ICI
BASE_URL = "https://storage.libmanuels.fr/Magnard/specimen/9782210120969/5/OEBPS/page{:03d}.xhtml"
BASE_HREF = "https://storage.libmanuels.fr/Magnard/specimen/9782210120969/5/OEBPS/"
START_PAGE = 2
END_PAGE = 164
OUTPUT_FOLDER = "pages_temp_clean"
FINAL_PDF_NAME = "Manuel_EMC_Complet_Clean.pdf"

# Configuration wkhtmltopdf (A adapter selon votre OS si besoin)
# PATH_WKHTMLTOPDF = None 
PATH_WKHTMLTOPDF = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe' 

if PATH_WKHTMLTOPDF:
    config = pdfkit.configuration(wkhtmltopdf=PATH_WKHTMLTOPDF)
else:
    config = None

options = {
    'page-size': 'A4',
    'margin-top': '0mm',
    'margin-right': '0mm',
    'margin-bottom': '0mm',
    'margin-left': '0mm',
    'encoding': "UTF-8",
    'enable-local-file-access': None,
    'viewport-size': '1377x784', 
    'load-error-handling': 'ignore' 
}

def download_and_convert():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    pdf_files = []

    print(f"Début du traitement de {START_PAGE} à {END_PAGE}...")

    for i in range(START_PAGE, END_PAGE + 1):
        url = BASE_URL.format(i)
        # On change l'extension en .html pour que le convertisseur soit plus tolérant
        html_filename = os.path.join(OUTPUT_FOLDER, f"page_{i:03d}.html")
        pdf_filename = os.path.join(OUTPUT_FOLDER, f"page_{i:03d}.pdf")

        try:
            print(f"Téléchargement : {url}")
            response = requests.get(url)
            
            if response.status_code == 200:
                # 1. Nettoyage avec BeautifulSoup
                # 'html.parser' va réparer les balises mal fermées
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 2. Injection propre de la balise <base> pour les images
                # On vérifie si <head> existe, sinon on le crée
                if not soup.head:
                    new_head = soup.new_tag("head")
                    soup.html.insert(0, new_head)
                
                base_tag = soup.new_tag("base", href=BASE_HREF)
                soup.head.insert(0, base_tag)

                # 3. Sauvegarde en HTML propre
                with open(html_filename, 'w', encoding='utf-8') as f:
                    f.write(str(soup))

                # 4. Conversion en PDF
                print(f"Conversion en PDF : page {i}")
                pdfkit.from_file(html_filename, pdf_filename, configuration=config, options=options)
                pdf_files.append(pdf_filename)
                
            else:
                print(f"Erreur {response.status_code} sur la page {i}")

        except Exception as e:
            print(f"Échec sur la page {i}: {e}")
        
        time.sleep(0.5)

    return pdf_files

def merge_pdfs(pdf_list, output_filename):
    if not pdf_list:
        print("Aucun PDF à fusionner.")
        return

    print("Fusion des fichiers PDF...")
    merger = PdfWriter()

    for pdf in pdf_list:
        try:
            merger.append(pdf)
        except Exception as e:
            print(f"Erreur lors de la fusion de {pdf}: {e}")

    with open(output_filename, "wb") as f_out:
        merger.write(f_out)
    
    print(f"Terminé ! Fichier créé : {output_filename}")

def cleanup(folder):
    print("Nettoyage des fichiers temporaires...")
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Erreur suppression {file_path}: {e}")
    os.rmdir(folder)

if __name__ == "__main__":
    generated_pdfs = download_and_convert()
    merge_pdfs(generated_pdfs, FINAL_PDF_NAME)
    # cleanup(OUTPUT_FOLDER) # Décommentez pour supprimer les fichiers temp
