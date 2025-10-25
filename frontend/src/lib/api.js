import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const trackOrder = async (orderNumber) => {
  try {
    const response = await axios.post(`${API_URL}/orders/search/`, {
      order_number: orderNumber,
    });
    return { data: response.data, error: null };
  } catch (error) {
    return {
      data: null,
      error: error.response?.data?.error || 'Error al buscar el pedido',
    };
  }
};
