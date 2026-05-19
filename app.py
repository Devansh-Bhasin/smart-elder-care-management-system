from flask import Flask, render_template, request, redirect, url_for, session, abort

app = Flask(__name__)
app.secret_key = 'prototype_secret_key'  # Required for session

# Hardcoded Users
USERS = {
    'admin': {'password': 'admin123', 'role': 'Admin'},
    'nurse': {'password': 'nurse123', 'role': 'Nurse'},
    'caregiver': {'password': 'care123', 'role': 'Caregiver'},
    'doctor': {'password': 'doc123', 'role': 'Doctor'},
    'resident1': {'password': 'res123', 'role': 'Resident'},
    'family1': {'password': 'fam123', 'role': 'Family'}
}

# --- Mock Associations ---
# Link Resident/Family accounts to specific residents in the data
ASSOCIATED_RESIDENTS = {
    'resident1': 'Alice Smith',
    'family1': 'Alice Smith'
}

# --- Mock Data for Prototype ---

MOCK_HEALTH = [
    {'resident': 'Alice Smith', 'heart_rate': '72', 'temp': '36.8', 'bp': '120/80', 'time': '10:30 AM'},
    {'resident': 'Alice Smith', 'heart_rate': '75', 'temp': '36.9', 'bp': '118/78', 'time': '02:45 PM'},
    {'resident': 'Alice Smith', 'heart_rate': '70', 'temp': '36.7', 'bp': '122/82', 'time': 'Yesterday'},
    {'resident': 'Alice Smith', 'heart_rate': '74', 'temp': '36.8', 'bp': '120/80', 'time': '2 days ago'},
    {'resident': 'Bob Jones', 'heart_rate': '85', 'temp': '37.2', 'bp': '140/90', 'time': '09:15 AM'},
    {'resident': 'Charlie Brown', 'heart_rate': '68', 'temp': '36.5', 'bp': '115/75', 'time': 'Yesterday'}
]

MOCK_ACTIVITIES = [
    {'resident': 'Alice Smith', 'activity': 'Morning Walk', 'date': '2026-03-24', 'start_time': '08:00 AM', 'end_time': '08:30 AM', 'status': 'Completed'},
    {'resident': 'Alice Smith', 'activity': 'Socializing in Garden', 'date': '2026-03-24', 'start_time': '11:30 AM', 'end_time': '12:30 PM', 'status': 'Completed'},
    {'resident': 'Alice Smith', 'activity': 'Afternoon Nap', 'date': '2026-03-24', 'start_time': '01:30 PM', 'end_time': '02:30 PM', 'status': 'Completed'},
    {'resident': 'Alice Smith', 'activity': 'Dinner with Peers', 'date': '2026-03-24', 'start_time': '06:00 PM', 'end_time': '06:45 PM', 'status': 'Upcoming'},
    {'resident': 'Alice Smith', 'activity': 'Reading Session', 'date': '2026-03-24', 'start_time': '08:00 PM', 'end_time': '08:30 PM', 'status': 'Upcoming'},
    {'resident': 'Bob Jones', 'activity': 'Physical Therapy', 'date': '2026-03-24', 'start_time': '11:00 AM', 'end_time': '11:45 AM', 'status': 'Upcoming'},
    {'resident': 'Charlie Brown', 'activity': 'Social Hour', 'date': '2026-03-24', 'start_time': '02:00 PM', 'end_time': '03:00 PM', 'status': 'Upcoming'}
]

MOCK_REPORTS = [
    {'date': '2023-10-26', 'resident': 'Alice Smith', 'summary': 'Excellent vitals, very active today.'},
    {'date': '2023-10-25', 'resident': 'Alice Smith', 'summary': 'Stable condition, participated in all activities.'},
    {'date': '2023-10-24', 'resident': 'Alice Smith', 'summary': 'Routine checkup normal.'},
    {'date': '2023-10-23', 'resident': 'Alice Smith', 'summary': 'Mild fatigue after morning walk, recovery quick.'},
    {'date': '2023-10-26', 'resident': 'Bob Jones', 'summary': 'Checkup required for BP issues.'},
    {'date': '2023-10-25', 'resident': 'Alice Brown', 'summary': 'Activity good, mood positive.'}
]

