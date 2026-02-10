import axios from 'axios';

export const api = axios.create({
    baseURL: "http://localhost:8000/api/",
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");

    if(token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
})

api.interceptors.response.use(
    (response) => response,

    async (error) => {
        const originalRequest = error.config;

        if(error.response?.status === 401 && !originalRequest._retry){
            originalRequest._retry = true;

            try{
                const refresh = localStorage.getItem("refresh");
                const res = await axios.post(
                    "http://localhost:8000/api/users/refresh/",
                    { refresh }
                );

                const newAccess = res.data.acces;

                localStorage.setItem("token", newAccess);

                originalRequest.headers.Authorization = `Bearer ${newAccess}`;

                return api(originalRequest);
            } catch(refreshError) {
                localStorage.removeItem("token");
                localStorage.removeItem("refresh");

                window.location.href = "/"
            }
        }

        return Promise.reject(error);
    }
);