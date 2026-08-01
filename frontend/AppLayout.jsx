export function Card({ children, className = "" }) {
  return (
    <div className={`bg-white rounded-card shadow-card border border-black/5 p-6 ${className}`}>
      {children}
    </div>
  );
}

export function CardHeader({ icon, title, accent = "text-ink" }) {
  return (
    <div className="flex items-center gap-2 mb-4">
      {icon && <span className={`text-lg ${accent}`}>{icon}</span>}
      <h3 className="font-display font-semibold text-sm uppercase tracking-wide text-ink">{title}</h3>
    </div>
  );
}

const CHIP_STYLES = {
  neutral: "bg-ink/5 text-ink",
  ready: "bg-ready-soft text-ready",
  gap: "bg-gap-soft text-gap",
  signal: "bg-signal-soft text-ink",
};

export function SkillChip({ label, tone = "neutral" }) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold ${CHIP_STYLES[tone]}`}
    >
      {label}
    </span>
  );
}

const STATUS_STYLES = {
  Missing: "bg-gap-soft text-gap",
  Weak: "bg-signal-soft text-ink",
  Good: "bg-ready-soft text-ready",
};

export function StatusBadge({ status }) {
  return (
    <span
      className={`px-2.5 py-1 rounded-full text-[11px] font-bold uppercase tracking-wide ${
        STATUS_STYLES[status] || STATUS_STYLES.Weak
      }`}
    >
      {status}
    </span>
  );
}

export function ImportanceBadge({ importance }) {
  const dot =
    importance === "High" ? "bg-gap" : importance === "Medium" ? "bg-signal" : "bg-ready";
  return (
    <span className="inline-flex items-center gap-1.5 text-xs text-slate-text font-medium">
      <span className={`w-1.5 h-1.5 rounded-full ${dot}`} />
      {importance}
    </span>
  );
}