MOCK_RESIDENTS = [
    {'name': 'Alice Smith', 'age': 82, 'room': '101', 'emergency_contact': 'John Smith (Son) - 555-0199'},
    {'name': 'Bob Jones', 'age': 75, 'room': '102', 'emergency_contact': 'Sarah Jones (Daughter) - 555-0122'},
    {'name': 'Charlie Brown', 'age': 88, 'room': '103', 'emergency_contact': 'Lucy Brown (Wife) - 555-0155'}
]

MOCK_MEDICATIONS = [
    {'resident': 'Alice Smith', 'medication': 'Lisinopril', 'dosage': '10mg', 'freq': 'Once Daily', 'status': 'Taken'},
    {'resident': 'Alice Smith', 'medication': 'Metformin', 'dosage': '500mg', 'freq': 'Twice Daily', 'status': 'Pending'},
    {'resident': 'Bob Jones', 'medication': 'Amlodipine', 'dosage': '5mg', 'freq': 'Once Daily', 'status': 'Overdue'}
]

MOCK_NOTIFICATIONS = [
    {'type': 'Medication', 'message': 'Alice Smith: Metformin due at 06:00 PM', 'status': 'Upcoming'},
    {'type': 'Activity', 'message': 'Group Therapy starting in 15 mins', 'status': 'Now'},
    {'type': 'System', 'message': 'New health reading recorded for Bob Jones', 'status': 'Read'}
]

MOCK_AUDIT_LOGS = [
    {'user': 'nurse', 'action': 'Recorded Health Reading', 'target': 'Alice Smith', 'time': '10:30 AM'},
    {'user': 'admin', 'action': 'Updated Role', 'target': 'caregiver', 'time': '09:00 AM'},
    {'user': 'doctor', 'action': 'Modified Prescription', 'target': 'Bob Jones', 'time': 'Yesterday'}
]

# Role Access Permissions
# Defines which ROLES can access which FEATURES with granular Read/Write
PERMISSIONS = {
    'Admin': [
        'health:read', 'health:write',
        'activity:read', 'activity:write',
        'alerts:read', 'alerts:write',
        'reports:read', 'reports:write',
        'users:read', 'users:write',
        'residents:read', 'residents:write',
        'medication:read', 'medication:write',
        'notifications:read',
        'audit:read',
        'settings:read', 'settings:write'
    ],
    'Nurse': ['health:read', 'health:write', 'reports:read', 'reports:write', 'residents:read', 'medication:read', 'medication:write', 'notifications:read'],
    'Doctor': ['health:read', 'health:write', 'reports:read', 'reports:write', 'residents:read', 'medication:read', 'medication:write', 'notifications:read'],
    'Caregiver': ['activity:read', 'activity:write', 'alerts:read', 'alerts:write', 'residents:read', 'notifications:read'],
    'Resident': ['health:read', 'activity:read', 'alerts:read', 'alerts:write', 'medication:read', 'notifications:read'],
    'Family': ['health:read', 'activity:read', 'alerts:read', 'reports:read', 'medication:read', 'notifications:read']
}

# Helper to check permission
def check_permission(feature_name, action='read'):
    if 'user' not in session:
        return False
    role = session['role']
    permission_key = f"{feature_name}:{action}"
    if role in PERMISSIONS and permission_key in PERMISSIONS[role]:
        return True
    return False

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and USERS[username]['password'] == password:
            session['user'] = username
            session['role'] = USERS[username]['role']
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid Credentials. Please try again.'
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    role = session['role']
    # Pass the allowed permissions to the template to conditionally render buttons
    allowed_features = PERMISSIONS.get(role, [])
    
    if role == 'Resident':
        return render_template('resident_dashboard.html', user=session['user'], role=role, allowed_features=allowed_features)
    
    return render_template('dashboard.html', user=session['user'], role=role, allowed_features=allowed_features)

