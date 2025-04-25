import requests
from bs4 import BeautifulSoup
import time
from plyer import notification

# Best Buy 5080 URL
URL = "https://www.bestbuy.com/site/searchpage.jsp?id=pcat17071&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%205080&st=5080"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def check_stock():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch page, status code: {response.status_code}")
        return False

    soup = BeautifulSoup(response.text, 'html.parser')

    # Check if "Add to Cart" buttons or "Sold Out" appear on listings
    items = soup.find_all('li', {'class': 'sku-item'})
    for item in items:
        title = item.find('h4', {'class': 'sku-header'})
        if title and '5080' in title.text:
            stock_status = item.get_text().lower()
            if 'add to cart' in stock_status:
                print(f"✅ IN STOCK: {title.text.strip()}")
                send_notification(title.text.strip())
                return True
            else:
                print(f"❌ OUT OF STOCK: {title.text.strip()}")
    return False

def send_notification(product_name):
    notification.notify(
        title='GPU IN STOCK!',
        message=f'{product_name} is available at Best Buy!',
        timeout=10
    )

# Check every 5 minutes (300 seconds)
if __name__ == '__main__':
    while True:
        print("Checking stock...")
        check_stock()
        time.sleep(300)