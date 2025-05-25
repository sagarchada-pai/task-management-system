import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '@/api/client';

export interface Project {
  id: number;
  name: string;
  description: string | null;
  owner_id: number;
  created_at: string;
}

export const useProjectStore = defineStore('projects', () => {
  const projects = ref<Project[]>([]);
  const currentProject = ref<Project | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Fetch all projects
  const fetchProjects = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/api/v1/projects');
      projects.value = response.data;
      return projects.value;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch projects';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Fetch a single project by ID
  const fetchProjectById = async (id: number) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get(`/api/v1/projects/${id}`);
      currentProject.value = response.data;
      return currentProject.value;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch project';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Create a new project
  const createProject = async (projectData: { name: string; description?: string }) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post('/api/v1/projects', projectData);
      projects.value.push(response.data);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create project';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Update an existing project
  const updateProject = async (id: number, projectData: { name?: string; description?: string }) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.put(`/api/v1/projects/${id}`, projectData);
      
      // Update in the projects list
      const index = projects.value.findIndex(p => p.id === id);
      if (index !== -1) {
        projects.value[index] = response.data;
      }
      
      // Update current project if it's the one being updated
      if (currentProject.value?.id === id) {
        currentProject.value = response.data;
      }
      
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update project';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Delete a project
  const deleteProject = async (id: number) => {
    loading.value = true;
    error.value = null;
    try {
      await apiClient.delete(`/api/v1/projects/${id}`);
      
      // Remove from the projects list
      projects.value = projects.value.filter(project => project.id !== id);
      
      // Clear current project if it's the one being deleted
      if (currentProject.value?.id === id) {
        currentProject.value = null;
      }
      
      return true;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete project';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    projects,
    currentProject,
    loading,
    error,
    fetchProjects,
    fetchProjectById,
    createProject,
    updateProject,
    deleteProject,
  };
});
