import { useState } from 'react';
import { Search } from 'lucide-react';

export default function SearchForm({ onSubmit, isLoading }) {
  const [topic, setTopic] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (topic.trim()) {
      onSubmit(topic);
      setTopic('');
    }
  };

  return (
    <div className="card mb-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Research Topic</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter research topic (e.g., 'Quantum computing 2024')"
            className="input-field text-lg"
            disabled={isLoading}
            autoFocus
          />
        </div>

        <div className="flex gap-3">
          <button
            type="submit"
            disabled={isLoading || !topic.trim()}
            className="btn-primary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Search size={20} />
            {isLoading ? 'Researching...' : 'Start Research'}
          </button>

          {isLoading && (
            <p className="text-sm text-gray-600 flex items-center">
              This may take 1-2 minutes...
            </p>
          )}
        </div>
      </form>

      <div className="mt-4 text-sm text-gray-600 bg-gray-50 p-3 rounded">
        <p><strong>💡 Tip:</strong> Try topics like "Quantum computing latest developments", "AI trends 2024", "Blockchain adoption in finance"</p>
      </div>
    </div>
  );
}