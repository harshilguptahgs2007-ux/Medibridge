# MediBridge — AI-Powered Clinical Care Platform

> **MediBridge** is a full-stack healthcare platform designed to connect patients and doctors through appointment management, medical records, prescriptions, document OCR, AI-assisted clinical briefs, and an AI health assistant.

---

##  What is MediBridge?

MediBridge brings important parts of a patient's healthcare journey into one platform.

Instead of keeping appointments, prescriptions, uploaded reports, and medical history in separate places, MediBridge provides a shared digital workflow for **patients and authorized doctors**.

The platform has two main experiences:

- **Patient Portal** — book appointments, upload medical documents, view prescriptions and records, get AI-assisted specialty guidance, and interact with MediBot.
- **Doctor Clinical Studio** — manage appointments, review authorized patients, create prescriptions, generate Google Meet appointments, and use an AI Medical Briefer to summarize clinical history.

---

##  Problem We Are Solving

Healthcare information is often fragmented:

- Patients may have reports and prescriptions stored in different places.
- Doctors may need to review multiple records before a consultation.
- Appointment coordination can require unnecessary back-and-forth.
- Important information in scanned medical documents is difficult to process manually.
- Patients often need help understanding what type of doctor they should consult.
- Doctors need a quick overview of a patient's previous clinical information.

### Our approach

**MediBridge creates a single digital bridge between patient information and clinical workflow.**

```text
Patient
   │
   ├── Profile
   ├── Medical Documents
   ├── Appointments
   ├── Prescriptions
   └── AI Health Assistant
          │
          ▼
     MediBridge API
          │
          ├── OCR / Document Processing
          ├── AI Assistance
          ├── Patient History
          ├── Prescription Generation
          └── Google Meet
          │
          ▼
Doctor Clinical Studio
   │
   ├── Appointment Management
   ├── Authorized Patients
   ├── Clinical History
   ├── AI Medical Brief
   └── Prescription Management
```

---

#  Key Features

## 1. Role-Based Patient & Doctor Portals

Users can register/login and access functionality based on their role.

### Patient features
- Patient profile management
- Browse doctors
- AI-assisted specialty recommendation
- Book appointments
- Accept/reject suggested appointment times
- Upload medical documents
- View medical records
- View and download prescriptions
- AI patient briefing
- MediBot AI assistant
- Voice input/output support

### Doctor features
- Doctor profile management
- Today's/active appointment schedule
- Accept appointments
- Suggest appointment times
- View authorized patients
- Review patient clinical history
- Generate AI clinical briefs
- Create prescriptions
- Download prescription files
- Create Google Meet appointments
- Maintain prescription archive

---

## 2.  MediBot AI Assistant

The dashboard includes **MediBot**, an AI-powered health assistant.

It can help users with general health-related questions, medicine information, appointment guidance, and navigation of MediBridge features.

The interface supports:

- Conversational chat
- Quick prompts
- Voice input
- Text-to-speech
- Patient/doctor role-aware conversations
- Hindi + English interaction support

> **Important:** MediBot is an AI assistance layer and should not be treated as a replacement for a qualified medical professional or emergency medical care.

---

## 3.  Doctor AI Medical Briefer

One of the core features for doctors is the **AI Medical Briefer**.

A doctor selects an authorized patient and MediBridge collects available clinical context such as:

- Patient information
- Previous appointment logs
- Prior prescriptions
- Uploaded medical documents

The system then produces a structured clinical brief to help the doctor quickly understand the patient's history before a consultation.

The UI is designed around a structured multi-section brief rather than presenting the doctor with one large block of AI-generated text.

### Why this matters

Instead of manually going through multiple records:

```text
Multiple Records
      ↓
Patient History
      ↓
AI Processing
      ↓
Structured Clinical Brief
      ↓
Doctor Review
```

This is intended to **reduce information overload and improve consultation preparation**.

---

## 4. Medical Document OCR

Patients can upload medical documents/scans.

MediBridge sends supported documents/images through an OCR pipeline and extracts readable text.

The extracted information can then be used for downstream AI-assisted processing such as:

- Medical history summarization
- Medicine identification
- Clinical briefing

The backend uses image/document processing libraries and an external OCR service for supported OCR workflows.

---

## 5.  Medicine & Salt Identification

MediBridge contains a medicine/salt catalog and processing logic for identifying medicines from extracted text.

This helps convert OCR output into more useful medicine information.

The system also provides AI-assisted medicine explanations through the AI service layer.

> Medicine information shown by the platform is informational. Actual prescriptions and treatment decisions remain with qualified healthcare professionals.

---

## 6.  Digital Prescription Generation

Doctors can create prescriptions from the Doctor Clinical Studio.

MediBridge can generate prescription documents in:

- **PDF**
- **DOCX**

The generated prescription files can be stored and accessed through the patient/doctor prescription interfaces.

This creates a complete flow:

