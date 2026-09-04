import { useState, useEffect, useRef } from 'react';
import SearchForm from './components/SearchForm';
import ProgressTracker from './components/ProgressTracker';
import ResultsDisplay from './components/ResultsDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import { researchAPI } from './services/api';
import { AlertCircle } from 'lucide-react';
import './index.css';

export default function App() {
  const [currentResearch, setCurrentResearch] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const pollIntervalRef = useRef(null);

  // Poll research status
  useEffect(() => {
    if (!currentResearch) return;

    const pollStatus = async () => {
      try {
        const status = await researchAPI.getResearchStatus(currentResearch);
        
        // Extract step number from status
        if (status.result?.research_steps) {
          setCurrentStep(status.result.research_steps.length);
        }

        if (status.status === 'completed') {
          setResult(status.result);
          setIsLoading(false);
          setCurrentStep(7);
          clearInterval(pollIntervalRef.current);
        } else if (status.status === 'error') {
          setError(status.error || 'Research failed');
          setIsLoading(false);
          clearInterval(pollIntervalRef.current);
        }
      } catch (err) {
        console.error('Polling error:', err);
      }
    };

    // Poll every 2 seconds
    pollIntervalRef.current = setInterval(pollStatus, 2000);

    return () => clearInterval(pollIntervalRef.current);
  }, [currentResearch]);

  const handleStartResearch = async (topic) => {
    setError(null);
    setResult(null);
    setCurrentStep(0);
    setIsLoading(true);

    try {
      const response = await researchAPI.startResearch(topic);
      setCurrentResearch(response.research_id);
      setCurrentStep(1);
    } catch (err) {
      setError(err.message);
      setIsLoading(false);
    }
  };

  const handleNewResearch = () => {
    setCurrentResearch(null);
    setIsLoading(false);
    setCurrentStep(0);
    setResult(null);
    setError(null);
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                🔍 Research Agent
              </h1>
              <p className="text-gray-600 text-sm mt-1">
                AI-powered research information gathering
              </p>
            </div>
            {result && (
              <button
                onClick={handleNewResearch}
                className="btn-primary"
              >
                New Research
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
            <AlertCircle className="text-danger flex-shrink-0 mt-0.5" size={20} />
            <div>
              <h3 className="font-semibold text-red-900">Error</h3>
              <p className="text-red-700 text-sm mt-1">{error}</p>
            </div>
          </div>
        )}

        {/* Search Form */}
        {!result && (
          <SearchForm
            onSubmit={handleStartResearch}
            isLoading={isLoading}
          />
        )}

        {/* Progress Tracker */}
        {isLoading && (
          <>
            <ProgressTracker
              currentStep={currentStep}
              totalSteps={7}
              status="in_progress"
            />
            <LoadingSpinner />
          </>
        )}

        {/* Results Display */}
        {result && !isLoading && (
          <>
            <ProgressTracker
              currentStep={7}
              totalSteps={7}
              status="completed"
            />
            <ResultsDisplay result={result} />
          </>
        )}

        {/* Empty State */}
        {!isLoading && !result && !error && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🚀</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">
              Ready to Research?
            </h2>
            <p className="text-gray-600">
              Enter a topic above to start gathering research information
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-50 border-t border-gray-200 mt-12">
        <div className="max-w-6xl mx-auto px-4 py-6 text-center text-gray-600 text-sm">
          <p>
            Agentic AI Research Agent • Powered by Google Gemini • Built with React
          </p>
        </div>
      </footer>
    </div>
  );
}