import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { dataAPI } from '../services/api';

function Dashboard() {
  const [stats, setStats] = useState({
    totalTeams: 0,
    totalPlayers: 0,
    totalFixtures: 0,
    completedMatches: 0,
    upcomingMatches: 0
  });

  const [recentFixtures, setRecentFixtures] = useState([]);
  const [topTeams, setTopTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch stats
      const statsResponse = await dataAPI.getStats();
      setStats(statsResponse.data);
      
      // Fetch fixtures (we'll take the first 3 for recent)
      const fixturesResponse = await dataAPI.getFixtures();
      setRecentFixtures(fixturesResponse.data.slice(0, 3));
      
      // Fetch league table (we'll take the first 5 for top teams)
      const leagueResponse = await dataAPI.getLeagueTable();
      const topTeamsData = leagueResponse.data.slice(0, 5).map((team, index) => ({
        name: team.team_name,
        points: team.points,
        position: index + 1
      }));
      setTopTeams(topTeamsData);
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-2 text-gray-600">Loading dashboard data...</p>
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
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-2 text-gray-600">Welcome to the Football League Management System</p>
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
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">Welcome to the Football League Management System</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                  <span className="text-white text-sm font-medium">T</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Total Teams</dt>
                  <dd className="text-lg font-medium text-gray-900">{stats.totalTeams}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                  <span className="text-white text-sm font-medium">P</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Total Players</dt>
                  <dd className="text-lg font-medium text-gray-900">{stats.totalPlayers}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                  <span className="text-white text-sm font-medium">F</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Total Fixtures</dt>
                  <dd className="text-lg font-medium text-gray-900">{stats.totalFixtures}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-purple-500 rounded-md flex items-center justify-center">
                  <span className="text-white text-sm font-medium">C</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Completed</dt>
                  <dd className="text-lg font-medium text-gray-900">{stats.completedMatches}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-red-500 rounded-md flex items-center justify-center">
                  <span className="text-white text-sm font-medium">U</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Upcoming</dt>
                  <dd className="text-lg font-medium text-gray-900">{stats.upcomingMatches}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Fixtures and Top Teams */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Fixtures */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Recent Fixtures
            </h3>
            <div className="space-y-3">
              {recentFixtures.map((fixture) => (
                <div key={fixture.id} className="border border-gray-200 rounded-lg p-3">
                  <div className="flex justify-between items-center">
                    <div className="flex-1">
                      <div className="text-sm font-medium text-gray-900">
                        {fixture.home_team} vs {fixture.away_team}
                      </div>
                      <div className="text-xs text-gray-500">{fixture.match_date}</div>
                    </div>
                    <div className="text-right">
                      {fixture.status === 'completed' ? (
                        <div className="text-sm font-bold text-gray-900">
                          {fixture.home_score} - {fixture.away_score}
                        </div>
                      ) : (
                        <div className="text-sm text-gray-500">Scheduled</div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4">
              <Link
                to="/fixtures"
                className="text-sm text-green-600 hover:text-green-500 font-medium"
              >
                View all fixtures →
              </Link>
            </div>
          </div>
        </div>

        {/* Top Teams */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              League Table (Top 5)
            </h3>
            <div className="space-y-2">
              {topTeams.map((team) => (
                <div key={team.position} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-b-0">
                  <div className="flex items-center">
                    <span className="w-6 h-6 bg-gray-200 rounded-full flex items-center justify-center text-xs font-medium text-gray-700 mr-3">
                      {team.position}
                    </span>
                    <span className="text-sm font-medium text-gray-900">{team.name}</span>
                  </div>
                  <span className="text-sm font-bold text-gray-900">{team.points} pts</span>
                </div>
              ))}
            </div>
            <div className="mt-4">
              <Link
                to="/league-table"
                className="text-sm text-green-600 hover:text-green-500 font-medium"
              >
                View full table →
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Quick Actions
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link
              to="/fixtures"
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                  <span className="text-white text-sm">⚽</span>
                </div>
              </div>
              <div className="ml-4">
                <div className="text-sm font-medium text-gray-900">Manage Fixtures</div>
                <div className="text-sm text-gray-500">Add results & schedule matches</div>
              </div>
            </Link>

            <Link
              to="/teams"
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                  <span className="text-white text-sm">👥</span>
                </div>
              </div>
              <div className="ml-4">
                <div className="text-sm font-medium text-gray-900">View Teams</div>
                <div className="text-sm text-gray-500">Team information & players</div>
              </div>
            </Link>

            <Link
              to="/league-table"
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                  <span className="text-white text-sm">🏆</span>
                </div>
              </div>
              <div className="ml-4">
                <div className="text-sm font-medium text-gray-900">League Table</div>
                <div className="text-sm text-gray-500">Current standings & points</div>
              </div>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard; 