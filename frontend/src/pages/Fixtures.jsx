import { useState, useEffect } from 'react';
import { dataAPI } from '../services/api';

function Fixtures() {
  const [fixtures, setFixtures] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, upcoming, completed

  useEffect(() => {
    fetchFixtures();
  }, []);

  const fetchFixtures = async () => {
    try {
      setLoading(true);
      const response = await dataAPI.getFixtures();
      setFixtures(response.data);
    } catch (error) {
      console.error('Error fetching fixtures:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredFixtures = fixtures.filter(fixture => {
    if (filter === 'upcoming') return fixture.status === 'scheduled';
    if (filter === 'completed') return fixture.status === 'completed';
    return true;
  });

  const getStatusBadge = (status) => {
    if (status === 'completed') {
      return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Completed</span>;
    } else {
      return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">Scheduled</span>;
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
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Fixtures</h1>
            <p className="text-gray-600">All matches for the 2024/25 season</p>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-wrap gap-2 justify-center">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                filter === 'all'
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              All Matches
            </button>
            <button
              onClick={() => setFilter('upcoming')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                filter === 'upcoming'
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Upcoming
            </button>
            <button
              onClick={() => setFilter('completed')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                filter === 'completed'
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Completed
            </button>
          </div>
        </div>
      </div>

      {/* Fixtures List */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Match
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Matchweek
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredFixtures.length > 0 ? (
                  filteredFixtures.map((fixture) => (
                    <tr key={fixture.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center space-x-4">
                          <div className="flex items-center space-x-3">
                            <div className="text-center">
                              <img 
                                src="https://via.placeholder.com/32x32/22c55e/ffffff?text=H" 
                                alt="Home Team"
                                className="w-8 h-8 rounded-full"
                              />
                              <p className="text-xs text-gray-600 mt-1 max-w-20 truncate">{fixture.home_team}</p>
                            </div>
                            <div className="text-center">
                              <span className="text-sm font-medium text-gray-900">vs</span>
                            </div>
                            <div className="text-center">
                              <img 
                                src="https://via.placeholder.com/32x32/3b82f6/ffffff?text=A" 
                                alt="Away Team"
                                className="w-8 h-8 rounded-full"
                              />
                              <p className="text-xs text-gray-600 mt-1 max-w-20 truncate">{fixture.away_team}</p>
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {fixture.match_date}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {fixture.status === 'completed' ? (
                          <span className="text-lg font-bold text-gray-900">
                            {fixture.home_score} - {fixture.away_score}
                          </span>
                        ) : (
                          <span className="text-sm text-gray-500">TBD</span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {getStatusBadge(fixture.status)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {fixture.id}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" className="px-6 py-12 text-center text-gray-500">
                      No fixtures found for the selected filter.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Season Info */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Season Overview</h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Total Matches:</span>
                <span className="font-semibold">{fixtures.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Completed:</span>
                <span className="font-semibold text-green-600">
                  {fixtures.filter(f => f.status === 'completed').length}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Remaining:</span>
                <span className="font-semibold text-yellow-600">
                  {fixtures.filter(f => f.status === 'scheduled').length}
                </span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Next Match</h3>
            {fixtures.filter(f => f.status === 'scheduled').length > 0 ? (
              <div className="text-center">
                <div className="flex items-center justify-center space-x-4 mb-3">
                  <div className="text-center">
                    <img 
                      src="https://via.placeholder.com/40x40/22c55e/ffffff?text=H" 
                      alt="Home Team"
                      className="w-10 h-10 rounded-full mx-auto"
                    />
                    <p className="text-sm text-gray-600 mt-1">
                      {fixtures.filter(f => f.status === 'scheduled')[0].home_team}
                    </p>
                  </div>
                  <span className="text-lg font-bold">vs</span>
                  <div className="text-center">
                    <img 
                      src="https://via.placeholder.com/40x40/3b82f6/ffffff?text=A" 
                      alt="Away Team"
                      className="w-10 h-10 rounded-full mx-auto"
                    />
                    <p className="text-sm text-gray-600 mt-1">
                      {fixtures.filter(f => f.status === 'scheduled')[0].away_team}
                    </p>
                  </div>
                </div>
                <p className="text-sm text-gray-600">
                  {fixtures.filter(f => f.status === 'scheduled')[0].match_date}
                </p>
              </div>
            ) : (
              <p className="text-gray-500 text-center">No upcoming matches</p>
            )}
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Total Goals:</span>
                <span className="font-semibold">
                  {fixtures
                    .filter(f => f.status === 'completed')
                    .reduce((sum, f) => sum + (f.home_score || 0) + (f.away_score || 0), 0)}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Avg Goals/Match:</span>
                <span className="font-semibold">
                  {fixtures.filter(f => f.status === 'completed').length > 0 
                    ? (fixtures
                        .filter(f => f.status === 'completed')
                        .reduce((sum, f) => sum + (f.home_score || 0) + (f.away_score || 0), 0) / 
                       fixtures.filter(f => f.status === 'completed').length).toFixed(1)
                    : '0.0'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Draws:</span>
                <span className="font-semibold">
                  {fixtures.filter(f => f.status === 'completed' && f.home_score === f.away_score).length}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Fixtures; 