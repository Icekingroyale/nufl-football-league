import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { dataAPI } from '../services/api';

function Home() {
  const [upcomingMatches, setUpcomingMatches] = useState([]);
  const [leagueTable, setLeagueTable] = useState([]);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHomeData();
  }, []);

  const fetchHomeData = async () => {
    try {
      setLoading(true);
      
      // Fetch upcoming matches (next 5 fixtures)
      const fixturesResponse = await dataAPI.getFixtures();
      const upcoming = fixturesResponse.data
        .filter(fixture => fixture.status === 'scheduled')
        .slice(0, 5);
      setUpcomingMatches(upcoming);
      
      // Fetch league table
      const tableResponse = await dataAPI.getLeagueTable();
      setLeagueTable(tableResponse.data.slice(0, 10)); // Top 10 teams
      
      // Mock news data (in real app, this would come from API)
      setNews([
        {
          id: 1,
          title: "UNILAG Lions Dominate Opening Weekend",
          excerpt: "The University of Lagos team showed exceptional form in their first match of the season...",
          category: "Match Report",
          date: "2024-01-15",
          image: "https://via.placeholder.com/300x200/22c55e/ffffff?text=UNILAG+vs+UNN"
        },
        {
          id: 2,
          title: "Key Player Injury Update: Ahmed Musa",
          excerpt: "University of Nigeria Nsukka's star striker faces 3-week recovery period...",
          category: "Injury News",
          date: "2024-01-14",
          image: "https://via.placeholder.com/300x200/ef4444/ffffff?text=Injury+Update"
        },
        {
          id: 3,
          title: "Transfer Window: New Signings Announced",
          excerpt: "Several universities have strengthened their squads with new talent...",
          category: "Transfer News",
          date: "2024-01-13",
          image: "https://via.placeholder.com/300x200/3b82f6/ffffff?text=Transfer+News"
        }
      ]);
      
    } catch (error) {
      console.error('Error fetching home data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-green-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-green-600 to-green-800 text-white">
        <div className="absolute inset-0 bg-black opacity-20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Nigerian Universities
              <span className="block text-green-200">Football League</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-green-100 max-w-3xl mx-auto">
              The premier university football competition in Nigeria, bringing together 
              the best student-athletes from universities nationwide.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/fixtures"
                className="bg-white text-green-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                View Fixtures
              </Link>
              <Link
                to="/tables"
                className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-green-600 transition-colors"
              >
                League Table
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Upcoming Matches */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-lg overflow-hidden">
              <div className="bg-green-600 text-white px-6 py-4">
                <h2 className="text-xl font-bold">Upcoming Matches</h2>
              </div>
              <div className="p-6">
                {upcomingMatches.length > 0 ? (
                  <div className="space-y-4">
                    {upcomingMatches.map((match) => (
                      <div key={match.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                        <div className="flex items-center space-x-4">
                          <div className="text-center">
                            <img 
                              src="https://via.placeholder.com/40x40/22c55e/ffffff?text=H" 
                              alt="Home Team"
                              className="w-10 h-10 rounded-full"
                            />
                            <p className="text-xs text-gray-600 mt-1">{match.home_team}</p>
                          </div>
                          <div className="text-center">
                            <span className="text-sm text-gray-500">vs</span>
                          </div>
                          <div className="text-center">
                            <img 
                              src="https://via.placeholder.com/40x40/3b82f6/ffffff?text=A" 
                              alt="Away Team"
                              className="w-10 h-10 rounded-full"
                            />
                            <p className="text-xs text-gray-600 mt-1">{match.away_team}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-semibold text-gray-900">{match.match_date}</p>
                          <p className="text-xs text-gray-500">Matchweek {match.id}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-8">No upcoming matches scheduled</p>
                )}
                <div className="mt-6 text-center">
                  <Link
                    to="/fixtures"
                    className="text-green-600 hover:text-green-700 font-semibold"
                  >
                    View All Fixtures →
                  </Link>
                </div>
              </div>
            </div>
          </div>

          {/* League Table */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-lg overflow-hidden">
              <div className="bg-green-600 text-white px-6 py-4">
                <h2 className="text-xl font-bold">League Table</h2>
              </div>
              <div className="p-6">
                <div className="space-y-2">
                  {leagueTable.map((team, index) => (
                    <div key={team.id} className="flex items-center justify-between p-2 hover:bg-gray-50 rounded">
                      <div className="flex items-center space-x-3">
                        <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                          index < 4 ? 'bg-green-100 text-green-800' : 
                          index < 6 ? 'bg-blue-100 text-blue-800' : 
                          index >= leagueTable.length - 3 ? 'bg-red-100 text-red-800' : 
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {index + 1}
                        </span>
                        <div className="flex items-center space-x-2">
                          <img 
                            src="https://via.placeholder.com/24x24/22c55e/ffffff?text=T" 
                            alt={team.name}
                            className="w-6 h-6 rounded-full"
                          />
                          <span className="text-sm font-medium">{team.name}</span>
                        </div>
                      </div>
                      <div className="text-right">
                        <span className="text-sm font-bold">{team.points}</span>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-4 text-center">
                  <Link
                    to="/tables"
                    className="text-green-600 hover:text-green-700 font-semibold text-sm"
                  >
                    View Full Table →
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* News Section */}
        <div className="mt-12">
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <div className="bg-green-600 text-white px-6 py-4">
              <h2 className="text-xl font-bold">Latest News</h2>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {news.map((article) => (
                  <div key={article.id} className="bg-gray-50 rounded-lg overflow-hidden hover:shadow-md transition-shadow">
                    <img 
                      src={article.image} 
                      alt={article.title}
                      className="w-full h-48 object-cover"
                    />
                    <div className="p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                          article.category === 'Match Report' ? 'bg-green-100 text-green-800' :
                          article.category === 'Injury News' ? 'bg-red-100 text-red-800' :
                          'bg-blue-100 text-blue-800'
                        }`}>
                          {article.category}
                        </span>
                        <span className="text-xs text-gray-500">{article.date}</span>
                      </div>
                      <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">
                        {article.title}
                      </h3>
                      <p className="text-sm text-gray-600 line-clamp-3">
                        {article.excerpt}
                      </p>
                      <Link
                        to={`/news/${article.id}`}
                        className="text-green-600 hover:text-green-700 font-semibold text-sm mt-2 inline-block"
                      >
                        Read More →
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-6 text-center">
                <Link
                  to="/news"
                  className="text-green-600 hover:text-green-700 font-semibold"
                >
                  View All News →
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Preview */}
        <div className="mt-12">
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <div className="bg-green-600 text-white px-6 py-4">
              <h2 className="text-xl font-bold">Season Statistics</h2>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600">380</div>
                  <div className="text-sm text-gray-600">Total Matches</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600">20</div>
                  <div className="text-sm text-gray-600">Teams</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600">950+</div>
                  <div className="text-sm text-gray-600">Goals Scored</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600">500+</div>
                  <div className="text-sm text-gray-600">Players</div>
                </div>
              </div>
              <div className="mt-6 text-center">
                <Link
                  to="/stats"
                  className="text-green-600 hover:text-green-700 font-semibold"
                >
                  View Detailed Statistics →
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home; 