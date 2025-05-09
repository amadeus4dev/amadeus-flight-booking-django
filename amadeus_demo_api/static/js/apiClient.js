


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken')


// axios 인스턴스 생성
const apiClient = axios.create({
    baseURL: '/api',  // 기본 baseURL
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
    }
});



// 요청 인터셉터
apiClient.interceptors.request.use(
    config => {
        // 토큰을 가져와서 헤더에 설정
        const accessToken = localStorage.getItem('accessToken');
        const refreshToken = localStorage.getItem('refreshToken');

        // 토큰이 있으면 요청 헤더에 추가한다. 
        if (accessToken) {
            config.headers['Authorization'] = `Bearer ${accessToken}`;
        }
        // Refresh 토큰을 보낼 경우 사용하고자 하는 커스텀 인증 헤더를 사용하면 된다. 
        if (refreshToken) {
            config.headers['x-refresh-token'] = refreshToken;
        }

        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// 응답 인터셉터 (예: 401 에러 처리)
apiClient.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            // 401 에러 처리 (예: 자동 로그아웃)
            console.warn('인증 실패: 다시 로그인하세요.');
            localStorage.removeItem('jwt_token');
            window.location.href = '/login';  // 로그인 페이지로 리다이렉트
        }
        return Promise.reject(error);
    }
);

window.apiClient = apiClient;