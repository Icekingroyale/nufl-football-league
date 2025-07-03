import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function News() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Mock news data
    setNews([
      {
        id: 1,
        title: "UNILAG Lions Dominate Opening Weekend",
        excerpt: "The University of Lagos team showed exceptional form in their first match of the season...",
        category: "Match Report",
        date: "2024-01-15",
        image: "https://via.placeholder.com/400x250/22c55e/ffffff?text=UNILAG+vs+UNN"
      },
      {
        id: 2,
        title: "Key Player Injury Update: Ahmed Musa",
        excerpt: "University of Nigeria Nsukka's star striker faces 3-week recovery period...",
        category: "Injury News",
        date: "2024-01-14",
        image: "https://via.placeholder.com/400x250/ef4444/ffffff?text=Injury+Update"
      },
      {
        id: 3,
        title: "Transfer Window: New Signings Announced",
        excerpt: "Several universities have strengthened their squads with new talent...",
        category: "Transfer News",
        date: "2024-01-13",
        image: "https://via.placeholder.com/400x250/3b82f6/ffffff?text=Transfer+News"
      },
      {
        id: 4,
        title: "NUFL Launches New Season with Exciting Fixtures",
        excerpt: "The Nigerian Universities Football League is back with a bang as the new season kicks off...",
        category: "General News",
        date: "2024-01-12",
        image: "https://via.placeholder.com/400x250/10b981/ffffff?text=NUFL+News"
      }
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
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Latest News</h1>
            <p className="text-gray-600">Injury news, match reports, transfers, and more</p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {news.map(article => (
            <div key={article.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
              <img src={article.image} alt={article.title} className="w-full h-48 object-cover" />
              <div className="p-6">
                <div className="flex items-center justify-between mb-2">
                  <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                    article.category === 'Match Report' ? 'bg-green-100 text-green-800' :
                    article.category === 'Injury News' ? 'bg-red-100 text-red-800' :
                    article.category === 'Transfer News' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
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
      </div>
    </div>
  );
}

export default News; 