# --- Feature Pages ---

@app.route('/health_monitoring', methods=['GET', 'POST'])
def health_monitoring():
    if not check_permission('health', 'read'):
        return "Access Denied: You do not have permission to view this page.", 403
    
    can_write = check_permission('health', 'write')
    message = ""
    if request.method == 'POST':
        if not can_write:
            return "Access Denied: You do not have permission to record data.", 403
        message = "Success: Health data recorded (Prototype Simulation)"
    
    # Filtering Logic for Privacy
    role = session['role']
    user = session['user']
    if role in ['Resident', 'Family']:
        target_name = ASSOCIATED_RESIDENTS.get(user)
        display_data = [d for d in MOCK_HEALTH if d['resident'] == target_name]
    else:
        display_data = MOCK_HEALTH
        
    return render_template('health.html', message=message, can_write=can_write, health_data=display_data)

def check_conflict(resident, date, start_str, end_str):
    import datetime
    try:
        new_start = datetime.datetime.strptime(start_str, "%H:%M")
        new_end = datetime.datetime.strptime(end_str, "%H:%M")
        
        # LOGICAL CHECK: End must be after Start
        if new_end <= new_start:
            return "Error: End time must be after start time."
    except:
        return False
    
    for act in MOCK_ACTIVITIES:
        if act['resident'] == resident and act['date'] == date:
            try:
                ext_start = datetime.datetime.strptime(act['start_time'], "%I:%M %p")
                ext_end = datetime.datetime.strptime(act['end_time'], "%I:%M %p")
                
                ext_start = ext_start.replace(year=1900, month=1, day=1)
                ext_end = ext_end.replace(year=1900, month=1, day=1)
                new_start = new_start.replace(year=1900, month=1, day=1)
                new_end = new_end.replace(year=1900, month=1, day=1)

                if (new_start < ext_end) and (new_end > ext_start):
                    return "Conflict: This resident already has an activity scheduled during this time."
            except:
                continue
    return None

@app.route('/activity_management', methods=['GET', 'POST'])
def activity_management():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    can_write = check_permission('activity', 'write')
    message = request.args.get('message', "")
    error = request.args.get('error', "")
    
    if request.method == 'POST':
        if not can_write:
            return "Access Denied: You do not have permission to record activities.", 403
        
        action = request.form.get('action', 'add')
        
        if action == 'update_status':
            idx = int(request.form.get('activity_index'))
            new_status = request.form.get('new_status')
            if 0 <= idx < len(MOCK_ACTIVITIES):
                MOCK_ACTIVITIES[idx]['status'] = new_status
                return redirect(url_for('activity_management', message=f"Success: Activity marked as {new_status}"))
        else:
            resident_name = request.form.get('resident_name')
            activity_type = request.form.get('activity_type')
            date = request.form.get('date', '2026-03-24')
            raw_start = request.form.get('start_time', '08:00')
            raw_end = request.form.get('end_time', '09:00')
            
            conflict_msg = check_conflict(resident_name, date, raw_start, raw_end)
            if conflict_msg:
                return redirect(url_for('activity_management', error=conflict_msg))

            import datetime
            try:
                start_time = datetime.datetime.strptime(raw_start, "%H:%M").strftime("%I:%M %p")
                end_time = datetime.datetime.strptime(raw_end, "%H:%M").strftime("%I:%M %p")
            except:
                start_time = raw_start
                end_time = raw_end

            MOCK_ACTIVITIES.append({
                'resident': resident_name,
                'activity': activity_type,
                'date': date,
                'start_time': start_time,
                'end_time': end_time,
                'status': 'Upcoming'
            })
            return redirect(url_for('activity_management', message=f"Success: {activity_type} scheduled for {resident_name}"))

    if not check_permission('activity', 'read'):
        return "Access Denied: You do not have permission to view this page.", 403

    # Filtering Logic for Privacy
    role = session['role']
    user = session['user']
    if role in ['Resident', 'Family']:
        target_name = ASSOCIATED_RESIDENTS.get(user)
        display_data = [a for a in MOCK_ACTIVITIES if a['resident'] == target_name]
    else:
        display_data = MOCK_ACTIVITIES

    return render_template('activity.html', message=message, error=error, can_write=can_write, activities=display_data, residents=MOCK_RESIDENTS)

