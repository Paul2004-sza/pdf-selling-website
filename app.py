import os
import stripe
from flask import Flask, render_template, request, redirect, url_for
from flask import send_file

# Initialize the Flask app and Stripe API
app = Flask(__name__)
stripe.api_key = "sk_test_51Q4MrsGO7zMrqrolrf4oCilbyrZQyJBxCOkgtlej42zuOy6p4H4aAiVJGsEshQJRK2Aa4vJxAb06xqS4bAQohJfp00PPvZbqne"  # Replace with your Stripe secret key

# List of available PDFs with prices (you can customize this)
pdf_files = [
    {"name": "Sample PDF 2", "price": 14.99, "filename": "new_pdf_for_sale.pdf"},
{"name": "Another PDF", "price": 9.99, "filename": "another_pdf_for_sale.pdf"},
]


@app.route('/')
def index():
    return render_template('index.html', pdf_files=pdf_files)


@app.route('/buy/<filename>')
def buy_pdf(filename):
    # Get the selected PDF's information
    selected_pdf = next((pdf for pdf in pdf_files if pdf["filename"] == filename), None)
    if not selected_pdf:
        return "PDF not found", 404

    # Create a Stripe checkout session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': selected_pdf["name"],
                },
                'unit_amount': int(selected_pdf["price"] * 100),  # price in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('success', filename=filename, _external=True),
        cancel_url=url_for('index', _external=True),
    )

    return redirect(checkout_session.url, code=303)


@app.route('/success/<filename>')
def success(filename):
    return render_template('success.html', filename=filename)


@app.route('/download/<filename>')
def download_pdf(filename):
    selected_pdf = next((pdf for pdf in pdf_files if pdf["filename"] == filename), None)
    if not selected_pdf:
        return "PDF not found", 404

    pdf_path = os.path.join('pdfs', filename)  # Adjust if your PDFs are stored elsewhere
    return send_file(pdf_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
