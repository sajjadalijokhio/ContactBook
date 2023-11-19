from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key

contacts = [
    {'id': 1, 'name': 'Ali', 'phone': '0345-1234567', 'email': 'ali.khan@example.com', 'address': '123 Gulshan-e-Iqbal, Karachi'},
    {'id': 2, 'name': 'Ahmed', 'phone': '0312-9876543', 'email': 'ahmed@example.com', 'address': '456 Defence, Lahore'}
]

def capitalize_contact_names(contacts_list):
    for contact in contacts_list:
        contact['name'] = contact['name'].title()

capitalize_contact_names(contacts)

def get_contact(contact_id):
    return next((c for c in contacts if c['id'] == contact_id), None)

@app.route('/')
def index():
    return render_template('index.html', contacts=contacts)

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        new_contact = {
            'id': len(contacts) + 1,
            'name': request.form['name'].title(),
            'phone': request.form['phone'],
            'email': request.form['email'],
            'address': request.form['address']
        }
        contacts.append(new_contact)
        flash('Contact added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_contact.html')

@app.route('/edit_contact/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    contact = get_contact(id)
    if contact:
        if request.method == 'POST':
            contact['name'] = request.form['name'].title()
            contact['phone'] = request.form['phone']
            contact['email'] = request.form['email']
            contact['address'] = request.form['address']
            flash('Contact updated successfully!', 'success')
            return redirect(url_for('index'))
        return render_template('edit_contact.html', contact=contact)
    return redirect(url_for('index'))

@app.route('/delete_contact/<int:id>')
def delete_contact(id):
    global contacts
    contacts = [c for c in contacts if c['id'] != id]
    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
