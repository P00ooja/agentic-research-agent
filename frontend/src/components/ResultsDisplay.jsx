import { ExternalLink, Copy, Check } from 'lucide-react';
import { useState } from 'react';
import ReactMarkdown from 'react-markdown';

export default function ResultsDisplay({ result, topic }) {
  const [copied, setCopied] = useState(false);

  if (!result) {
    return null;
  }

  const handleCopy = () => {
    const text = `Topic: ${result.topic}\n\n${result.summary}`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">{result.topic}</h2>
            <p className="text-gray-600">
              Research completed with {result.sources?.length || 0} sources
            </p>
          </div>
          <button
            onClick={handleCopy}
            className="btn-secondary flex items-center gap-2"
          >
            {copied ? (
              <>
                <Check size={20} />
                Copied!
              </>
            ) : (
              <>
                <Copy size={20} />
                Copy
              </>
            )}
          </button>
        </div>
      </div>

      {/* Summary */}
      {result.summary && (
        <div className="card">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Research Summary</h3>
          <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap">
            <ReactMarkdown>{result.summary}</ReactMarkdown>
          </div>
        </div>
      )}

      {/* Entities Found */}
      {result.entities_found && Object.keys(result.entities_found).length > 0 && (
        <div className="card">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Key Entities</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(result.entities_found).map(([category, entities]) => (
              entities.length > 0 && (
                <div key={category}>
                  <h4 className="font-semibold text-gray-700 mb-2 capitalize">
                    {category}
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {entities.map((entity, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-primary bg-opacity-10 text-primary rounded-full text-sm font-medium"
                      >
                        {entity}
                      </span>
                    ))}
                  </div>
                </div>
              )
            ))}
          </div>
        </div>
      )}

      {/* Sources */}
      {result.sources && result.sources.length > 0 && (
        <div className="card">
          <h3 className="text-xl font-bold text-gray-800 mb-4">
            Sources ({result.sources.length})
          </h3>
          <div className="space-y-3">
            {result.sources.map((source, idx) => (
              <div key={idx} className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-grow">
                    <h4 className="font-semibold text-gray-800 break-words">
                      {source.title || `Source ${idx + 1}`}
                    </h4>
                    {source.snippet && (
                      <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                        {source.snippet}
                      </p>
                    )}
                    <p className="text-xs text-gray-500 mt-2 break-all">
                      {source.url}
                    </p>
                  </div>
                  {source.url && (
                    <a
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex-shrink-0 p-2 text-primary hover:bg-primary hover:bg-opacity-10 rounded transition"
                    >
                        <ExternalLink size={20} />
                    </a>
                    )}
                                    </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Research Steps */}
      {result.research_steps && (
        <div className="card">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Research Steps</h3>
          <div className="bg-gray-50 p-4 rounded-lg font-mono text-sm text-gray-700 space-y-1">
            {result.research_steps.map((step) => (
              <div key={step.step}>
                <span className="text-primary font-semibold">[Step {step.step}]</span> {step.description}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}