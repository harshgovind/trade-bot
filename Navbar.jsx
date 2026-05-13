// src/components/Navbar.jsx
import React from 'react';

const Navbar = ({ isFlashActive }) => {
  return (
    <nav className="flex justify-between p-4 bg-slate-900 border-b border-slate-800">
      <div className="flex gap-6">
        <button className="text-slate-300 hover:text-white">Dashboard</button>
        
        {/* PASTE THE CODE HERE */}
        <button className="relative p-2">
          <span className="text-slate-300">Flash Signals</span>
          {isFlashActive && (
            <span className="absolute top-0 right-0 flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
            </span>
          )}
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