```text
Doctor Consultation
       ↓
Prescription Creation
       ↓
Prescription Record
       ↓
PDF / DOCX Generation
       ↓
Patient Access
```

---

## 7.  Appointment Management

The platform supports appointment workflows for both sides.

### Patient side
- View doctors
- Request/book appointments
- View appointment status
- Accept/reject suggested slots

### Doctor side
- View appointment requests
- Accept appointments
- Suggest alternative appointment times
- Create online meeting links

This makes the appointment lifecycle more structured than simple messaging-based coordination.

---

## 8.  Google Meet Integration

MediBridge can create online consultation meetings through the Google Calendar/Meet integration.

The backend provides an API that accepts:

- Start time
- Meeting title
- Duration

and returns the generated meeting information.

This allows an appointment to move from:

**Booking → Confirmation → Online Consultation**

without requiring a separate manual meeting-creation workflow.

---

#  Interface

### Doctor Dashboard

The Doctor Clinical Studio provides a clean clinical dashboard with:

- Confirmed consultations
- Pending requests
- Prescriptions issued
- Authorized patients
- Active consultation schedule
- Quick clinical actions

### AI Assistant

MediBot appears as an integrated assistant rather than a separate application, allowing users to ask questions while remaining inside the healthcare portal.

---

# Technology Stack

## Frontend

- **React**
- **Vite**
- **React Router**
- **Axios**
- **Lucide React**
- Browser Speech APIs / custom speech hooks

## Backend

- **Python**
- **Flask**
- **Flask-CORS**
- **PyJWT**
- **Werkzeug**
- **Pillow**
- **PyMuPDF**
- **pypdf**
- **ReportLab**
- **python-docx**

## AI / External Services

- **Groq API** — conversational and AI-assisted features
- **NVIDIA OCR API** — document/image OCR workflow
- **Google Calendar/Meet APIs** — online consultation creation

---

#  Project Structure

```text
MediBridge/
│
├── backend/
│   ├── requirements.txt
│   ├── prescriptions/
│   ├── uploads/
│   └── routes/
│       ├── index.py
│       ├── auth.py
│       ├── auth_utils.py
│       ├── patient.py
│       ├── doctor.py
│       ├── briefer.py
│       ├── med_salts.py
│       ├── prescription_generator.py
│       ├── meeting_generator.py
│       ├── storage.py
│       └── data/
│           ├── users.json
│           ├── patients.json
│           ├── doctors.json
│           ├── appointments.json
│           └── prescriptions.json
│
└── frontend/
    ├── package.json
    ├── index.html
    └── src/
        ├── api/
        ├── components/
        ├── context/
        ├── hooks/
        ├── layouts/
        └── pages/
            ├── doctor/
            └── patient/
```

---

#  API Overview

The Flask backend exposes APIs for the major application workflows.

### Authentication

```text
POST /api/auth/register
POST /api/auth/login
```

### Patient APIs

```text
GET  /api/patients/me
PUT  /api/patients/me

GET  /api/patients/doctors

POST /api/patients/appointments
GET  /api/patients/appointments

GET  /api/patients/prescriptions

GET  /api/patients/me/medical-documents
POST /api/patients/me/medical-documents

POST /api/patients/ai-recommend-specialty
```

### Doctor APIs

```text
GET  /api/doctors/profile
PUT  /api/doctors/profile

GET  /api/doctors/appointments
GET  /api/doctors/my-patients

PUT  /api/doctors/appointments/<id>/accept
PUT  /api/doctors/appointments/<id>/suggest

POST /api/doctors/appointments/<id>/meet

POST /api/doctors/appointments/<id>/prescription

GET  /api/doctors/patient/<id>/history
POST /api/doctors/patient/<id>/ai-brief
```

### AI / Document / Meeting APIs

```text
POST /api/extract
POST /upload
GET  /brief_assist

POST /api/create-meet
GET  /api/check-status

GET /
```

`GET /` acts as a simple backend health check and returns an `ok` status.

---

#  Running the Project Locally

## 1. Clone the project

```bash
git clone <YOUR_REPOSITORY_URL>
cd MediBridge
```

---

## 2. Start the Backend

Create a Python virtual environment:

```bash
cd backend

python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create/configure the environment variables required by the backend.

Then start Flask:

```bash
python routes/index.py
```

The backend runs on:

```text
http://localhost:5000
```

Health check:

```text
http://localhost:5000/
```

Expected response:

```json
{
  "status": "ok"
}
```

---

## 3. Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite will display the local frontend URL in the terminal, normally similar to:

```text
http://localhost:5173
```

Configure the frontend API base URL using:

```text
VITE_API_BASE_URL=http://localhost:5000
```

---

#  Environment Variables

Do **not** commit API keys, tokens, OAuth credentials, or `.env` files to GitHub.

Use `.env.example` files as templates.

Typical configuration includes:

### Backend

```env
SECRET_KEY=your-secret-key
NVIDIA_API_KEY=your-nvidia-key
NVIDIA_OCR_URL=your-ocr-url
KIMI_API_KEY=your-kimi-key
```

### Frontend

```env
VITE_API_BASE_URL=http://localhost:5000
```

Depending on the selected AI/integration workflow, additional credentials may be required.

###  Security before public submission

The supplied project archive contains credential-related files and API keys. **Rotate/revoke any exposed keys before pushing this project to a public repository.**

In particular, never publish:

```text
.env
credentials.json
token.json
API keys
OAuth tokens
```

Add them to `.gitignore` where appropriate.

---

#  End-to-End User Flow

## Patient

```text
Register / Login
      ↓
