import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '@/api/client';

interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
}

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter();
  const user = ref<User | null>(null);
  const isAuthenticated = ref(false);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Initialize auth state from localStorage
  const initAuth = () => {
    const token = localStorage.getItem('access_token');
    if (token) {
      isAuthenticated.value = true;
      // Optionally fetch user data
      fetchUser();
    }
  };

  // Login user
  const login = async (email: string, password: string) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post('/api/v1/auth/login', {
        username: email,
        password,
      });
      
      const { access_token, refresh_token } = response.data;
      
      // Store tokens
      localStorage.setItem('access_token', access_token);
      if (refresh_token) {
        localStorage.setItem('refresh_token', refresh_token);
      }
      
      // Update state
      isAuthenticated.value = true;
      await fetchUser();
      
      // Redirect to dashboard
      router.push('/dashboard');
      return true;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Login failed';
      return false;
    } finally {
      loading.value = false;
    }
  };

  // Register new user
  const register = async (email: string, password: string, fullName: string) => {
    loading.value = true;
    error.value = null;
    try {
      await apiClient.post('/api/v1/auth/register', {
        email,
        password,
        full_name: fullName,
      });
      
      // Auto-login after registration
      return await login(email, password);
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Registration failed';
      return false;
    } finally {
      loading.value = false;
    }
  };

  // Logout user
  const logout = () => {
    // Clear tokens
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    
    // Reset state
    user.value = null;
    isAuthenticated.value = false;
    
    // Redirect to login
    router.push('/login');
  };

  // Fetch current user data
  const fetchUser = async () => {
    try {
      const response = await apiClient.get('/api/v1/users/me');
      user.value = response.data;
      return user.value;
    } catch (err) {
      // If fetching user fails, log out
      logout();
      throw err;
    }
  };

  // Update user profile
  const updateProfile = async (data: { email?: string; full_name?: string; password?: string }) => {
    try {
      const response = await apiClient.put('/api/v1/users/me', data);
      user.value = response.data;
      return true;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update profile';
      return false;
    }
  };

  return {
    user,
    isAuthenticated,
    loading,
    error,
    initAuth,
    login,
    register,
    logout,
    fetchUser,
    updateProfile,
  };
});
