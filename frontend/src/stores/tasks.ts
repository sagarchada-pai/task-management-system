import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '@/api/client';

export interface Comment {
  id: number;
  content: string;
  task_id: number;
  user_id: number;
  created_at: string;
  author?: {
    id: number;
    email: string;
    full_name: string;
  };
}

export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: 'todo' | 'in_progress' | 'in_review' | 'done';
  priority: number | null;
  due_date: string | null;
  project_id: number;
  assignee_id: number | null;
  created_by: number;
  created_at: string;
  updated_at: string | null;
  assignee?: {
    id: number;
    email: string;
    full_name: string;
  };
  comments?: Comment[];
}

export const useTaskStore = defineStore('tasks', () => {
  const tasks = ref<Task[]>([]);
  const currentTask = ref<Task | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Fetch tasks with optional filters
  const fetchTasks = async (filters: {
    project_id?: number;
    status?: string;
    assignee_id?: number;
  } = {}) => {
    loading.value = true;
    error.value = null;
    try {
      const params = new URLSearchParams();
      
      if (filters.project_id) params.append('project_id', filters.project_id.toString());
      if (filters.status) params.append('status', filters.status);
      if (filters.assignee_id) params.append('assignee_id', filters.assignee_id.toString());
      
      const response = await apiClient.get(`/api/v1/tasks?${params.toString()}`);
      tasks.value = response.data;
      return tasks.value;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch tasks';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Fetch a single task by ID
  const fetchTaskById = async (id: number) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get(`/api/v1/tasks/${id}`);
      currentTask.value = response.data;
      return currentTask.value;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch task';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Create a new task
  const createTask = async (taskData: {
    title: string;
    description?: string;
    status?: string;
    priority?: number;
    due_date?: string;
    project_id: number;
    assignee_id?: number;
  }) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post('/api/v1/tasks', taskData);
      tasks.value.push(response.data);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create task';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Update an existing task
  const updateTask = async (id: number, taskData: {
    title?: string;
    description?: string | null;
    status?: string;
    priority?: number | null;
    due_date?: string | null;
    project_id?: number;
    assignee_id?: number | null;
  }) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.put(`/api/v1/tasks/${id}`, taskData);
      
      // Update in the tasks list
      const index = tasks.value.findIndex(t => t.id === id);
      if (index !== -1) {
        tasks.value[index] = response.data;
      }
      
      // Update current task if it's the one being updated
      if (currentTask.value?.id === id) {
        currentTask.value = response.data;
      }
      
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update task';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Delete a task
  const deleteTask = async (id: number) => {
    loading.value = true;
    error.value = null;
    try {
      await apiClient.delete(`/api/v1/tasks/${id}`);
      
      // Remove from the tasks list
      tasks.value = tasks.value.filter(task => task.id !== id);
      
      // Clear current task if it's the one being deleted
      if (currentTask.value?.id === id) {
        currentTask.value = null;
      }
      
      return true;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete task';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Add a comment to a task
  const addComment = async (taskId: number, content: string) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post(`/api/v1/tasks/${taskId}/comments`, { content });
      
      // Add comment to current task if it's the one being commented on
      if (currentTask.value?.id === taskId) {
        if (!currentTask.value.comments) {
          currentTask.value.comments = [];
        }
        currentTask.value.comments.push(response.data);
      }
      
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to add comment';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Fetch comments for a task
  const fetchTaskComments = async (taskId: number) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get(`/api/v1/tasks/${taskId}/comments`);
      
      // Update current task comments if it's the one being fetched
      if (currentTask.value?.id === taskId) {
        currentTask.value.comments = response.data;
      }
      
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch comments';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    tasks,
    currentTask,
    loading,
    error,
    fetchTasks,
    fetchTaskById,
    createTask,
    updateTask,
    deleteTask,
    addComment,
    fetchTaskComments,
  };
});
