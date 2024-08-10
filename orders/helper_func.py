import razorpay
from django.conf import settings
from playwright.sync_api import sync_playwright

def verify_signature(razorpay_order_id,razorpay_payment_id,razorpay_signature):
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )
    try:
        return client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
    except:
        return False

def html_to_pdf(html_content, output_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content)
        # await page.pdf(path=output_path)
        page.pdf(path=output_path,print_background=True)
        browser.close()