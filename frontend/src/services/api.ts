import axios from 'axios';
import type { UploadResponse, AuditReport, AIAnalysisResponse } from '../types';

const API_BASE_URL = '/api';

export const api = {
  uploadDataset: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post<UploadResponse>(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  analyzeDataset: async (datasetId: string): Promise<AuditReport> => {
    const response = await axios.post<AuditReport>(`${API_BASE_URL}/analyze/${datasetId}`);
    return response.data;
  },

  getAuditReport: async (datasetId: string): Promise<AuditReport> => {
    const response = await axios.get<AuditReport>(`${API_BASE_URL}/report/${datasetId}`);
    return response.data;
  },

  analyzeAI: async (datasetId: string): Promise<AIAnalysisResponse> => {
    const response = await axios.post<AIAnalysisResponse>(`${API_BASE_URL}/analyze-ai/${datasetId}`);
    return response.data;
  },

  getHistory: async (): Promise<any[]> => {
    const response = await axios.get<any[]>(`${API_BASE_URL}/history`);
    return response.data;
  },

  getPdfReportDownloadUrl: (datasetId: string): string => {
    return `${API_BASE_URL}/dataset/${datasetId}/export-pdf`;
  }
};
