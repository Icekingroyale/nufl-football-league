import { useState, useEffect } from 'react';

function Stats() {
  const [topScorers, setTopScorers] = useState([]);
  const [topAssists, setTopAssists] = useState([]);
  const [cleanSheets, setCleanSheets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Mock data for now
    setTopScorers([
      { id: 1, name: 'Ahmed Musa', team: 'University of Nigeria Nsukka', goals: 12, image: 'https://via.placeholder.com/48x48/22c55e/ffffff?text=AM' },
      { id: 2, name: 'John Obi', team: 'University of Lagos', goals: 10, image: 'https://via.placeholder.com/48x48/3b82f6/ffffff?text=JO' },
      { id: 3, name: 'Chinedu Eze', team: 'Nnamdi Azikiwe University', goals: 9, image: 'https://via.placeholder.com/48x48/ef4444/ffffff?text=CE' },
    ]);
    setTopAssists([
      { id: 1, name: 'Samuel Okoro', team: 'Ebonyi State University', assists: 8, image: 'https://via.placeholder.com/48x48/22c55e/ffffff?text=SO' },
      { id: 2, name: 'Ifeanyi Ubah', team: 'University of Lagos', assists: 7, image: 'https://via.placeholder.com/48x48/3b82f6/ffffff?text=IU' },
      { id: 3, name: 'Bola Akin', team: 'University of Nigeria Nsukka', assists: 6, image: 'https://via.placeholder.com/48x48/ef4444/ffffff?text=BA' },
    ]);
    setCleanSheets([
      { id: 1, name: 'Peter Obi', team: 'University of Lagos', sheets: 6, image: 'https://via.placeholder.com/48x48/22c55e/ffffff?text=PO' },
      { id: 2, name: 'Emeka Okafor', team: 'Nnamdi Azikiwe University', sheets: 5, image: 'https://via.placeholder.com/48x48/3b82f6/ffffff?text=EO' },
      { id: 3, name: 'Chuka Nwosu', team: 'Ebonyi State University', sheets: 4, image: 'https://via.placeholder.com/48x48/ef4444/ffffff?text=CN' },
    ]);
    setLoading(false);
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
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Season Statistics</h1>
            <p className="text-gray-600">Top performers and team stats for the 2024/25 season</p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Top Scorers */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-bold text-green-600 mb-4">Top Scorers</h2>
          <ul className="space-y-4">
            {topScorers.map(player => (
              <li key={player.id} className="flex items-center space-x-4">
                <img src={player.image} alt={player.name} className="w-12 h-12 rounded-full" />
                <div className="flex-1">
                  <div className="font-semibold text-gray-900">{player.name}</div>
                  <div className="text-sm text-gray-500">{player.team}</div>
                </div>
                <div className="text-lg font-bold text-green-600">{player.goals}</div>
              </li>
            ))}
          </ul>
        </div>
        {/* Top Assists */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-bold text-blue-600 mb-4">Top Assists</h2>
          <ul className="space-y-4">
            {topAssists.map(player => (
              <li key={player.id} className="flex items-center space-x-4">
                <img src={player.image} alt={player.name} className="w-12 h-12 rounded-full" />
                <div className="flex-1">
                  <div className="font-semibold text-gray-900">{player.name}</div>
                  <div className="text-sm text-gray-500">{player.team}</div>
                </div>
                <div className="text-lg font-bold text-blue-600">{player.assists}</div>
              </li>
            ))}
          </ul>
        </div>
        {/* Clean Sheets */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-bold text-purple-600 mb-4">Clean Sheets</h2>
          <ul className="space-y-4">
            {cleanSheets.map(player => (
              <li key={player.id} className="flex items-center space-x-4">
                <img src={player.image} alt={player.name} className="w-12 h-12 rounded-full" />
                <div className="flex-1">
                  <div className="font-semibold text-gray-900">{player.name}</div>
                  <div className="text-sm text-gray-500">{player.team}</div>
                </div>
                <div className="text-lg font-bold text-purple-600">{player.sheets}</div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Stats; 