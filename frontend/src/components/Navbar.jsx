import React from 'react';
import BrandLogo from './BrandLogo';

export default function Navbar({ activeTab, setActiveTab }) {
  const navLinks = [
    { id: 'triage', label: 'Triage Assistant' },
    { id: 'analytics', label: 'Risk Analytics' },
    { id: 'pricing', label: 'Pricing' },
    { id: 'docs', label: 'Clinical Docs' },
  ];

  return (
    <header className="fixed top-0 w-full z-50 bg-white/95 backdrop-blur-xl border-b border-[#dae2fd]/70 shadow-[0_1px_12px_rgba(0,0,0,0.05)]">
      <div className="h-18 w-full max-w-[1560px] mx-auto px-4 sm:px-8 flex items-center justify-between gap-6 py-3">
        {/* Brand and Certification Badge */}
        <div className="flex items-center gap-6">
          <div 
            className="flex items-center cursor-pointer transition-transform hover:scale-[1.02]"
            onClick={() => setActiveTab('triage')}
          >
            <BrandLogo className="h-11 w-auto object-contain" />
          </div>

          <div className="hidden lg:flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#6cf8bb]/25 text-[#006c49] text-xs font-semibold border border-[#006c49]/15">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#006c49] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#006c49]"></span>
            </span>
            <span>HIPAA & GDPR Ready • TLS 1.3 Encrypted</span>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden md:flex items-center gap-2">
          {navLinks.map((link) => (
            <button
              key={link.id}
              onClick={() => setActiveTab(link.id)}
              className={`px-4 py-2 rounded-xl text-sm font-semibold transition-all ${
                activeTab === link.id
                  ? 'bg-[#007bb9] text-white shadow-md shadow-[#007bb9]/20'
                  : 'text-[#3f4850] hover:text-[#131b2e] hover:bg-[#eaedff]'
              }`}
            >
              {link.label}
            </button>
          ))}
        </nav>

        {/* Right CTA and Patient Profile */}
        <div className="flex items-center gap-4">
          <button
            onClick={() => setActiveTab('pricing')}
            className="hidden sm:inline-flex items-center justify-center px-5 py-2 rounded-full bg-[#006194] text-white text-xs font-bold hover:bg-[#007bb9] transition-all shadow-md shadow-[#006194]/20 active:scale-95"
          >
            Upgrade to Pro
          </button>

          <div className="flex items-center gap-2">
            <img
              alt="Clinical Patient Profile"
              className="w-10 h-10 rounded-full object-cover ring-2 ring-[#0284c7]/40 shadow-sm"
              src="https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=160"
            />
          </div>
        </div>
      </div>
    </header>
  );
}
