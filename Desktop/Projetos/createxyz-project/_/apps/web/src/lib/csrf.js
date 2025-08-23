import { useState, useEffect } from 'react';

// Geração de token CSRF
export const generateCSRFToken = () => {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
};

// Validação de token CSRF
export const validateCSRFToken = (token, sessionToken) => {
  return token && sessionToken && token === sessionToken;
};

// Hook para gerenciar CSRF token
export const useCSRFToken = () => {
  const [token, setToken] = useState(null);

  useEffect(() => {
    let storedToken = sessionStorage.getItem('csrf_token');
    if (!storedToken) {
      storedToken = generateCSRFToken();
      sessionStorage.setItem('csrf_token', storedToken);
    }
    setToken(storedToken);
  }, []);

  return token;
};