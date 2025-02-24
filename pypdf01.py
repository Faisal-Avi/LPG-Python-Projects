from pypdf import PdfReader, PdfWriter

reader = PdfReader("OUp5hm0S.pdf")

writer = PdfWriter()
writer.append_pages_from_reader(reader)
writer.encrypt("1234")

with open("OUp5hm0S.pdf", "wb") as out_file:
    writer.write(out_file)