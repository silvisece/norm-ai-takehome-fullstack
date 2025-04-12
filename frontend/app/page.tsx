'use client';

import React, { useState } from 'react';
import HeaderNav from '@/components/HeaderNav';

// Define types for the query response
type Citation = {
  source: string;
  text: string;
};

type QueryResponse = {
  response: string;
  citations: Citation[];
};

export default function Page() {
  const [query, setQuery] = useState('');
  const [data, setData] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:80';

  const handleQueryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };

  const handleQuerySubmit = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setData(null);

    try {
      const response = await fetch(`${API_BASE}/query?query=${encodeURIComponent(query)}`);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Unexpected server error');
      }

      const json = await response.json();
      setData(json);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch response. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') handleQuerySubmit();
  };

  return (
    <div className="flex flex-col h-screen">
      <HeaderNav signOut={() => {}} />

      <main className="flex-1 flex flex-col items-center justify-center px-4">
        <section className="w-full max-w-xl bg-white p-6 rounded-lg shadow-md">
          <input
            type="text"
            value={query}
            onChange={handleQueryChange}
            onKeyDown={handleKeyDown}
            placeholder="Enter your query"
            aria-label="Legal query input"
            className="w-full p-3 mb-4 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-300"
          />
          <button
            onClick={handleQuerySubmit}
            disabled={loading}
            className={`w-full py-2 px-4 rounded text-white font-semibold shadow-md transition ${
              loading ? 'bg-blue-300 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
            }`}
          >
            {loading ? 'Asking...' : 'Ask the Hand'}
          </button>
          {error && <p className="text-red-500 mt-3 text-sm">{error}</p>}
        </section>

        {data && (
          <section className="mt-8 w-full max-w-2xl text-left">
            <h3 className="text-lg font-medium mb-2">🧾 Upon careful consideration, I've concluded that...</h3>
            <div className="bg-gray-50 border-l-4 border-blue-300 p-4 mb-6 rounded whitespace-pre-wrap">
              {data.response}
            </div>

            <h3 className="text-lg font-medium mb-2">📚 Citations</h3>
            <ol className="list-decimal list-inside space-y-3">
              {data.citations.map((citation, index) => (
                <li key={index}>
                  <div className="font-semibold text-gray-800">{citation.source}</div>
                  <div className="italic text-gray-600">
                    {citation.text.replace(/^Source \d+:\s*/, '')}
                  </div>
                </li>
              ))}
            </ol>
          </section>
        )}
      </main>
    </div>
  );
}
