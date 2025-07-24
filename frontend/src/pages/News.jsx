import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { dataAPI } from '../services/api';

function News() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchNews() {
      try {
        const response = await dataAPI.getNews();
        setNews(response.data);
      } catch (error) {
        console.error('Error fetching news:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchNews();
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
            <div key={article.id} className="bg-white rounded-lg shadow-lg p-6 flex flex-col items-center hover:shadow-xl transition-shadow">
              <img src={article.image_url || 'https://via.placeholder.com/400x250?text=No+Image'} alt={article.title} className="w-full h-48 object-cover mb-4 rounded" />
              <h3 className="text-lg font-bold text-gray-900 mb-1">{article.title}</h3>
              <div className="text-sm text-gray-500 mb-2">{article.author} - {article.category}</div>
              <div className="text-xs text-gray-400">{article.created_at}</div>
              <p className="mt-2 text-gray-700">{article.content}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default News; 