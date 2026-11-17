import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { PageContainer } from '../components/layout/PageContainer';
import { SectionHeader } from '../components/common/SectionHeader';
import { SearchInput } from '../components/common/SearchInput';
import { LoadingState } from '../components/common/LoadingState';
import { Button } from '../components/common/Button';
import apiClient from '../services/api';
import { Search, Book, Lightbulb, AlertCircle } from 'lucide-react';

const KnowledgeBase = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    setIsSearching(true);
    setHasSearched(true);

    try {
      const response = await apiClient.get('/api/v1/safety/retrieve', {
        params: { q: searchQuery },
      });
      setSearchResults(response.data.passages || []);
    } catch (error) {
      console.error('Search failed:', error);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const clearSearch = () => {
    setSearchQuery('');
    setSearchResults([]);
    setHasSearched(false);
  };

  return (
    <PageContainer>
      <SectionHeader
        title="Knowledge Base"
        subtitle="Food safety guidelines, best practices, and AI-powered retrieval"
      />

      {/* Search Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-primary-50 to-sage-50 rounded-lg border border-soft-sage p-8 mb-8"
      >
        <h2 className="text-2xl font-bold text-text-primary mb-4">Search Food Safety Guidelines</h2>
        <p className="text-text-secondary mb-6">
          Ask our RAG system any questions about food safety, handling, and best practices
        </p>

        <div className="flex gap-3 mb-4">
          <SearchInput
            placeholder="Ask about food safety, temperature, storage..."
            value={searchQuery}
            onChange={setSearchQuery}
            onClear={clearSearch}
            disabled={isSearching}
          />
          <Button
            onClick={handleSearch}
            loading={isSearching}
            className="px-6"
          >
            Search
          </Button>
        </div>

        <div className="flex gap-4 flex-wrap">
          <button
            onClick={() => {
              setSearchQuery('Safe food storage temperature');
              setTimeout(handleSearch, 100);
            }}
            className="text-xs px-3 py-1 rounded-full bg-white border border-soft-sage text-primary-600 hover:bg-soft-sage transition-colors"
          >
            Safe storage temperature
          </button>
          <button
            onClick={() => {
              setSearchQuery('How to identify spoiled food');
              setTimeout(handleSearch, 100);
            }}
            className="text-xs px-3 py-1 rounded-full bg-white border border-soft-sage text-primary-600 hover:bg-soft-sage transition-colors"
          >
            Identifying spoiled food
          </button>
          <button
            onClick={() => {
              setSearchQuery('Food handling best practices');
              setTimeout(handleSearch, 100);
            }}
            className="text-xs px-3 py-1 rounded-full bg-white border border-soft-sage text-primary-600 hover:bg-soft-sage transition-colors"
          >
            Handling best practices
          </button>
        </div>
      </motion.div>

      {/* Results Section */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
      >
        {isSearching ? (
          <LoadingState message="Searching knowledge base..." />
        ) : hasSearched && searchResults.length === 0 ? (
          <div className="bg-white rounded-lg border border-soft-sage shadow-sm p-8 text-center">
            <AlertCircle size={40} className="mx-auto mb-3 text-warning" />
            <h3 className="font-semibold text-text-primary mb-2">No results found</h3>
            <p className="text-text-secondary mb-4">
              Try a different search query or check our featured guidelines below
            </p>
          </div>
        ) : hasSearched && searchResults.length > 0 ? (
          <div className="space-y-4">
            <div className="text-sm text-text-muted mb-4">
              Found <span className="font-semibold text-text-primary">{searchResults.length}</span> relevant{' '}
              {searchResults.length === 1 ? 'result' : 'results'}
            </div>
            {searchResults.map((result, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="bg-white rounded-lg border border-soft-sage shadow-sm p-6 hover:shadow-md transition-shadow"
              >
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-10 h-10 bg-soft-sage rounded-lg flex items-center justify-center">
                    <Book size={20} className="text-primary-600" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-text-primary mb-2">
                      {typeof result === 'string' ? 'Safety Guideline' : result.title || 'Food Safety Information'}
                    </h3>
                    <p className="text-text-secondary text-sm mb-3">
                      {typeof result === 'string' ? result : result.content || result.text}
                    </p>
                    <div className="flex gap-2">
                      {typeof result === 'object' && result.score && (
                        <span className="text-xs px-2 py-1 bg-soft-sage text-text-muted rounded">
                          Relevance: {(result.score * 100).toFixed(0)}%
                        </span>
                      )}
                      <span className="text-xs px-2 py-1 bg-soft-sage text-text-muted rounded">
                        Food Safety Database
                      </span>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Featured Guidelines */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white rounded-lg border border-soft-sage shadow-sm p-6"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-soft-sage rounded-lg">
                  <Lightbulb size={20} className="text-primary-600" />
                </div>
                <h3 className="font-semibold text-text-primary">Food Safety Essentials</h3>
              </div>
              <ul className="space-y-2 text-sm text-text-secondary">
                <li className="flex gap-2">
                  <span className="text-primary-600">•</span>
                  <span>Maintain refrigeration at 4°C or below</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-primary-600">•</span>
                  <span>Cook foods to safe internal temperatures</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-primary-600">•</span>
                  <span>Avoid cross-contamination between raw and cooked foods</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-primary-600">•</span>
                  <span>Store food in clean, sealed containers</span>
                </li>
              </ul>
            </motion.div>

            {/* Storage Guidelines */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white rounded-lg border border-soft-sage shadow-sm p-6"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-soft-sage rounded-lg">
                  <AlertCircle size={20} className="text-accent" />
                </div>
                <h3 className="font-semibold text-text-primary">Storage Best Practices</h3>
              </div>
              <ul className="space-y-2 text-sm text-text-secondary">
                <li className="flex gap-2">
                  <span className="text-accent">•</span>
                  <span>Perishables: Use within 2 hours of prep (1 hour if above 32°C)</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-accent">•</span>
                  <span>Refrigerated foods: 3-4 days maximum</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-accent">•</span>
                  <span>Frozen foods: Maintain at -18°C or below</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-accent">•</span>
                  <span>Always label with date and contents</span>
                </li>
              </ul>
            </motion.div>
          </div>
        )}
      </motion.div>
    </PageContainer>
  );
};

export default KnowledgeBase;
