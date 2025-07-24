
import { WorkflowFormData, ApiResponse, Workflow } from './types';

const API_BASE_URL = '';
const API_KEY = 'xplaincrypto-api-key';

export class ApiClient {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': API_KEY,
          ...options.headers,
        },
        ...options,
      });

      const result = await response.json();
      
      if (!response.ok) {
        return {
          success: false,
          error: result.error || result.detail || `HTTP ${response.status}`,
        };
      }

      return result;
    } catch (error) {
      console.error('API Request failed:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }

  async startWorkflow(data: WorkflowFormData): Promise<ApiResponse<{ workflowId: string }>> {
    const backendData = {
      repository_url: data.githubUrl,
      task_prompt: data.mode === 'prompt-driven' ? data.prompt : null,
    };

    const response = await this.request<any>('/api/workflow', {
      method: 'POST',
      body: JSON.stringify(backendData),
    });

    if (response.success) {
      // Extract workflow ID from direct backend response
      const workflowId = response.workflow_id || response.id || 'unknown';
      return {
        success: true,
        data: { workflowId },
      };
    }

    return response;
  }

  async getWorkflowStatus(workflowId: string): Promise<ApiResponse<Workflow>> {
    const response = await this.request<any>(`/api/workflows/${workflowId}`);
    
    if (response.success && response.data) {
      // Transform backend response to frontend format
      const workflow: Workflow = {
        id: workflowId,
        githubUrl: response.data.repository_url || '',
        status: response.data.status || 'unknown',
        progress: response.data.progress || 0,
        createdAt: new Date(response.data.created_at || Date.now()),
        updatedAt: new Date(response.data.updated_at || Date.now()),
        userId: '',
        prompt: response.data.task_prompt,
        error: response.data.error,
      };
      
      return {
        success: true,
        data: workflow,
      };
    }

    return response;
  }

  async listWorkflows(): Promise<ApiResponse<Workflow[]>> {
    return this.request<Workflow[]>('/api/workflows');
  }

  createWebSocketConnection(workflowId: string): WebSocket | null {
    try {
      // For now, return null as WebSocket isn't implemented yet
      return null;
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
      return null;
    }
  }
}

export const apiClient = new ApiClient();
