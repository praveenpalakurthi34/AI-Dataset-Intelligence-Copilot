import { CheckCircle2, Target, Zap, Bot } from "lucide-react";

interface Decision {
  decision: string;
  target: string;
  confidence: number;
  reason: string;
  expected_impact: string;
  auto_fix: boolean;
}

interface Props {
  decision: Decision;
}

export default function DecisionCard({ decision }: Props) {
  return (
    <div className="rounded-xl border border-slate-700 bg-slate-900 p-5 shadow">

      <div className="flex items-center justify-between">

        <h3 className="font-bold text-lg text-white flex items-center gap-2">
          <CheckCircle2 className="text-emerald-400" />
          {decision.decision}
        </h3>

        <span
          className={`px-3 py-1 rounded-full text-xs font-semibold ${
            decision.auto_fix
              ? "bg-green-500/20 text-green-400"
              : "bg-red-500/20 text-red-400"
          }`}
        >
          {decision.auto_fix ? "Auto Fix" : "Manual Review"}
        </span>

      </div>

      <div className="mt-4 space-y-3 text-sm">

        <div className="flex items-center gap-2">
          <Target className="w-4 h-4 text-blue-400" />
          <span className="text-slate-300">
            <strong>Target:</strong> {decision.target}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <Zap className="w-4 h-4 text-yellow-400" />
          <span className="text-slate-300">
            <strong>Confidence:</strong> {decision.confidence}%
          </span>
        </div>

        <div>
          <p className="text-slate-400 font-semibold">
            Reason
          </p>

          <p className="text-slate-300 mt-1">
            {decision.reason}
          </p>
        </div>

        <div>
          <p className="text-slate-400 font-semibold">
            Expected Impact
          </p>

          <p className="text-green-400 mt-1">
            {decision.expected_impact}
          </p>
        </div>

        <div className="flex items-center gap-2 pt-2">
          <Bot className="w-4 h-4 text-violet-400" />

          <span className="text-slate-300">
            {decision.auto_fix
              ? "This action can be performed automatically."
              : "Manual verification is recommended."}
          </span>
        </div>

      </div>

    </div>
  );
}