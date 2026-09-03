import React from 'react';

export default function BrandLogo({ className = "h-9 w-auto" }) {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      viewBox="0 0 240 60" 
      className={className}
      fill="none"
    >
      <rect x="6" y="8" width="44" height="44" rx="12" fill="url(#gradLogo)" />
      <path d="M16 30h6l3-7 5 15 4-11 3 5h7" stroke="#ffffff" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round"/>
      <circle cx="40" cy="20" r="3" fill="#38BDF8"/>
      <defs>
        <linearGradient id="gradLogo" x1="6" y1="8" x2="50" y2="52" gradientUnits="userSpaceOnUse">
          <stop stopColor="#0284C7"/>
          <stop offset="1" stopColor="#0EA5E9"/>
        </linearGradient>
      </defs>
      <text x="60" y="34" fontFamily="system-ui, -apple-system, sans-serif" fontWeight="800" fontSize="22" fill="#0F172A" letterSpacing="-0.5px">
        Clinix<tspan fill="#0284C7">IQ</tspan>
      </text>
      <text x="60" y="47" fontFamily="system-ui, -apple-system, sans-serif" fontWeight="600" fontSize="9" fill="#0284C7" letterSpacing="1.2px">
        CLINICAL AI TRIAGE
      </text>
    </svg>
  );
}
