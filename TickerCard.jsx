import React from 'react';

const TickerCard = ({ ticker, probability, expectedMove, catalyst }) => {
  return (
    <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl hover:border-blue-500 transition-all cursor-pointer group">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-xl font-bold text-white">{ticker}</h3>
        <div className="text-right">
          <div className="text-blue-400 font-mono font-bold">{(probability * 100).toFixed(1)}%</div>
          <div className="text-[10px] text-slate-500 uppercase">P(Bullish)</div>
        </div>
      </div>
      <p className="text-slate-400 text-sm mb-4 italic leading-relaxed">
        "{catalyst}"
      </p>
      <div className="pt-4 border-t border-slate-800 flex justify-between items-center">
        <span className="text-xs text-slate-500">Exp. Move</span>
        <span className="text-green-400 font-medium">+{expectedMove}%</span>
      </div>
    </div>
  );
};

export default TickerCard;
