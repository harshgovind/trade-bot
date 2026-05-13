import React, { useState } from 'react';

const HorizonSlider = ({ onHorizonChange }) => {
  const [days, setDays] = useState(30);

  const handleChange = (e) => {
    const value = e.target.value;
    setDays(value);
    onHorizonChange(value); // Triggers re-ranking in the backend
  };

  return (
    <div className="p-6 bg-slate-900 rounded-xl border border-slate-800">
      <div className="flex justify-between mb-4">
        <span className="text-slate-400 text-sm font-medium">Time Horizon (T)</span>
        <span className="text-blue-400 font-bold">{days} Days</span>
      </div>
      <input
        type="range"
        min="7"
        max="365"
        value={days}
        onChange={handleChange}
        className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
      />
      <div className="flex justify-between mt-2 text-[10px] text-slate-500 uppercase tracking-widest">
        <span>Short-Term (Momentum)</span>
        <span>Long-Term (Fundamental)</span>
      </div>
    </div>
  );
};

export default HorizonSlider;
