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
                          src="https://via.placeholder.com/48x48/22c55e/ffffff?text=H" 
                          alt="Home Team"
                          className="w-12 h-12 rounded-full"
                        />
                        <div className="flex-1">
                          <p className="font-semibold text-gray-900">{match.home_team}</p>
                          <p className="text-sm text-gray-500">Home</p>
                        </div>
                      </div>
                      
                      <div className="text-center mx-4">
                        <div className="text-2xl font-bold text-gray-900">
                          {match.home_score} - {match.away_score}
                        </div>
                        <div className={`text-xs font-semibold px-2 py-1 rounded-full ${
                          result.winner === 'home' ? 'bg-green-100 text-green-800' :
                          result.winner === 'away' ? 'bg-red-100 text-red-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {result.winner === 'home' ? 'HOME WIN' :
                           result.winner === 'away' ? 'AWAY WIN' : 'DRAW'}
                        </div>
                      </div>

                      <div className="flex items-center space-x-3 flex-1 justify-end">
                        <div className="flex-1 text-right">
                          <p className="font-semibold text-gray-900">{match.away_team}</p>
                          <p className="text-sm text-gray-500">Away</p>
                        </div>
                        <img 
                          src="https://via.placeholder.com/48x48/3b82f6/ffffff?text=A" 
                          alt="Away Team"
                          className="w-12 h-12 rounded-full"
                        />
                      </div>
                    </div>

                    {/* Match Stats */}
                    <div className="border-t pt-4">
                      <div className="grid grid-cols-3 gap-4 text-center text-sm">
                        <div>
                          <div className="font-semibold text-gray-900">{match.home_score}</div>
                          <div className="text-gray-500">Goals</div>
                        </div>
                        <div>
                          <div className="font-semibold text-gray-900">-</div>
                          <div className="text-gray-500">Assists</div>
                        </div>
                        <div>
                          <div className="font-semibold text-gray-900">{match.away_score}</div>
                          <div className="text-gray-500">Goals</div>
                        </div>
                      </div>
                    </div>

                    {/* Match Highlights */}
                    <div className="mt-4 pt-4 border-t">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-gray-900">Highlights</span>
                        <button className="text-green-600 hover:text-green-700 text-sm font-medium">
                          Watch →
                        </button>
                      </div>
                      <div className="mt-2 bg-gray-100 rounded-lg p-3">
                        <div className="text-xs text-gray-600">
                          {result.winner === 'home' ? 
                            `${match.home_team} secured a ${match.home_score}-${match.away_score} victory over ${match.away_team}` :
                           result.winner === 'away' ? 
                            `${match.away_team} claimed a ${match.away_score}-${match.home_score} win against ${match.home_team}` :
                            `${match.home_team} and ${match.away_team} played to a ${match.home_score}-${match.away_score} draw`
                          }
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="text-gray-500 text-lg">No results found for the selected matchweek.</div>
          </div>
        )}

        {/* Season Summary */}
        <div className="mt-12">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-6">Season Summary</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">{results.length}</div>
                <div className="text-sm text-gray-600">Matches Played</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">
                  {results.reduce((sum, match) => sum + match.home_score + match.away_score, 0)}
                </div>
                <div className="text-sm text-gray-600">Total Goals</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-yellow-600">
                  {results.filter(match => match.home_score === match.away_score).length}
                </div>
                <div className="text-sm text-gray-600">Draws</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600">
                  {results.length > 0 ? 
                    (results.reduce((sum, match) => sum + match.home_score + match.away_score, 0) / results.length).toFixed(1) : 
                    '0.0'
                  }
                </div>
                <div className="text-sm text-gray-600">Avg Goals/Match</div>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Form */}
        <div className="mt-8">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-6">Recent Form</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {results.slice(-6).map((match) => {
                const result = getMatchResult(match);
                return (
                  <div key={match.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <img 
                        src="https://via.placeholder.com/32x32/22c55e/ffffff?text=H" 
                        alt="Home Team"
                        className="w-8 h-8 rounded-full"
                      />
                      <span className="text-sm font-medium">{match.home_team}</span>
                    </div>
                    <div className="text-center">
                      <div className="text-sm font-bold">{match.home_score} - {match.away_score}</div>
                      <div className={`text-xs px-2 py-1 rounded-full ${
                        result.winner === 'home' ? 'bg-green-100 text-green-800' :
                        result.winner === 'away' ? 'bg-red-100 text-red-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {result.result}
                      </div>
                    </div>
                    <div className="flex items-center space-x-3">
                      <span className="text-sm font-medium">{match.away_team}</span>
                      <img 
                        src="https://via.placeholder.com/32x32/3b82f6/ffffff?text=A" 
                        alt="Away Team"
                        className="w-8 h-8 rounded-full"
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Results; 