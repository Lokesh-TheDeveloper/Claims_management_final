import axios from "axios";

const API_URL = "https://claims-management-final-1.onrender.com/";

export const createClaim = (claimData) => {
  return axios.post(API_URL, claimData);
};

export const getClaim = (claimId) => {
  return axios.get(`${API_URL}/${claimId}`);
};

export const updateClaim = (claimId, status) => {
  return axios.put(`${API_URL}/${claimId}`, { status });
};

export const deleteClaim = (claimId) => {
  return axios.delete(`${API_URL}/${claimId}`);
};
