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
    # Changed from home.html to index.html so it matches your file
    return render_template('index.html')

@app.route('/menu')
def menu():
    # If your menu is a separate file named menu.html, keep this. 
    # If your menu is inside index.html, you can delete this route.
    return render_template('menu.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('passcode') == "1234":
            session['admin_logged_in'] = True
            return render_template('admin.html', orders=orders)
    if session.get('admin_logged_in'):
        return render_template('admin.html', orders=orders)
    return redirect(url_for('home'))

@app.route('/order', methods=['POST'])
def place_order():
    name = request.form.get('customer_name')
    phone = request.form.get('phone')
    foods = request.form.getlist('food')
    delivery = request.form.get('delivery') 
    addr = request.form.get('address')
    instructions = request.form.get('instructions')

    if not foods:
        return "<h1>Error</h1><p>Select food!</p><a href='/'>Back</a>", 400

    subtotal = sum(MENU_PRICES.get(f, 0) for f in foods)
    current_delivery_cost = DELIVERY_FEE if delivery == 'on' else 0
    total = int(subtotal + current_delivery_cost)
    
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

@app.route('/complete-order/<int:order_id>')
def complete_order(order_id):
    if session.get('admin_logged_in'):
        for o in orders:
            if o['id'] == order_id:
                o['status'] = "Completed ✅"
                break
    return redirect(url_for('admin_login'))

@app.route('/admin-logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)