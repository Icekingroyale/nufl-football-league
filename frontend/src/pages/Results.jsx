import { useState, useEffect } from 'react';
import { dataAPI } from '../services/api';

function Results() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedMatchweek, setSelectedMatchweek] = useState('all');

  useEffect(() => {
    fetchResults();
  }, []);

  const fetchResults = async () => {
    try {
      setLoading(true);
      const response = await dataAPI.getFixtures();
      const completedMatches = response.data.filter(fixture => fixture.status === 'completed');
      setResults(completedMatches);
    } catch (error) {
      console.error('Error fetching results:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredResults = selectedMatchweek === 'all' 
    ? results 
    : results.filter(match => match.id.toString() === selectedMatchweek);

  const matchweeks = [...new Set(results.map(match => match.id))].sort((a, b) => a - b);

  const getMatchResult = (match) => {
    if (match.home_score > match.away_score) {
      return { winner: 'home', result: 'W' };
    } else if (match.away_score > match.home_score) {
      return { winner: 'away', result: 'L' };
    } else {
      return { winner: 'draw', result: 'D' };
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-green-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Results</h1>
            <p className="text-gray-600">All completed matches and scores</p>
          </div>
        </div>
      </div>

      {/* Matchweek Filter */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-wrap gap-2 justify-center">
            <button
              onClick={() => setSelectedMatchweek('all')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                selectedMatchweek === 'all'
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              All Matchweeks
            </button>
            {matchweeks.map((week) => (
              <button
                key={week}
                onClick={() => setSelectedMatchweek(week.toString())}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  selectedMatchweek === week.toString()
                    ? 'bg-green-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Matchweek {week}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Results List */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {filteredResults.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredResults.map((match) => {
              const result = getMatchResult(match);
              return (
                <div key={match.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
                  <div className="p-6">
                    {/* Match Header */}
                    <div className="text-center mb-4">
                      <div className="text-sm text-gray-500 mb-2">Matchweek {match.id}</div>
                      <div className="text-sm text-gray-600">{match.match_date}</div>
                    </div>

                    {/* Teams and Score */}
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-3 flex-1">
                        <img 
                          src={match.home_team_logo || 'https://via.placeholder.com/48x48/22c55e/ffffff?text=H'} 
                          alt={match.home_team}
                          className="w-12 h-12 rounded-full object-cover"
                        />
                        <span className="font-medium">{match.home_team}</span>
                      </div>
                      <div className="mx-4 text-2xl font-bold">
                        {match.home_score !== null ? match.home_score : '-'} - {match.away_score !== null ? match.away_score : '-'}
                      </div>
                      <div className="flex items-center space-x-3 flex-1 justify-end">
                        <span className="font-medium">{match.away_team}</span>
                        <img 
                          src={match.away_team_logo || 'https://via.placeholder.com/48x48/22c55e/ffffff?text=A'} 
                          alt={match.away_team}
                          className="w-12 h-12 rounded-full object-cover"
                        />
                      </div>
                    </div>

                    {/* Match Details */}
                    <div className="text-center text-sm text-gray-500">
                      <div>{match.venue}</div>
                      <div>{match.time}</div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500">No results found for the selected matchweek.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Results;