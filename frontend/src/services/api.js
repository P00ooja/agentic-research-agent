import axios from 'axios';

// Create axios instance
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service methods
export const researchAPI = {
  /**
   * Start a new research
   * @param {string} topic - Research topic
   * @returns {Promise<{research_id: string, status: string}>}
   */
  startResearch: async (topic) => {
    try {
      const response = await apiClient.post('/research', { topic });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to start research');
    }
  },

  /**
   * Get research status and results
   * @param {string} researchId - Research ID
   * @returns {Promise<{status: string, progress: number, result: object}>}
   */
  getResearchStatus: async (researchId) => {
    try {
      const response = await apiClient.get(`/research/${researchId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get research status');
    }
  },

  /**
   * Get research history
   * @returns {Promise<{history: Array}>}
   */
  getSearchHistory: async () => {
    try {
      const response = await apiClient.get('/search-history');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get search history');
    }
  },
};

export default apiClient;
