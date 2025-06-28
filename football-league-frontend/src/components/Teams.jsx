import { useState, useEffect } from 'react';
import { dataAPI } from '../services/api';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTeams();
  }, []);

  const fetchTeams = async () => {
    try {
      setLoading(true);
      const response = await dataAPI.getTeams();
      setTeams(response.data);
    } catch (error) {
      console.error('Error fetching teams:', error);
      setError('Failed to load teams');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Teams</h1>
          <p className="mt-2 text-gray-600">Loading teams...</p>
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
          <h1 className="text-3xl font-bold text-gray-900">Teams</h1>
          <p className="mt-2 text-gray-600">View team information and players</p>
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
        <h1 className="text-3xl font-bold text-gray-900">Teams</h1>
        <p className="mt-2 text-gray-600">View team information and players</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {teams.map((team) => (
          <div key={team.id} className="bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-bold text-green-700 mb-2">{team.name}</h2>
            <div className="text-sm text-gray-600 mb-1">City: {team.city}</div>
            <div className="text-sm text-gray-600 mb-1">Founded: {team.founded_year}</div>
            <div className="mt-3">
              <div className="font-semibold text-gray-800 mb-1">Players: {team.player_count}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Teams; 