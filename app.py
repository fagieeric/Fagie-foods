from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "fagie_foods_secret_2026"

# Database & Prices (UGX)
orders = []
MENU_PRICES = {
    "Burger": 15000, "Pizza": 35000, "Chicken (2pc)": 12000,
    "Rolex (Special)": 6000, "Fries": 5000, "Fresh Juice": 4000, "Soda": 2500
}
DELIVERY_FEE = 2000 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/admin-login', methods=['POST'])
def admin_login():
    passcode = request.form.get('passcode')
    if passcode == "1234":
        session['admin_logged_in'] = True
        return render_template('admin.html', orders=orders)
    return "<h1>Access Denied</h1><p>Incorrect Passcode.</p><a href='/'>Back Home</a>", 401

@app.route('/order', methods=['POST'])
def place_order():
    name = request.form.get('customer_name')
    phone = request.form.get('phone')
    foods = request.form.getlist('food')
    delivery = request.form.get('delivery') 
    addr = request.form.get('address')
    instructions = request.form.get('instructions')

    if not foods:
        return "<h1>Error</h1><p>Select food!</p><a href='/menu'>Back</a>", 400

    subtotal = sum(MENU_PRICES.get(f, 0) for f in foods)
    total = int(subtotal + (DELIVERY_FEE if delivery == 'on' else 0))
    otype = f"🚚 Deliver to: {addr}" if delivery == 'on' else "🛍️ Pickup (Mukono Town)"

    new_order = {
        "id": len(orders) + 1,
        "name": name,
        "phone": phone,
        "food_items": foods,
        "instructions": instructions,
        "total": total,
        "type": otype,
        "status": "Pending"
    }
    orders.append(new_order)
    return render_template('success.html', name=name, phone=phone, food_list=foods, 
                           total=total, type=otype, instructions=instructions)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)