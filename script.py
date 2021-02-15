import csv
import time
from tqdm import tqdm
from datetime import *
from bs4 import BeautifulSoup
from num2words import num2words
import pdfkit


#extract text fom html file
html="cerfa_template.html"
soup = BeautifulSoup(open(html), "html.parser")
text = soup.get_text()
#print(type(str(soup)))

#static info
today = datetime.now().date().strftime('%d/%m/%Y')

#contact file name without extension
contacts = "contact"

#count the number of rows in file
with open(f"{contacts}.csv", encoding='utf-8') as file:
	reader = csv.reader(file)
	next(reader)  # Skip header row
	rows = sum(1 for row in reader)
	print(f"Total contacts: {rows}")

#variable to be used in loop to increment the number of contacts
x = 0

#function to check the right boxes in the form
def checkbox(form_input, html, html_str):
	to_replace = str(html.find(text=form_input).parent)
	by_replace = to_replace[:37]+' checked'+to_replace[37:]
	return html_str.replace(to_replace,by_replace)



#open contact file that will be used to send emails
with open(f"{contacts}.csv", encoding='utf-8') as file:
	reader = csv.reader(file)
	next(reader)  # Skip header row
	#loop through contacts to prepare email and send individually
	for firstname,lastname,address,postal_code,commune,amount_numbers,date,droit,forme,nature,mode,code_cerfa in tqdm(reader, total=rows):
		html_str = str(soup).format(firstname=firstname, lastname=lastname, code_cerfa=code_cerfa, address=address, postal_code=postal_code, commune=commune, amount_numbers=amount_numbers, amount_letters= num2words(amount_numbers, lang="fr"), date=date, today=today)
		html_str = checkbox(str(droit),soup,html_str)
		html_str = checkbox(str(forme),soup,html_str)
		html_str = checkbox(str(nature),soup,html_str)
		html_str = checkbox(str(mode),soup,html_str)
		Html_file = open(f"cerfa_html/{code_cerfa}.html","w")
		Html_file.write(html_str)
		Html_file.close()

#convert html files to pdfs

#css = ['css/style.css', 'css/bootstrap-grid.css', 'css/bootstrap.css']

options = {'encoding':"UTF-8"}

pdfkit.from_file('cerfa_html/2019-2396.html','out.pdf' , options=options)
