import qrcode
from reportlab.pdfgen import canvas

from pypdf import PdfReader, PdfWriter

data = "http://192.168.188.26:8888/reports/rwservlet/getjobid1218?server=repserver1& REPORT NAME = inv_pos"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

img.save("qr001.png")

# Create a PDF document
c = canvas.Canvas("qr0001.pdf")


# Draw the QR code on the PDF
c.drawInlineImage("qr001.png", 200, 700, width=100, height=100)

# Save the PDF
c.save()

reader = PdfReader("qr0001.pdf")

writer = PdfWriter()
writer.append_pages_from_reader(reader)
writer.encrypt("1234")

with open("qr0001.pdf", "wb") as out_file:
    writer.write(out_file)

