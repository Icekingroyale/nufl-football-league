import { useState, useEffect } from 'react';

function Clubs() {
  const [clubs, setClubs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Mock clubs data
    setClubs([
      { id: 1, name: 'University of Lagos', crest: 'https://via.placeholder.com/64x64/22c55e/ffffff?text=UL', founded: 1962, stadium: 'Akoka Stadium', city: 'Lagos' },
      { id: 2, name: 'University of Nigeria Nsukka', crest: 'https://via.placeholder.com/64x64/3b82f6/ffffff?text=UNN', founded: 1960, stadium: 'Nsukka Arena', city: 'Nsukka' },
      { id: 3, name: 'Nnamdi Azikiwe University', crest: 'https://via.placeholder.com/64x64/ef4444/ffffff?text=NAU', founded: 1991, stadium: 'Awka Stadium', city: 'Awka' },
      { id: 4, name: 'Ebonyi State University', crest: 'https://via.placeholder.com/64x64/10b981/ffffff?text=EBSU', founded: 1999, stadium: 'Abakaliki Field', city: 'Abakaliki' },
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
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Clubs</h1>
            <p className="text-gray-600">All participating universities in the NUFL</p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {clubs.map(club => (
            <div key={club.id} className="bg-white rounded-lg shadow-lg p-6 flex flex-col items-center hover:shadow-xl transition-shadow">
              <img src={club.crest} alt={club.name} className="w-16 h-16 rounded-full mb-4" />
              <h3 className="text-lg font-bold text-gray-900 mb-1">{club.name}</h3>
              <div className="text-sm text-gray-500 mb-2">Founded: {club.founded}</div>
              <div className="text-sm text-gray-500 mb-2">Stadium: {club.stadium}</div>
              <div className="text-sm text-gray-500">City: {club.city}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Clubs; 