Patient Dashboard
      ↓
Find Doctor
      ↓
AI Specialty Guidance (optional)
      ↓
Book Appointment
      ↓
Doctor Accepts / Suggests Time
      ↓
Consultation
      ↓
Prescription
      ↓
View / Download Prescription
```

## Patient + AI

```text
Upload Medical Report
        ↓
OCR / Text Extraction
        ↓
Medical Information Processing
        ↓
AI-Assisted Summary
        ↓
Patient / Doctor Review
```

## Doctor

```text
Login
  ↓
Doctor Clinical Studio
  ↓
Appointment Requests
  ↓
Accept / Suggest Time
  ↓
Create Google Meet
  ↓
Select Authorized Patient
  ↓
Review History
  ↓
Generate AI Medical Brief
  ↓
Consult Patient
  ↓
Create Prescription
  ↓
Generate PDF / DOCX
```

---

#  Why MediBridge Stands Out

### 1. More than an appointment app

MediBridge combines **appointments + records + prescriptions + OCR + AI assistance + online consultation** in one workflow.

### 2. AI is connected to the workflow

AI is not only a chatbot. It is also used for:

- Specialty guidance
- Medical document processing
- Clinical briefing
- Medicine-related explanations
- Patient assistance

### 3. Doctor-focused AI

The **AI Medical Briefer** focuses on a real clinical workflow problem: helping doctors review available patient information before a consultation.

### 4. Patient-doctor continuity

The same platform connects the patient journey with the doctor's workflow instead of treating them as two unrelated applications.

### 5. Practical document handling

Prescription generation in **PDF and DOCX** makes the platform closer to a usable healthcare workflow.

---

#  Privacy & Responsible AI

MediBridge is designed as an **AI-assisted healthcare platform**, not an autonomous medical decision-maker.

AI-generated information should be reviewed by a qualified healthcare professional where appropriate.

For a production deployment, the system should additionally implement and/or strengthen:

- Encryption in transit and at rest
- Secure secret management
- Production-grade database storage
- Fine-grained authorization
- Audit logs
- Stronger file validation
- Rate limiting
- Secure OAuth token handling
- Medical-data retention policies
- Compliance review for applicable healthcare/privacy regulations

---

#  Current Project Scope

This project is suitable as a **hackathon/prototype demonstration** showing how AI can be integrated into a healthcare workflow.

The current implementation uses local JSON-based data/storage components for several application records, making it easy to demonstrate without requiring a complete production database infrastructure.

For production, the storage layer can be migrated to a secure relational/document database with proper access control and auditing.

---

#  Hackathon / Judge Pitch

> **MediBridge is an AI-powered clinical care platform that bridges the gap between patients and doctors. It combines appointment management, medical document OCR, prescription generation, online consultations, and AI-powered health assistance in a single workflow. Our key innovation is the Doctor AI Medical Briefer, which converts a patient's available history, prescriptions, appointment logs, and uploaded reports into a structured clinical overview—helping doctors spend less time searching through records and more time focusing on the patient.**

---

#  Demo Screens

The project UI includes:

- Doctor Clinical Studio dashboard
- Active consultation schedule
- AI Medical Briefer
- MediBot AI Assistant
- Patient dashboard
- Medical records
- Prescription archive
- Appointment management

For GitHub, screenshots can be placed in:

```text
docs/
├── doctor-dashboard.png
├── medibot.png
└── ai-medical-briefer.png
```

and embedded here using standard Markdown image syntax.

---

#  Team

**Project:** MediBridge  
**Category:** AI / Healthcare / Full-Stack Web Application

Add your team members, roles, GitHub repository, demo video, and live deployment links here before the final submission.

---

##  Future Enhancements

- PostgreSQL/MongoDB production database
- Real-time notifications
- Doctor-patient secure messaging
- Better clinical document classification
- More robust multilingual support
- Automated appointment reminders
- Advanced analytics for doctors
- Stronger authentication such as MFA
- Cloud-based secure file storage
- Comprehensive audit logging
- Production-grade healthcare privacy/compliance architecture

---

##  Final Summary

**MediBridge turns fragmented healthcare interactions into one connected digital workflow.**

**Patient → Records → AI Assistance → Appointment → Doctor → Clinical Brief → Consultation → Prescription**

The goal is simple:

> **Make healthcare information easier to access, easier to understand, and easier for doctors to act on—while keeping clinical decisions in human hands.**
