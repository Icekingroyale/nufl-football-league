import { useState, useEffect } from 'react';
import { dataAPI, actionsAPI } from '../services/api';

function Fixtures({ isAuthenticated = false }) {
  const [showAddForm, setShowAddForm] = useState(false);
  const [formData, setFormData] = useState({
    homeTeam: '',
    awayTeam: '',
    homeScore: '',
    awayScore: '',
    matchDate: ''
  });

  const [fixtures, setFixtures] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchFixturesAndTeams();
  }, []);

  const fetchFixturesAndTeams = async () => {
    try {
      setLoading(true);
      
      // Fetch fixtures
      const fixturesResponse = await dataAPI.getFixtures();
      setFixtures(fixturesResponse.data);
      
      // Fetch teams for the form
      const teamsResponse = await dataAPI.getTeams();
      setTeams(teamsResponse.data.map(team => team.name));
      
    } catch (error) {
      console.error('Error fetching fixtures and teams:', error);
      setError('Failed to load fixtures and teams');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.homeTeam || !formData.awayTeam || !formData.matchDate) {
      alert('Please fill in all required fields');
      return;
    }

    if (formData.homeTeam === formData.awayTeam) {
      alert('Home and away teams cannot be the same');
      return;
    }

    try {
      setSubmitting(true);
      
      const fixtureData = {
        home_team: formData.homeTeam,
        away_team: formData.awayTeam,
        match_date: formData.matchDate
      };

      await actionsAPI.addFixture(fixtureData);
      
      // Reset form and refresh data
      setFormData({
        homeTeam: '',
        awayTeam: '',
        homeScore: '',
        awayScore: '',
        matchDate: ''
      });
      setShowAddForm(false);
      
      // Refresh fixtures list
      await fetchFixturesAndTeams();
      
      alert('Fixture added successfully!');
    } catch (error) {
      console.error('Error adding fixture:', error);
      alert('Failed to add fixture. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const getStatusBadge = (status) => {
    if (status === 'completed') {
      return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Completed</span>;
    } else {
      return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">Scheduled</span>;
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Fixtures</h1>
          <p className="mt-2 text-gray-600">Loading fixtures...</p>
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
          <h1 className="text-3xl font-bold text-gray-900">Fixtures</h1>
          <p className="mt-2 text-gray-600">Manage match fixtures and results</p>
        </div>
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Fixtures</h1>
          <p className="mt-2 text-gray-600">Manage match fixtures and results</p>
        </div>
        {isAuthenticated && (
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
          >
            {showAddForm ? 'Cancel' : 'Add New Fixture'}
          </button>
        )}
      </div>

      {showAddForm && (
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Add New Fixture</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="homeTeam" className="block text-sm font-medium text-gray-700">
                  Home Team *
                </label>
                <select
                  id="homeTeam"
                  name="homeTeam"
                  value={formData.homeTeam}
                  onChange={handleInputChange}
                  required
                  disabled={submitting}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md disabled:opacity-50"
                >
                  <option value="">Select Home Team</option>
                  {teams.map((team) => (
                    <option key={team} value={team}>{team}</option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="awayTeam" className="block text-sm font-medium text-gray-700">
                  Away Team *
                </label>
                <select
                  id="awayTeam"
                  name="awayTeam"
                  value={formData.awayTeam}
                  onChange={handleInputChange}
                  required
                  disabled={submitting}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md disabled:opacity-50"
                >
                  <option value="">Select Away Team</option>
                  {teams.map((team) => (
                    <option key={team} value={team}>{team}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label htmlFor="matchDate" className="block text-sm font-medium text-gray-700">
                  Match Date *
                </label>
                <input
                  type="date"
                  id="matchDate"
                  name="matchDate"
                  value={formData.matchDate}
                  onChange={handleInputChange}
                  required
                  disabled={submitting}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-sm disabled:opacity-50"
                />
              </div>

              <div>
                <label htmlFor="homeScore" className="block text-sm font-medium text-gray-700">
                  Home Score
                </label>
                <input
                  type="number"
                  id="homeScore"
                  name="homeScore"
                  value={formData.homeScore}
                  onChange={handleInputChange}
                  min="0"
                  disabled={submitting}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-sm disabled:opacity-50"
                  placeholder="Optional"
                />
              </div>

              <div>
                <label htmlFor="awayScore" className="block text-sm font-medium text-gray-700">
                  Away Score
                </label>
                <input
                  type="number"
                  id="awayScore"
                  name="awayScore"
                  value={formData.awayScore}
                  onChange={handleInputChange}
                  min="0"
                  disabled={submitting}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-sm disabled:opacity-50"
                  placeholder="Optional"
                />
              </div>
            </div>

            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => setShowAddForm(false)}
                disabled={submitting}
                className="bg-gray-300 hover:bg-gray-400 text-gray-700 px-4 py-2 rounded-md text-sm font-medium transition-colors disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors disabled:opacity-50"
              >
                {submitting ? 'Adding...' : 'Add Fixture'}
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            All Fixtures
          </h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Match
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  {isAuthenticated && (
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  )}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {fixtures.map((fixture) => (
                  <tr key={fixture.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {fixture.home_team} vs {fixture.away_team}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {fixture.match_date}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {fixture.status === 'completed' ? (
                        <span className="text-sm font-bold text-gray-900">
                          {fixture.home_score} - {fixture.away_score}
                        </span>
                      ) : (
                        <span className="text-sm text-gray-500">TBD</span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {getStatusBadge(fixture.status)}
                    </td>
                    {isAuthenticated && (
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        {fixture.status === 'scheduled' ? (
                          <button className="text-green-600 hover:text-green-900">
                            Update Result
                          </button>
                        ) : (
                          <button className="text-blue-600 hover:text-blue-900">
                            Edit
                          </button>
                        )}
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Fixtures; 