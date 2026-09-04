import { CheckCircle2, Circle, Clock } from 'lucide-react';

export default function ProgressTracker({ currentStep, totalSteps, status }) {
  const steps = [
    { num: 1, label: 'Searching Information' },
    { num: 2, label: 'Analyzing Results' },
    { num: 3, label: 'Identifying Entities' },
    { num: 4, label: 'Gathering Details' },
    { num: 5, label: 'Synthesizing Report' },
    { num: 6, label: 'Formatting Report' },
    { num: 7, label: 'Complete' },
  ];

  const progressPercentage = currentStep ? (currentStep / totalSteps) * 100 : 0;

  return (
    <div className="card mb-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Research Progress</h3>

      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex justify-between text-sm text-gray-600 mb-2">
          <span>Step {currentStep} of {totalSteps}</span>
          <span>{Math.round(progressPercentage)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div
            className="bg-gradient-to-r from-primary to-secondary h-full transition-all duration-300"
            style={{ width: `${progressPercentage}%` }}
          />
        </div>
      </div>

      {/* Status */}
      <div className="mb-6">
        <p className={`text-sm font-semibold mb-2 ${
          status === 'completed' ? 'text-secondary' :
          status === 'error' ? 'text-danger' :
          'text-primary'
        }`}>
          Status: <span className="capitalize">{status}</span>
        </p>
      </div>

      {/* Steps Timeline */}
      <div className="space-y-3">
        {steps.map((step) => {
          const isCompleted = currentStep > step.num;
          const isCurrent = currentStep === step.num;

          return (
            <div key={step.num} className="flex items-center gap-3">
              <div className="flex-shrink-0">
                {isCompleted ? (
                  <CheckCircle2 size={24} className="text-secondary" />
                ) : isCurrent ? (
                  <Clock size={24} className="text-primary animate-spin" />
                ) : (
                  <Circle size={24} className="text-gray-300" />
                )}
              </div>
              <div className="flex-grow">
                <p className={`font-medium ${
                  isCompleted || isCurrent ? 'text-gray-800' : 'text-gray-400'
                }`}>
                  {step.label}
                </p>
              </div>
              {isCompleted && (
                <span className="text-xs text-secondary font-semibold">✓</span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}