import qrcode

def generate_password_protected_qrcode(data, password, output_file):
    # Concatenate the data and password in the URL format
    url = f"{data}?password={password}"

    # Generate the QR code for the combined data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create the QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)

if __name__ == "__main__":
    # Example: Generate a QR code with a password parameter for "https://example.com"
    data_to_encode = "https://example.com"
    password_for_qr = "1234"
    output_filename = "password_protected_qrcode1.png"

    generate_password_protected_qrcode(data_to_encode, password_for_qr, output_filename)
    print(f"Password-protected QR code saved to {output_filename}")
