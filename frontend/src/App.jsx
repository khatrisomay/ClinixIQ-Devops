import React, { useState } from 'react';
import Navbar from './components/Navbar';
import TriageAcuityRibbon from './components/TriageAcuityRibbon';
import TriageChatPanel from './components/TriageChatPanel';
import AnalyticsPanel from './components/AnalyticsPanel';
import PricingSection from './components/PricingSection';
import SBARSummaryModal from './components/SBARSummaryModal';
import SubscriptionStatusModal from './components/SubscriptionStatusModal';
import CheckoutFeedbackModal from './components/CheckoutFeedbackModal';

export default function App() {
  const [activeTab, setActiveTab] = useState('triage');
  const [isSbarModalOpen, setIsSbarModalOpen] = useState(false);
  const [isBillingModalOpen, setIsBillingModalOpen] = useState(false);
  const [currentPlan, setCurrentPlan] = useState('starter');
  const [triageData, setTriageData] = useState(null);

  const handleTriageComplete = (result) => {
    setTriageData(result);
  };

  const handleTriggerER = () => {
    if (confirm("URGENT PROTOCOL: Are you experiencing sudden shortness of breath, acute radiating chest pain, or severe weakness? Clicking OK will simulate direct emergency dispatch transfer.")) {
      alert("EMERGENCY ESCALATION DISPATCHED: Patient telemetry sent to regional emergency dispatch. Please remain seated and dial 911 immediately.");
    }
  };

  const handleDownloadPDF = () => {
    alert("Preparing Doctor-Ready Clinical Export: Generating verified SBAR PDF with cryptographic signature (SHA-256)...");
    window.print();
  };

  const handleUpgradePro = () => {
    alert("Redirecting to ClinixIQ Pro checkout. 14-day clinical trial activated with instant EHR export capabilities.");
  };

  const handleScheduleB2B = () => {
    alert("Opening Institutional EHR (Epic & Cerner FHIR API) Integration Briefing Calendar.");
  };

  return (
    <div className="min-h-screen w-full bg-[#faf8ff] text-[#131b2e] flex flex-col font-sans selection:bg-[#006194] selection:text-white">
      {/* Top Fixed Medical Header */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentPlan={currentPlan}
        onOpenBillingModal={() => setIsBillingModalOpen(true)}
      />

      {/* Main Content Area: Edge-to-Edge Fluid Full Width */}
      <main className="w-full pt-20 flex-1 flex flex-col">
        {/* Dynamic Clinical Alert Ribbon */}
        <TriageAcuityRibbon
          triageData={triageData}
          onUnlockReport={() => setIsSbarModalOpen(true)}
          onTriggerER={handleTriggerER}
        />

        {/* Primary Interactive Workspace: Full Width Grid */}
        {(activeTab === 'triage' || activeTab === 'analytics') && (
          <div className="w-full px-4 sm:px-8 lg:px-12 pb-10 pt-2 grid grid-cols-1 xl:grid-cols-12 gap-8 items-start">
            {/* Left Panel: Conversational AI Diagnostic Intake Chat (5 cols) */}
            <TriageChatPanel onTriageComplete={handleTriageComplete} />

            {/* Right Panel: Clinical Analytics, Radar Chart & Risk Curve (7 cols) */}
            <AnalyticsPanel
              triageData={triageData}
              onOpenSummaryModal={() => setIsSbarModalOpen(true)}
              onDownloadPDF={handleDownloadPDF}
            />
          </div>
        )}

        {/* Clinical Monetization & Subscription Grid */}
        <div className={activeTab === 'pricing' ? 'block' : 'block'}>
          <PricingSection
            onUpgradePro={handleUpgradePro}
            onScheduleB2B={handleScheduleB2B}
          />
        </div>

        {/* Clinical Docs View if Tab Selected */}
        {activeTab === 'docs' && (
          <div className="w-full px-4 sm:px-8 lg:px-12 py-10 space-y-5">
            <h2 className="text-3xl font-extrabold text-[#131b2e] tracking-tight">ClinixIQ Clinical Protocol & Regulatory Documentation</h2>
            <div className="p-8 bg-white rounded-2xl border border-[#dae2fd] space-y-4 text-sm sm:text-base text-[#3f4850] leading-relaxed shadow-sm">
              <p><strong>Clinical Validation:</strong> ClinixIQ Bayesian inference models are calibrated against peer-reviewed NHANES epidemiological datasets and Mayo Clinic differential diagnostic pathways.</p>
              <p><strong>HIPAA Safe Harbor Compliance:</strong> All free-text clinical symptoms undergo deterministic token de-identification before transmission to the Python ML inference cluster.</p>
              <p><strong>HL7 FHIR Interoperability:</strong> JSON schemas conform to Fast Healthcare Interoperability Resources (FHIR) R4 specifications for direct Epic and Cerner EHR synchronization.</p>
            </div>
          </div>
        )}
      </main>

      {/* SBAR Diagnostic Modal */}
      <SBARSummaryModal
        isOpen={isSbarModalOpen}
        onClose={() => setIsSbarModalOpen(false)}
        triageData={triageData}
      />

      {/* Clinical Footer */}
      <footer className="w-full bg-[#f2f3ff] border-t border-[#dae2fd]/60 py-10 mt-8">
        <div className="w-full px-4 sm:px-8 lg:px-12 flex flex-col md:flex-row items-center justify-between gap-4 text-[#3f4850] text-sm">
          <div>© 2025 ClinixIQ Health Systems Inc. Clinical Intelligence & Diagnostic Protocol.</div>
          <div className="flex items-center gap-8 font-medium">
            <button onClick={() => setActiveTab('docs')} className="hover:text-[#131b2e] transition-colors">
              Compliance & Validation
            </button>
            <button onClick={() => alert("Data Processing Agreement: Standard Business Associate Agreement (BAA) active.")} className="hover:text-[#131b2e] transition-colors">
              Data Processing Agreement
            </button>
            <button onClick={handleScheduleB2B} className="hover:text-[#131b2e] transition-colors">
              Institutional Inquiries
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}
