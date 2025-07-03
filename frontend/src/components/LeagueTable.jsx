import { useState, useEffect } from 'react';
import { dataAPI } from '../services/api';

function LeagueTable() {
  const [table, setTable] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchLeagueTable();
  }, []);

  const fetchLeagueTable = async () => {
    try {
      setLoading(true);
      const response = await dataAPI.getLeagueTable();
      setTable(response.data);
    } catch (error) {
      console.error('Error fetching league table:', error);
      setError('Failed to load league table');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">League Table</h1>
          <p className="mt-2 text-gray-600">Loading league table...</p>
        </div>
        <div className="flex justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">League Table</h1>
          <p className="mt-2 text-gray-600">Current standings and points</p>
        </div>
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">League Table</h1>
        <p className="mt-2 text-gray-600">Current standings and points</p>
      </div>
      <div className="bg-white shadow rounded-lg p-6">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Pos</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Team</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Played</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Points</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">GF</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">GA</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">GD</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {table.map((row, index) => (
              <tr key={index}>
                <td className="px-4 py-2 font-bold text-gray-700">{index + 1}</td>
                <td className="px-4 py-2">{row.team_name}</td>
                <td className="px-4 py-2">{row.matches_played}</td>
                <td className="px-4 py-2 font-bold">{row.points}</td>
                <td className="px-4 py-2">{row.goals_for}</td>
                <td className="px-4 py-2">{row.goals_against}</td>
                <td className="px-4 py-2">{row.goal_difference}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default LeagueTable; 