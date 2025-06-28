import { useState, useEffect } from 'react';
import { dataAPI } from '../services/api';

function Tables() {
  const [leagueTable, setLeagueTable] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeagueTable();
  }, []);

  const fetchLeagueTable = async () => {
    try {
      setLoading(true);
      const response = await dataAPI.getLeagueTable();
      setLeagueTable(response.data);
    } catch (error) {
      console.error('Error fetching league table:', error);
    } finally {
      setLoading(false);
    }
  };

  const getPositionColor = (position) => {
    if (position <= 4) return 'bg-green-100 text-green-800'; // Champions League
    if (position <= 6) return 'bg-blue-100 text-blue-800'; // Europa League
    if (position >= leagueTable.length - 2) return 'bg-red-100 text-red-800'; // Relegation
    return 'bg-gray-100 text-gray-800';
  };

  const getPositionLabel = (position) => {
    if (position <= 4) return 'Champions League';
    if (position <= 6) return 'Europa League';
    if (position >= leagueTable.length - 2) return 'Relegation';
    return 'Mid-table';
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
            <h1 className="text-3xl font-bold text-gray-900 mb-2">League Table</h1>
            <p className="text-gray-600">Current standings for the 2024/25 season</p>
          </div>
        </div>
      </div>

      {/* Table Legend */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-wrap gap-4 justify-center text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-green-100 rounded"></div>
              <span className="text-green-800">Champions League</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-blue-100 rounded"></div>
              <span className="text-blue-800">Europa League</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-red-100 rounded"></div>
              <span className="text-red-800">Relegation</span>
            </div>
          </div>
        </div>
      </div>

      {/* League Table */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Pos
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Club
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Pl
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    W
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    D
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    L
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    GF
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    GA
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    GD
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Pts
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Form
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {leagueTable.map((team, index) => (
                  <tr key={team.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${getPositionColor(index + 1)}`}>
                          {index + 1}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <img 
                          src="https://via.placeholder.com/32x32/22c55e/ffffff?text=T" 
                          alt={team.name}
                          className="w-8 h-8 rounded-full mr-3"
                        />
                        <div>
                          <div className="text-sm font-medium text-gray-900">{team.name}</div>
                          <div className="text-xs text-gray-500">{getPositionLabel(index + 1)}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                      {team.matches_played || 0}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                      {team.wins || 0}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                      {team.draws || 0}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                      {team.losses || 0}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                      {team.goals_for || 0}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                      {team.goals_against || 0}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
                      <span className={team.goal_difference > 0 ? 'text-green-600' : team.goal_difference < 0 ? 'text-red-600' : 'text-gray-900'}>
                        {team.goal_difference > 0 ? '+' : ''}{team.goal_difference || 0}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center">
                      <span className="text-lg font-bold text-gray-900">{team.points || 0}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center">
                      <div className="flex space-x-1 justify-center">
                        {['W', 'D', 'L', 'W', 'W'].map((result, i) => (
                          <div
                            key={i}
                            className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                              result === 'W' ? 'bg-green-100 text-green-800' :
                              result === 'D' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-red-100 text-red-800'
                            }`}
                          >
                            {result}
                          </div>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Table Statistics */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">League Leaders</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Points:</span>
                <div className="text-right">
                  <div className="font-semibold">{leagueTable[0]?.name || 'N/A'}</div>
                  <div className="text-xs text-gray-500">{leagueTable[0]?.points || 0} pts</div>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Goals For:</span>
                <div className="text-right">
                  <div className="font-semibold">{leagueTable[0]?.name || 'N/A'}</div>
                  <div className="text-xs text-gray-500">{leagueTable[0]?.goals_for || 0} goals</div>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Goal Difference:</span>
                <div className="text-right">
                  <div className="font-semibold">{leagueTable[0]?.name || 'N/A'}</div>
                  <div className="text-xs text-gray-500">+{leagueTable[0]?.goal_difference || 0}</div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Season Stats</h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Total Teams:</span>
                <span className="font-semibold">{leagueTable.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Total Matches:</span>
                <span className="font-semibold">
                  {leagueTable.reduce((sum, team) => sum + (team.matches_played || 0), 0) / 2}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Total Goals:</span>
                <span className="font-semibold">
                  {leagueTable.reduce((sum, team) => sum + (team.goals_for || 0), 0)}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Avg Goals/Match:</span>
                <span className="font-semibold">
                  {leagueTable.length > 0 ? 
                    (leagueTable.reduce((sum, team) => sum + (team.goals_for || 0), 0) / 
                     (leagueTable.reduce((sum, team) => sum + (team.matches_played || 0), 0) / 2)).toFixed(1) : 
                    '0.0'
                  }
                </span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Qualification Zones</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-green-600">Champions League (1-4):</span>
                <div className="text-right">
                  {leagueTable.slice(0, 4).map((team, i) => (
                    <div key={i} className="text-xs text-gray-600">{i + 1}. {team.name}</div>
                  ))}
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-blue-600">Europa League (5-6):</span>
                <div className="text-right">
                  {leagueTable.slice(4, 6).map((team, i) => (
                    <div key={i} className="text-xs text-gray-600">{i + 5}. {team.name}</div>
                  ))}
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-red-600">Relegation:</span>
                <div className="text-right">
                  {leagueTable.slice(-2).map((team, i) => (
                    <div key={i} className="text-xs text-gray-600">{leagueTable.length - 1 + i}. {team.name}</div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Form</h3>
            <div className="space-y-3">
              {leagueTable.slice(0, 5).map((team, index) => (
                <div key={team.id} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className={`w-4 h-4 rounded-full ${getPositionColor(index + 1)}`}></span>
                    <span className="text-sm font-medium">{team.name}</span>
                  </div>
                  <div className="flex space-x-1">
                    {['W', 'W', 'D', 'L', 'W'].map((result, i) => (
                      <div
                        key={i}
                        className={`w-4 h-4 rounded-full flex items-center justify-center text-xs font-bold ${
                          result === 'W' ? 'bg-green-100 text-green-800' :
                          result === 'D' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}
                      >
                        {result}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Tables; 