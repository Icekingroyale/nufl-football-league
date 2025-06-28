import { Link } from 'react-router-dom';

const AdminDashboard = () => {
  const adminCards = [
    {
      title: 'Manage Teams',
      description: 'Add, edit, and delete teams',
      icon: '🏆',
      link: '/admin/teams',
      color: 'bg-green-600 hover:bg-green-700'
    },
    {
      title: 'Manage Players',
      description: 'Add, edit, and delete players',
      icon: '⚽',
      link: '/admin/players',
      color: 'bg-blue-600 hover:bg-blue-700'
    },
    {
      title: 'Manage Fixtures',
      description: 'Schedule and manage matches',
      icon: '📅',
      link: '/admin/fixtures',
      color: 'bg-purple-600 hover:bg-purple-700'
    },
    {
      title: 'Manage News',
      description: 'Add and edit news articles',
      icon: '📰',
      link: '/admin/news',
      color: 'bg-red-600 hover:bg-red-700'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Admin Dashboard</h1>
          <p className="text-xl text-gray-600">Manage your Nigerian Universities Football League</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {adminCards.map((card, index) => (
            <Link
              key={index}
              to={card.link}
              className={`${card.color} rounded-lg shadow-lg p-6 text-white transform transition-all duration-200 hover:scale-105 hover:shadow-xl`}
            >
              <div className="text-4xl mb-4">{card.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{card.title}</h3>
              <p className="text-gray-100">{card.description}</p>
            </Link>
          ))}
        </div>

        <div className="mt-12 bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Quick Stats</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-green-100 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-green-600">0</div>
              <div className="text-sm text-green-800">Teams</div>
            </div>
            <div className="bg-blue-100 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-blue-600">0</div>
              <div className="text-sm text-blue-800">Players</div>
            </div>
            <div className="bg-purple-100 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-purple-600">0</div>
              <div className="text-sm text-purple-800">Fixtures</div>
            </div>
            <div className="bg-red-100 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-red-600">0</div>
              <div className="text-sm text-red-800">News Articles</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard; 