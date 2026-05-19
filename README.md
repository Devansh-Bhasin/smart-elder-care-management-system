# Smart Elder Care Management System (Prototype)

**Course:** INFO3150 - Object Oriented Systems & Engineering  
**Submission:** Prototype Iteration 2 (Submission 2)  

---

## 👥 Team 1 members
*   **Devansh Bhasin**
*   **Saurav Kharal**
*   **Pasang Sherpa**
*   **Jimmy Lu**

---

### 📅 Advanced Activity Management System
Our **Activity Management module** has been built to be intentionally robust, addressing common practical scheduling challenges:
*   **Native Time Picker & AM/PM Formatting**: Integrated standard `<input type="time">` elements for intuitive and error-free time selection. The backend automatically converts these 24-hour inputs into user-friendly AM/PM displays (e.g., "14:30" → "02:30 PM").
*   **Intelligent Conflict Detection**: The system's logical engine prevents overlapping activities by validating new entries against existing schedules for the same resident and date.
*   **Logical Time Validation**: Enforces strict scheduling rules by ensuring the "End Time" is always set later than the "Start Time."
*   **One-Way Status Transitions**: All activities default to **"Upcoming"**. Caregivers can manually mark them as **"Completed"** or **"Skipped"**, providing a clear and professional audit trail.
*   **Post-Action Redirection**: Implemented the **Post/Redirect/Get** pattern to ensure that the activity log remains accurate and free from duplicate entries, even if the user refreshes their browser.

---

## 🔐 Prototype Credentials Guide
Log in with these credentials to access different system perspectives:

| Role | Username | Password | Key Access |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | User Management & Registration |
| **Nurse** | `nurse` | `nurse123` | Clinical Records & Medications |
| **Doctor** | `doctor` | `doctor123` | Clinical Analysis & Reports |
| **Caregiver** | `caregiver` | `caregiver123` | Daily Activities & Alerts |
| **Resident** | `resident1` | `res123` | Personal Schedule & Help alerts |
| **Family Member** | `family1` | `fam123` | Restricted Resident View |

---

## 📂 System Architecture
- **Architecture Style**: **3-Tier Layered Pattern** (Presentation, Logic, Data).
- **Backend**: Python (Flask) with granular RBAC (Role-Based Access Control).
- **Frontend**: Responsive HTML5/CSS3 with Jinja2 Templating and Glassmorphism design.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Flask (`pip install flask`)

### Execution
1.  Navigate to the project root.
2.  Run the application: `python app.py`
3.  Open: `http://127.0.0.1:5000/`

---

## 📄 Prototype Disclaimer
This prototype is a functional demonstration designed to **validate requirements** and **Object-Oriented Design patterns**. System features like persistent databases and AI sensors are simulated via interactive mock data to illustrate the final user experience.
