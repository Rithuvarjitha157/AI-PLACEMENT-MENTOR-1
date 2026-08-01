/**
 * ReadinessGauge — the signature visual element of the app.
 * A radial "mission control" dial with a large mono-numeral readout,
 * used consistently anywhere a score/percentage is shown.
 */
export default function ReadinessGauge({ value = 0, label, size = 120, accent = "#FFB100" }) {
  const stroke = 10;
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const clamped = Math.max(0, Math.min(100, value));
  const offset = circumference - (clamped / 100) * circumference;

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#E7EAF1"
            strokeWidth={stroke}
            fill="none"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={accent}
            strokeWidth={stroke}
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            style={{ transition: "stroke-dashoffset 0.6s ease" }}
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="font-mono-score text-2xl font-bold text-ink">{Math.round(clamped)}</span>
        </div>
      </div>
      {label && (
        <span className="text-xs font-semibold tracking-wide text-slate-text uppercase text-center">
          {label}
        </span>
      )}
    </div>
  );
}
