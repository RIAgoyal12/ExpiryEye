from PIL import Image, ImageEnhance, ImageFilter
from pytesseract import pytesseract
import enum
import re
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Define OS types
class OS(enum.Enum):
    Mac = 0
    Windows = 1
    Linux = 2

# Define languages for OCR
class Language(enum.Enum):
    Eng = 'eng'

# Class for reading and processing images
class ImageReader:
    def __init__(self, os: OS):
        if os == OS.Mac:
            print("Running on Mac")
        elif os == OS.Windows:
            windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            pytesseract.tesseract_cmd = windows_path
            print("Running on Windows:", windows_path)
        elif os == OS.Linux:
            linux_path = '/usr/bin/tesseract'
            pytesseract.tesseract_cmd = linux_path
            print("Running on Linux:", linux_path)

    # Preprocess image for better OCR accuracy
    def preprocess_image(self, image_path: str) -> Image:
        img = Image.open(image_path)
        img = img.convert('L')  # Convert to grayscale
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)  # Enhance contrast
        img = img.filter(ImageFilter.MedianFilter())  # Apply median filter
        return img

    # Extract text from the image
    def extract_text(self, image_path: str, lang: Language) -> str:
        img = self.preprocess_image(image_path)
        text = pytesseract.image_to_string(img, lang=lang.value)
        return text

    # Extract dates from the text
    def extract_dates(self, text: str):
        date_pattern = r'\b\d{2}/\d{2}/\d{4}\b'
        matches = re.finditer(date_pattern, text)

        manufacture_date = None
        expiry_date = None

        for match in matches:
            date_str = match.group()
            start, end = match.span()
            context = text[max(0, start - 15):end + 15].lower()  # Context around the date

            # Determine if it's an expiry or manufacture date
            if 'exp' in context or 'expiry' in context:
                try:
                    expiry_date = datetime.strptime(date_str, '%d/%m/%Y').strftime('%d/%m/%Y')
                except ValueError:
                    continue
            elif 'mfg' in context or 'manufacture' in context:
                try:
                    manufacture_date = datetime.strptime(date_str, '%d/%m/%Y').strftime('%d/%m/%Y')
                except ValueError:
                    continue

        return manufacture_date, expiry_date

    # Send notification email
    def send_notification(self, expiry_date: datetime, email: str):
        notification_days = 15
        current_date = datetime.now().date()

        if expiry_date.date() - timedelta(days=notification_days) <= current_date:
            msg = MIMEMultipart()
            msg['From'] = 'rgoyal_be22@thapar.edu'
            msg['To'] = email
            msg['Subject'] = 'Expiry Date Notification'
            body = f"Reminder: The item is set to expire on {expiry_date.strftime('%d/%m/%Y')}."
            msg.attach(MIMEText(body, 'plain'))

            try:
                # Establish SMTP connection
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(msg['From'], 'uccl elto pgeq inna')  # App password (Use environment variables for security)
                    server.sendmail(msg['From'], msg['To'], msg.as_string())
                    print("Notification sent successfully.")
            except Exception as e:
                print("Error sending email:", e)

# Main script execution
if __name__ == '__main__':
    ir = ImageReader(OS.Windows)  # Specify Linux OS
    text = ir.extract_text('expiry.jpg', lang=Language.Eng)
    print("Extracted Text:", text)

    manufacture_date_str, expiry_date_str = ir.extract_dates(text)

    # Check and display extracted manufacture date
    if manufacture_date_str:
        print("Manufacture Date:", manufacture_date_str)

    # Check and process extracted expiry date
    if expiry_date_str:
        print("Expiry Date:", expiry_date_str)
        try:
            expiry_date = datetime.strptime(expiry_date_str, '%d/%m/%Y')
            date_str = "2024-11-12"
            date1 = datetime.strptime(date_str, '%Y-%m-%d')
            receiver = 'riagoyal125@gmail.com'
            ir.send_notification(date1, receiver)
        except ValueError:
            print("Could not parse the expiry date format. Ensure the format is correct.")
    else:
        print("No expiry date found in the text.")
