from flask import Flask, request, jsonify, render_template, redirect, url_for
from PIL import Image, ImageEnhance, ImageFilter
from pytesseract import pytesseract
import re
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import enum

# Enum for OS and Language
class OS(enum.Enum):
    Windows = 1

class Language(enum.Enum):
    Eng = 'eng'

class ImageReader:
    def __init__(self, os: OS):
        if os == OS.Windows:
            windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            pytesseract.tesseract_cmd = windows_path
            print("Running on Windows")
    
    def preprocess_image(self, image_path: str) -> Image:
        img = Image.open(image_path)
        img = img.convert('L')
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        img = img.filter(ImageFilter.MedianFilter())
        return img
    
    def extract_text(self, image_path: str, lang: Language) -> str:
        img = self.preprocess_image(image_path)
        text = pytesseract.image_to_string(img, lang=lang.value)
        return text

    def extract_dates(self, text: str):
        text = re.sub(r'\s*\.\s*', '.', text)  # Normalize spaces around dots
        text = re.sub(r'\s+', ' ', text)       # Normalize multiple spaces to single space
        text = text.replace('MFG', 'mfg').replace('EXP', 'exp')  # Standardize the keywords

        date_patterns = [
            r'\b\d{2}/\d{2}/\d{4}\b',  # dd/mm/yyyy
            r'\b\d{4}-\d{2}-\d{2}\b',  # yyyy-mm-dd
            r'\b\d{2}-\d{2}-\d{4}\b',  # dd-mm-yyyy
        ]

        date_formats = [
            '%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y'
        ]

        manufacture_date = None
        expiry_date = None

        for pattern in date_patterns:
            matches = list(re.finditer(pattern, text))
            for match in matches:
                date_str = match.group().strip()
                start, end = match.span()
                context = text[max(0, start - 15):end + 15].lower()

                if 'exp' in context or 'expiry' in context:
                    expiry_date = self.parse_date(date_str, date_formats)
                elif 'mfg' in context or 'manufacture' in context:
                    manufacture_date = self.parse_date(date_str, date_formats)

                if manufacture_date and expiry_date:
                    return manufacture_date, expiry_date

        return manufacture_date, expiry_date

    def parse_date(self, date_str, date_formats):
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, date_format)
                return parsed_date.strftime('%d/%m/%Y')
            except ValueError:
                continue
        return None

    def send_notification(self, expiry_date: datetime, email: str):
        notification_days = 15
        current_date = datetime.now().date()

        if expiry_date.date() - timedelta(days=notification_days) <= current_date:
            msg = MIMEMultipart()
            msg['From'] = 'rgoyal_be22@thapar.edu'  # Replace with your email
            msg['To'] = email
            msg['Subject'] = 'Expiry Date Notification'
            body = f"Reminder: The item you scanned is set to expire on {expiry_date.strftime('%d-%m-%Y')}. Please use it before the expiration date to avoid waste."
            msg.attach(MIMEText(body, 'plain'))
            
            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(msg['From'],  'uccl elto pgeq inna')  # Use app-specific password
                    server.sendmail(msg['From'], msg['To'], msg.as_string())
                    print("Notification sent successfully.")
            except Exception as e:
                print("Error sending email:", e)

# Flask Web Application
app = Flask(__name__,template_folder='.')

@app.route('/contactus', methods=['GET', 'POST'])


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        expiry_date_str = request.form.get('expiry_date')
        image = request.files.get('image')

        if expiry_date_str:
            try:
                expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
                print(f"Manually entered expiry date: {expiry_date.strftime('%d-%m-%Y')}")
                ImageReader(OS.Windows).send_notification(expiry_date, email)
            except ValueError:
                print("Invalid expiry date format. Please use yyyy-mm-dd.")
        elif image:
            image_path = "uploaded_image.jpg"
            image.save(image_path)
            ir = ImageReader(OS.Windows)
            text = ir.extract_text(image_path, Language.Eng)
            print("Extracted Text:", text)
            _, expiry_date_str_from_image = ir.extract_dates(text)
            if expiry_date_str_from_image:
                try:
                    expiry_date = datetime.strptime(expiry_date_str_from_image, '%d/%m/%Y')
                    print(f"Extracted expiry date: {expiry_date}")
                    ir.send_notification(expiry_date, email)
                except ValueError:
                    print("Failed to parse expiry date.")
            else:
                print("No expiry date found in the image.")
        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)