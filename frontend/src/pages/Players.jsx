import { useState, useEffect } from 'react';
import { dataAPI } from '../services/api';

function Players() {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchPlayers() {
      try {
        const response = await dataAPI.getPlayers();
        setPlayers(response.data);
      } catch (error) {
        console.error('Error fetching players:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchPlayers();
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
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Players</h1>
            <p className="text-gray-600">Meet the stars of the NUFL</p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {players.map(player => (
            <div key={player.id} className="bg-white rounded-lg shadow-lg p-6 flex flex-col items-center hover:shadow-xl transition-shadow">
              <img src={player.photo_url || 'https://via.placeholder.com/64x64?text=No+Image'} alt={player.name} className="w-16 h-16 rounded-full mb-4 object-cover" />
              <h3 className="text-lg font-bold text-gray-900 mb-1">{player.name}</h3>
              <div className="text-sm text-gray-500 mb-2">{player.position} - {player.team_name || player.team}</div>
              <div className="flex space-x-4 mt-2">
                <div className="text-center">
                  <div className="text-green-600 font-bold text-lg">{player.goals ?? '-'}</div>
                  <div className="text-xs text-gray-500">Goals</div>
                </div>
                <div className="text-center">
                  <div className="text-blue-600 font-bold text-lg">{player.assists ?? '-'}</div>
                  <div className="text-xs text-gray-500">Assists</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Players; 