@app.route('/emergency_alerts', methods=['GET', 'POST'])
def emergency_alerts():
    if not check_permission('alerts', 'read'):
        return "Access Denied: You do not have permission to view this page.", 403

    can_write = check_permission('alerts', 'write')
    message = ""
    if request.method == 'POST':
        if not can_write:
            return "Access Denied: You do not have permission to trigger alerts.", 403
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"ALERT TRIGGERED at {timestamp}!"

    return render_template('alerts.html', message=message, can_write=can_write)

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if not check_permission('reports', 'read'):
        return "Access Denied: You do not have permission to view this page.", 403
    
    can_write = check_permission('reports', 'write')
    message = ""
    if request.method == 'POST':
        if not can_write:
            return "Access Denied", 403
        message = "Success: Report generated and archived (Prototype Simulation)"
    
    # Filtering Logic for Privacy
    role = session['role']
    user = session['user']
    if role in ['Resident', 'Family']:
        target_name = ASSOCIATED_RESIDENTS.get(user)
        display_data = [r for r in MOCK_REPORTS if r['resident'] == target_name]
    else:
        display_data = MOCK_REPORTS
        
    return render_template('reports.html', report_data=display_data, can_write=can_write, message=message)

@app.route('/user_management')
def user_management():
    if not check_permission('users', 'read'):
        return "Access Denied: You do not have permission to view this page.", 403
    
    # List all users
    user_list = []
    for u, details in USERS.items():
        user_list.append({'username': u, 'role': details['role']})
        
    return render_template('users.html', users=user_list)

@app.route('/residents')
def residents():
    if not check_permission('residents', 'read'):
        return "Access Denied", 403
    
    role = session['role']
    user = session['user']
    if role in ['Resident', 'Family']:
        target_name = ASSOCIATED_RESIDENTS.get(user)
        display_data = [r for r in MOCK_RESIDENTS if r['name'] == target_name]
    else:
        display_data = MOCK_RESIDENTS
        
    can_write = check_permission('residents', 'write')
    return render_template('residents.html', residents=display_data, can_write=can_write)

@app.route('/medication', methods=['GET', 'POST'])
def medication():
    if not check_permission('medication', 'read'):
        return "Access Denied", 403
    
    can_write = check_permission('medication', 'write')
    message = ""
    if request.method == 'POST':
        message = "Success: Medication record updated (Prototype)"
        
    role = session['role']
    user = session['user']
    if role in ['Resident', 'Family']:
        target_name = ASSOCIATED_RESIDENTS.get(user)
        display_data = [m for m in MOCK_MEDICATIONS if m['resident'] == target_name]
    else:
        display_data = MOCK_MEDICATIONS
        
    return render_template('medication.html', medication_data=display_data, can_write=can_write, message=message)

@app.route('/notifications')
def notifications():
    if not check_permission('notifications', 'read'):
        return "Access Denied", 403
    return render_template('notifications.html', notifications=MOCK_NOTIFICATIONS)

@app.route('/audit_logs')
def audit_logs():
    if not check_permission('audit', 'read'):
        return "Access Denied", 403
    return render_template('audit_logs.html', logs=MOCK_AUDIT_LOGS)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if not check_permission('settings', 'read'):
        return "Access Denied", 403
    
    message = ""
    if request.method == 'POST':
        message = "Success: System settings updated (Prototype)"
    return render_template('settings.html', message=message)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
