import { Link } from 'react-router-dom';

function AdminDashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
            <p className="text-gray-600">Manage all aspects of the Nigerian Universities Football League</p>
          </div>
        </div>
      </div>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <Link to="/admin/teams" className="bg-green-600 hover:bg-green-700 text-white rounded-lg shadow-lg p-8 flex flex-col items-center transition-colors">
            <span className="text-3xl mb-2">🏆</span>
            <span className="font-bold text-lg">Manage Teams</span>
          </Link>
          <Link to="/admin/players" className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg shadow-lg p-8 flex flex-col items-center transition-colors">
            <span className="text-3xl mb-2">👤</span>
            <span className="font-bold text-lg">Manage Players</span>
          </Link>
          <Link to="/admin/fixtures" className="bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg shadow-lg p-8 flex flex-col items-center transition-colors">
            <span className="text-3xl mb-2">📅</span>
            <span className="font-bold text-lg">Manage Fixtures</span>
          </Link>
          <Link to="/admin/news" className="bg-red-600 hover:bg-red-700 text-white rounded-lg shadow-lg p-8 flex flex-col items-center transition-colors">
            <span className="text-3xl mb-2">📰</span>
            <span className="font-bold text-lg">Manage News</span>
          </Link>
        </div>
        <div className="mt-12 text-center">
          <Link to="/tables" className="text-green-600 hover:text-green-700 font-semibold text-lg">
            View League Table →
          </Link>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard; 