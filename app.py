from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from dotenv import load_dotenv
import random
import string
import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('MY_SECRET', 'fallback-secret')

# --- In-memory CRM Data ---
crm_contacts = []
crm_deals = []
crm_notes = []

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_contact_by_id(cid):
    for c in crm_contacts:
        if c['id'] == cid:
            return c
    return None

def get_deal_by_id(did):
    for d in crm_deals:
        if d['id'] == did:
            return d
    return None

@app.route('/')
def home():
    return redirect(url_for('crm_dashboard'))

@app.route('/crm')
def crm_dashboard():
    return render_template('crm_dashboard.html', contacts=crm_contacts, deals=crm_deals)

@app.route('/crm/contact/new', methods=['GET', 'POST'])
def crm_new_contact():
    if request.method == 'POST':
        cid = random_string(8)
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        crm_contacts.append({'id': cid, 'name': name, 'email': email, 'phone': phone, 'created': get_time()})
        flash('Contact added!', 'success')
        return redirect(url_for('crm_dashboard'))
    return render_template('crm_contact_form.html', contact=None)

@app.route('/crm/contact/<cid>', methods=['GET', 'POST'])
def crm_edit_contact(cid):
    contact = get_contact_by_id(cid)
    if not contact:
        flash('Contact not found.', 'danger')
        return redirect(url_for('crm_dashboard'))
    if request.method == 'POST':
        contact['name'] = request.form.get('name')
        contact['email'] = request.form.get('email')
        contact['phone'] = request.form.get('phone')
        flash('Contact updated!', 'success')
        return redirect(url_for('crm_dashboard'))
    return render_template('crm_contact_form.html', contact=contact)

@app.route('/crm/contact/delete/<cid>')
def crm_delete_contact(cid):
    global crm_contacts
    crm_contacts = [c for c in crm_contacts if c['id'] != cid]
    flash('Contact deleted.', 'info')
    return redirect(url_for('crm_dashboard'))

@app.route('/crm/deal/new', methods=['GET', 'POST'])
def crm_new_deal():
    if request.method == 'POST':
        did = random_string(8)
        title = request.form.get('title')
        value = request.form.get('value')
        contact_id = request.form.get('contact_id')
        crm_deals.append({'id': did, 'title': title, 'value': value, 'contact_id': contact_id, 'created': get_time()})
        flash('Deal added!', 'success')
        return redirect(url_for('crm_dashboard'))
    return render_template('crm_deal_form.html', deal=None, contacts=crm_contacts)

@app.route('/crm/deal/<did>', methods=['GET', 'POST'])
def crm_edit_deal(did):
    deal = get_deal_by_id(did)
    if not deal:
        flash('Deal not found.', 'danger')
        return redirect(url_for('crm_dashboard'))
    if request.method == 'POST':
        deal['title'] = request.form.get('title')
        deal['value'] = request.form.get('value')
        deal['contact_id'] = request.form.get('contact_id')
        flash('Deal updated!', 'success')
        return redirect(url_for('crm_dashboard'))
    return render_template('crm_deal_form.html', deal=deal, contacts=crm_contacts)

@app.route('/crm/deal/delete/<did>')
def crm_delete_deal(did):
    global crm_deals
    crm_deals = [d for d in crm_deals if d['id'] != did]
    flash('Deal deleted.', 'info')
    return redirect(url_for('crm_dashboard'))

@app.route('/crm/note/new/<cid>', methods=['GET', 'POST'])
def crm_new_note(cid):
    contact = get_contact_by_id(cid)
    if not contact:
        flash('Contact not found.', 'danger')
        return redirect(url_for('crm_dashboard'))
    if request.method == 'POST':
        note = request.form.get('note')
        crm_notes.append({'contact_id': cid, 'note': note, 'created': get_time()})
        flash('Note added!', 'success')
        return redirect(url_for('crm_dashboard'))
    return render_template('crm_note_form.html', contact=contact)

@app.route('/crm/notes/<cid>')
def crm_view_notes(cid):
    contact = get_contact_by_id(cid)
    if not contact:
        flash('Contact not found.', 'danger')
        return redirect(url_for('crm_dashboard'))
    notes = [n for n in crm_notes if n['contact_id'] == cid]
    return render_template('crm_notes.html', contact=contact, notes=notes)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message='Page not found!'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', error_message='Internal server error!'), 500

if __name__ == '__main__':
    app.run(debug=True)
