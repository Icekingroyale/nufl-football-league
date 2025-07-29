import { useState, useEffect } from 'react';
import { dataAPI } from '../services/api';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchTeams() {
      try {
        const response = await dataAPI.getTeams();
        console.log('Teams data:', response.data);
        setTeams(response.data);
      } catch (error) {
        console.error('Error fetching teams:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchTeams();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-green-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Teams</h1>
            <p className="text-gray-600">Meet the teams of the NUFL</p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {teams.map(team => (
            <div key={team.id} className="bg-white rounded-lg shadow-lg p-6 flex flex-col items-center hover:shadow-xl transition-shadow">
              <img src={team.logo_url || 'https://via.placeholder.com/64x64?text=No+Logo'} alt={team.name} className="w-16 h-16 rounded-full mb-4 object-cover" />
              <h3 className="text-lg font-bold text-gray-900 mb-1">{team.name}</h3>
              <div className="text-sm text-gray-500 mb-2">{team.university} - {team.city}</div>
              <div className="text-xs text-gray-400">Founded: {team.founded}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Teams; 