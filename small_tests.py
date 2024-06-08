import PyPDF2

# Open the two PDF files you want to merge
pdf1 = open(r"C:\Users\itama\Downloads\תיק פרוייקט.pdf", 'rb')
pdf2 = open(r"C:\Users\itama\Downloads\code_in_pdf_4.pdf", 'rb')

# Create a PDF reader object for each file
reader1 = PyPDF2.PdfReader(pdf1)
reader2 = PyPDF2.PdfReader(pdf2)

# Create a PDF writer object
writer = PyPDF2.PdfWriter()

# Add the pages from the first PDF file to the writer object
for i in range(len(reader1.pages)):
    writer.add_page(reader1.pages[i])

# Add the pages from the second PDF file to the writer object
for i in range(len(reader2.pages)):
    writer.add_page(reader2.pages[i])

# Create a new PDF file and write the merged content to it
with open('merged_file.pdf', 'wb') as output:
    writer.write(output)

# Close the input files
pdf1.close()
pdf2.close()