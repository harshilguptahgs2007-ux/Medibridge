import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { lazy, Suspense } from "react";

// Shell Layouts
import { PatientLayout } from "./layouts/PatientLayout";
import { DoctorLayout } from "./layouts/DoctorLayout";

// Shared Login Page
import { LoginRegister } from "./pages/LoginRegister";

// Patient Pages — lazy loaded per route
const PatientDashboard    = lazy(() => import("./pages/patient/PatientDashboard").then(m => ({ default: m.PatientDashboard })));
const PatientAppointments = lazy(() => import("./pages/patient/PatientAppointments").then(m => ({ default: m.PatientAppointments })));
const DoctorList          = lazy(() => import("./pages/patient/DoctorList").then(m => ({ default: m.DoctorList })));
const MedicalRecords      = lazy(() => import("./pages/patient/MedicalRecords").then(m => ({ default: m.MedicalRecords })));
const OcrScanner          = lazy(() => import("./pages/patient/OcrScanner").then(m => ({ default: m.OcrScanner })));
const AiBriefing          = lazy(() => import("./pages/patient/AiBriefing").then(m => ({ default: m.AiBriefing })));
const PatientProfile      = lazy(() => import("./pages/patient/PatientProfile").then(m => ({ default: m.PatientProfile })));
const PatientPrescriptions= lazy(() => import("./pages/patient/PatientPrescriptions").then(m => ({ default: m.PatientPrescriptions })));

// Doctor Pages — lazy loaded per route
const DoctorDashboard     = lazy(() => import("./pages/doctor/DoctorDashboard").then(m => ({ default: m.DoctorDashboard })));
const DoctorAppointments  = lazy(() => import("./pages/doctor/DoctorAppointments").then(m => ({ default: m.DoctorAppointments })));
const DoctorRequests      = lazy(() => import("./pages/doctor/DoctorRequests").then(m => ({ default: m.DoctorRequests })));
const DoctorPrescriptions = lazy(() => import("./pages/doctor/DoctorPrescriptions").then(m => ({ default: m.DoctorPrescriptions })));
const DoctorProfile       = lazy(() => import("./pages/doctor/DoctorProfile").then(m => ({ default: m.DoctorProfile })));
const DoctorAiBriefer     = lazy(() => import("./pages/doctor/DoctorAiBriefer").then(m => ({ default: m.DoctorAiBriefer })));

import "./App.css";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Suspense fallback={<div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", fontSize: "1rem", color: "#6b7280" }}>Loading...</div>}>
          <Routes>
            {/* Public Authentication page */}
            <Route path="/login" element={<LoginRegister />} />

            {/* Patient Role-Protected dashboard tree */}
            <Route element={<ProtectedRoute allowedRoles={["patient"]} />}>
              <Route path="/patient" element={<PatientLayout />}>
                <Route index element={<PatientDashboard />} />
                <Route path="appointments" element={<PatientAppointments />} />
                <Route path="doctors" element={<DoctorList />} />
                <Route path="records" element={<MedicalRecords />} />
                <Route path="ocr" element={<OcrScanner />} />
                <Route path="ai-brief" element={<AiBriefing />} />
                <Route path="profile" element={<PatientProfile />} />
                <Route path="prescriptions" element={<PatientPrescriptions />} />
              </Route>
            </Route>

            {/* Doctor Role-Protected dashboard tree */}
            <Route element={<ProtectedRoute allowedRoles={["doctor"]} />}>
              <Route path="/doctor" element={<DoctorLayout />}>
                <Route index element={<DoctorDashboard />} />
                <Route path="appointments" element={<DoctorAppointments />} />
                <Route path="requests" element={<DoctorRequests />} />
                <Route path="prescriptions" element={<DoctorPrescriptions />} />
                <Route path="ai-briefer" element={<DoctorAiBriefer />} />
                <Route path="profile" element={<DoctorProfile />} />
              </Route>
            </Route>

            {/* Default fallback route redirection */}
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </Suspense>
      </Router>
    </AuthProvider>
  );
}

export default App;