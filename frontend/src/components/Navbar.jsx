import React, { useState } from 'react';
import BrandLogo from './BrandLogo';

export default function Navbar({ activeTab, setActiveTab, onOpenPricing }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { id: 'triage', label: 'Triage Assistant' },
    { id: 'analytics', label: 'Risk Analytics' },
    { id: 'pricing', label: 'Pricing' },
    { id: 'docs', label: 'Clinical Docs' },
  ];

  return (
    <header className="fixed top-0 w-full z-50 bg-white/95 backdrop-blur-xl border-b border-[#dae2fd]/60 shadow-[0_1px_8px_rgba(0,0,0,0.04)]">
      <div className="h-16 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between gap-4">
        {/* Brand and Certification Badge */}
        <div className="flex items-center gap-6">
          <div 
            className="flex items-center cursor-pointer transition-opacity hover:opacity-90"
            onClick={() => setActiveTab('triage')}
          >
            <BrandLogo className="h-9 w-auto object-contain" />
          </div>

          <div className="hidden xl:flex items-center gap-2 px-3 py-1 rounded-full bg-[#6cf8bb]/20 text-[#006c49] text-[11px] font-semibold">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#006c49] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-[#006c49]"></span>
            </span>
            <span>HIPAA & GDPR Ready • TLS Encrypted</span>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden md:flex items-center gap-1.5">
          {navLinks.map((link) => (
            <button
              key={link.id}
              onClick={() => setActiveTab(link.id)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === link.id
                  ? 'bg-[#007bb9] text-white font-semibold shadow-sm'
                  : 'text-[#3f4850] hover:text-[#131b2e] hover:bg-[#eaedff]'
              }`}
            >
              {link.label}
            </button>
          ))}
        </nav>

        {/* Right CTA and Patient Profile */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setActiveTab('pricing')}
            className="hidden sm:inline-flex items-center justify-center px-4 py-1.5 rounded-full bg-[#006194] text-white text-xs font-semibold hover:bg-[#007bb9] transition-all shadow-sm active:scale-95"
          >
            Upgrade to Pro
          </button>

          <div className="flex items-center gap-2 pl-1">
            <img
              alt="Clinical Patient Profile"
              className="w-8 h-8 rounded-full object-cover ring-2 ring-[#0284c7]/30 shadow-sm"
              src="https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=120"
            />
          </div>

          {/* Mobile hamburger button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-1.5 text-[#3f4850] hover:text-[#131b2e] rounded-lg hover:bg-[#eaedff]"
          >
            <span className="material-symbols-outlined text-[24px]">menu</span>
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-[#dae2fd] bg-white px-4 py-3 space-y-1 shadow-lg">
          {navLinks.map((link) => (
            <button
              key={link.id}
              onClick={() => {
                setActiveTab(link.id);
                setMobileMenuOpen(false);
              }}
              className={`block w-full text-left px-3 py-2 text-sm rounded-lg font-medium ${
                activeTab === link.id
                  ? 'bg-[#007bb9] text-white'
                  : 'text-[#3f4850] hover:bg-[#eaedff]'
              }`}
            >
              {link.label}
            </button>
          ))}
        </div>
      )}
    </header>
  );
}
