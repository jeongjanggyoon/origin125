// 전역 상태 관리
const state = {
    students: Array.from({ length: 20 }, (_, i) => ({
        number: i + 1,
        emotion: null,
        emotionType: null,
        emotionText: ''
    })),
    currentStudent: null,
    emotionHistory: [],
    charts: {}
};

// 감정 타입별 이름 매핑
const emotionNames = {
    '😊': '행복해요',
    '😄': '기뻐요',
    '🥰': '사랑해요',
    '😎': '멋져요',
    '🤗': '포근해요',
    '😐': '그냥 그래요',
    '🤔': '고민돼요',
    '😑': '무표정',
    '😶': '조용해요',
    '😢': '슬퍼요',
    '😭': '많이 슬퍼요',
    '😠': '화나요',
    '😰': '불안해요',
    '😫': '힘들어요',
    '🤒': '아파요'
};

// 칭찬 메시지 배열
const praiseMessages = [
    '오늘도 최고로 멋진 우리 반! 🌟',
    '여러분 모두 별처럼 빛나요! ✨',
    '함께해서 행복한 우리 반! 💖',
    '너희들은 선생님의 자랑이야! 🏆',
    '오늘도 열심히 한 우리 반 파이팅! 💪',
    '친구들과 잘 지내는 너희가 자랑스러워! 🤗',
    '웃는 얼굴이 가득한 교실! 😊',
    '서로 도와주는 착한 친구들! 🙌',
    '창의적이고 똑똑한 우리 반! 🧠',
    '감정을 잘 표현하는 용감한 친구들! 🦁',
    '매일매일 성장하는 우리! 🌱',
    '서로를 배려하는 따뜻한 마음! ❤️',
    '즐겁게 배우는 멋진 학생들! 📚',
    '긍정 에너지 넘치는 우리 반! ⚡',
    '모두가 소중한 보물이에요! 💎'
];

// 초기화
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    loadSavedData();
    setupEventListeners();
    updateDateTime();
    updateNoiseMeter();
    generateStudentCards();
    updateDashboard();
    updateEmotionWorld();
    updateTimelineChart();
    updateWeeklyChart();
});

// 앱 초기화
function initializeApp() {
    // 날짜/시간 업데이트 (1초마다)
    setInterval(updateDateTime, 1000);

    // 소음 측정기 업데이트 (0.5초마다)
    setInterval(updateNoiseMeter, 500);

    // 날씨 업데이트 (10분마다)
    updateWeather();
    setInterval(updateWeather, 600000);
}

// 날짜/시간 업데이트
function updateDateTime() {
    const now = new Date();

    // 날짜
    const dateStr = now.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
    });
    document.getElementById('date').textContent = dateStr;

    // 시간
    const timeStr = now.toLocaleTimeString('ko-KR', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    document.getElementById('time').textContent = timeStr;
}

// 날씨 업데이트 (기본값 또는 실제 API 사용 가능)
function updateWeather() {
    // 간단한 날씨 시뮬레이션 (실제로는 API 사용 가능)
    const weatherOptions = [
        { icon: '☀️', text: '맑음', temp: 20 },
        { icon: '⛅', text: '구름 조금', temp: 18 },
        { icon: '☁️', text: '흐림', temp: 15 },
        { icon: '🌧️', text: '비', temp: 12 }
    ];

    // 로컬 스토리지에서 오늘 날씨 가져오기 (하루에 한 번만 변경)
    const today = new Date().toDateString();
    let savedWeather = localStorage.getItem('todayWeather');
    let savedDate = localStorage.getItem('weatherDate');

    if (savedDate !== today || !savedWeather) {
        const randomWeather = weatherOptions[Math.floor(Math.random() * weatherOptions.length)];
        savedWeather = JSON.stringify(randomWeather);
        localStorage.setItem('todayWeather', savedWeather);
        localStorage.setItem('weatherDate', today);
    }

    const weather = JSON.parse(savedWeather);
    document.getElementById('weather').innerHTML = `${weather.icon} ${weather.text} ${weather.temp}°C`;
}

// 소음 측정기 (마이크 권한 필요, 시뮬레이션 모드 포함)
let audioContext;
let microphone;
let analyser;
let dataArray;

async function updateNoiseMeter() {
    try {
        if (!audioContext) {
            // 마이크 접근 시도
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            microphone = audioContext.createMediaStreamSource(stream);
            analyser = audioContext.createAnalyser();
            analyser.fftSize = 256;
            microphone.connect(analyser);
            dataArray = new Uint8Array(analyser.frequencyBinCount);
        }

        analyser.getByteFrequencyData(dataArray);
        const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
        const decibels = Math.round(average);

        document.getElementById('noise-level').textContent = decibels;
        document.getElementById('noise-fill').style.width = `${Math.min(decibels, 100)}%`;
    } catch (error) {
        // 마이크 권한이 없을 경우 시뮬레이션
        const simulatedNoise = Math.floor(Math.random() * 40) + 30; // 30-70 dB
        document.getElementById('noise-level').textContent = simulatedNoise;
        document.getElementById('noise-fill').style.width = `${simulatedNoise}%`;
    }
}

// 이벤트 리스너 설정
function setupEventListeners() {
    // 탭 버튼
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            switchTab(tabId);
        });
    });

    // 감정 선택 버튼
    document.querySelectorAll('.emotion-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const emotion = btn.getAttribute('data-emotion');
            const emotionType = btn.getAttribute('data-type');
            selectEmotion(emotion, emotionType);
        });
    });
}

// 탭 전환
function switchTab(tabId) {
    // 모든 탭 버튼과 패널 비활성화
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));

    // 선택된 탭 활성화
    document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');
    document.getElementById(tabId).classList.add('active');

    // 탭별 업데이트
    if (tabId === 'tab2') {
        updateDashboard();
    } else if (tabId === 'tab3') {
        updateEmotionWorld();
    } else if (tabId === 'tab4') {
        updateTimelineChart();
        updateWeeklyChart();
    }
}

// 학생 카드 생성 (탭1)
function generateStudentCards() {
    const container = document.querySelector('.students-grid');
    container.innerHTML = '';

    state.students.forEach(student => {
        const card = document.createElement('div');
        card.className = `student-card ${student.emotion ? 'has-emotion' : ''}`;
        card.onclick = () => openEmotionModal(student.number);

        card.innerHTML = `
            <div class="student-number">${student.number}번</div>
            <div class="student-emotion">${student.emotion || '❓'}</div>
            <div class="student-emotion-text">${student.emotionText || '기분 선택'}</div>
        `;

        container.appendChild(card);
    });
}

// 감정 선택 모달 열기
function openEmotionModal(studentNumber) {
    state.currentStudent = studentNumber;
    document.getElementById('modal-student-number').textContent = studentNumber;
    document.getElementById('emotion-modal').classList.add('active');
}

// 모달 닫기
function closeModal() {
    document.getElementById('emotion-modal').classList.remove('active');
    state.currentStudent = null;
}

// 감정 선택
function selectEmotion(emotion, emotionType) {
    if (!state.currentStudent) return;

    const student = state.students.find(s => s.number === state.currentStudent);
    student.emotion = emotion;
    student.emotionType = emotionType;
    student.emotionText = emotionNames[emotion];

    // 히스토리 저장
    state.emotionHistory.push({
        student: state.currentStudent,
        emotion: emotion,
        emotionType: emotionType,
        timestamp: new Date().toISOString()
    });

    // UI 업데이트
    generateStudentCards();
    updateDashboard();
    updateEmotionWorld();
    saveData();
    closeModal();

    // 축하 효과
    showCelebration();
}

// 축하 효과
function showCelebration() {
    // 간단한 알림
    const message = document.createElement('div');
    message.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px 60px;
        border-radius: 20px;
        font-size: 2em;
        font-weight: bold;
        z-index: 10000;
        animation: fadeIn 0.5s ease;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    `;
    message.textContent = '감정을 선택했어요! 👍';
    document.body.appendChild(message);

    setTimeout(() => {
        message.style.animation = 'fadeOut 0.5s ease';
        setTimeout(() => message.remove(), 500);
    }, 1500);
}

// 대시보드 업데이트 (탭2)
function updateDashboard() {
    // 통계 계산
    const stats = {
        positive: state.students.filter(s => s.emotionType === 'positive').length,
        neutral: state.students.filter(s => s.emotionType === 'neutral').length,
        negative: state.students.filter(s => s.emotionType === 'negative').length,
        unselected: state.students.filter(s => !s.emotion).length
    };

    document.getElementById('positive-count').textContent = stats.positive;
    document.getElementById('neutral-count').textContent = stats.neutral;
    document.getElementById('negative-count').textContent = stats.negative;
    document.getElementById('unselected-count').textContent = stats.unselected;

    // 차트 업데이트
    updateEmotionChart(stats);

    // 세부 감정 분포
    updateEmotionDetails();
}

// 감정 차트 (탭2)
function updateEmotionChart(stats) {
    const ctx = document.getElementById('emotionChart');
    if (!ctx) return;

    if (state.charts.emotion) {
        state.charts.emotion.destroy();
    }

    state.charts.emotion = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['좋은 기분 😊', '보통 😐', '힘든 기분 😢', '미선택 ❓'],
            datasets: [{
                data: [stats.positive, stats.neutral, stats.negative, stats.unselected],
                backgroundColor: [
                    '#4ade80',
                    '#facc15',
                    '#ef4444',
                    '#94a3b8'
                ],
                borderWidth: 3,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            size: 16,
                            weight: 'bold'
                        },
                        padding: 20
                    }
                },
                tooltip: {
                    titleFont: {
                        size: 18
                    },
                    bodyFont: {
                        size: 16
                    },
                    padding: 15
                }
            }
        }
    });
}

// 세부 감정 분포
function updateEmotionDetails() {
    const container = document.getElementById('emotion-details');
    if (!container) return;

    const emotionCounts = {};
    state.students.forEach(student => {
        if (student.emotion) {
            emotionCounts[student.emotion] = (emotionCounts[student.emotion] || 0) + 1;
        }
    });

    container.innerHTML = '';
    Object.entries(emotionCounts)
        .sort((a, b) => b[1] - a[1])
        .forEach(([emoji, count]) => {
            const item = document.createElement('div');
            item.className = 'emotion-detail-item';
            item.innerHTML = `
                <span class="emotion-detail-emoji">${emoji}</span>
                <div>${emotionNames[emoji]}</div>
                <div style="font-size: 2em; margin-top: 10px;">${count}명</div>
            `;
            container.appendChild(item);
        });
}

// 감정 세계 애니메이션 (탭3)
function updateEmotionWorld() {
    const container = document.getElementById('emotion-world');
    if (!container) return;

    container.innerHTML = '';

    state.students.forEach(student => {
        if (!student.emotion) return;

        const floatingStudent = document.createElement('div');
        floatingStudent.className = 'floating-student';

        // 감정 타입에 따라 위치 설정
        let x, y;
        if (student.emotionType === 'positive') {
            x = Math.random() * 30 + 10; // 왼쪽 영역
            y = Math.random() * 60 + 10;
        } else if (student.emotionType === 'neutral') {
            x = Math.random() * 30 + 35; // 중앙 영역
            y = Math.random() * 60 + 10;
        } else if (student.emotionType === 'negative') {
            x = Math.random() * 30 + 65; // 오른쪽 영역
            y = Math.random() * 60 + 10;
        } else {
            x = Math.random() * 80 + 10;
            y = Math.random() * 80 + 10;
        }

        floatingStudent.style.left = x + '%';
        floatingStudent.style.top = y + '%';
        floatingStudent.style.animationDelay = Math.random() * 3 + 's';

        floatingStudent.innerHTML = `
            <div class="floating-emoji">${student.emotion}</div>
            <div class="floating-number">${student.number}번</div>
        `;

        container.appendChild(floatingStudent);
    });
}

// 타임라인 차트 (탭4)
function updateTimelineChart() {
    const ctx = document.getElementById('timelineChart');
    if (!ctx) return;

    if (state.charts.timeline) {
        state.charts.timeline.destroy();
    }

    // 최근 10개의 감정 변화 표시
    const recentHistory = state.emotionHistory.slice(-10);
    const labels = recentHistory.map((h, i) => `${i + 1}번째`);
    const positiveData = recentHistory.map(h => h.emotionType === 'positive' ? 1 : 0);
    const neutralData = recentHistory.map(h => h.emotionType === 'neutral' ? 1 : 0);
    const negativeData = recentHistory.map(h => h.emotionType === 'negative' ? 1 : 0);

    state.charts.timeline = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: '좋은 기분 😊',
                    data: positiveData,
                    borderColor: '#4ade80',
                    backgroundColor: 'rgba(74, 222, 128, 0.1)',
                    tension: 0.4
                },
                {
                    label: '보통 😐',
                    data: neutralData,
                    borderColor: '#facc15',
                    backgroundColor: 'rgba(250, 204, 21, 0.1)',
                    tension: 0.4
                },
                {
                    label: '힘든 기분 😢',
                    data: negativeData,
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    labels: {
                        font: { size: 14, weight: 'bold' }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    ticks: {
                        font: { size: 12 }
                    }
                }
            }
        }
    });
}

// 주간 차트 (탭4)
function updateWeeklyChart() {
    const ctx = document.getElementById('weeklyChart');
    if (!ctx) return;

    if (state.charts.weekly) {
        state.charts.weekly.destroy();
    }

    // 요일별 데이터 (시뮬레이션)
    const weekDays = ['월', '화', '수', '목', '금'];
    const weeklyData = weekDays.map(() => ({
        positive: Math.floor(Math.random() * 10) + 5,
        neutral: Math.floor(Math.random() * 5) + 2,
        negative: Math.floor(Math.random() * 3) + 1
    }));

    state.charts.weekly = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: weekDays,
            datasets: [
                {
                    label: '좋은 기분 😊',
                    data: weeklyData.map(d => d.positive),
                    backgroundColor: '#4ade80'
                },
                {
                    label: '보통 😐',
                    data: weeklyData.map(d => d.neutral),
                    backgroundColor: '#facc15'
                },
                {
                    label: '힘든 기분 😢',
                    data: weeklyData.map(d => d.negative),
                    backgroundColor: '#ef4444'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    labels: {
                        font: { size: 14, weight: 'bold' }
                    }
                }
            },
            scales: {
                x: {
                    stacked: true,
                    ticks: {
                        font: { size: 14, weight: 'bold' }
                    }
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    ticks: {
                        font: { size: 12 }
                    }
                }
            }
        }
    });
}

// 칭찬 메시지 표시
function showRandomPraise() {
    const randomMessage = praiseMessages[Math.floor(Math.random() * praiseMessages.length)];
    const container = document.getElementById('praise-messages');
    container.style.animation = 'none';
    setTimeout(() => {
        container.textContent = randomMessage;
        container.style.animation = 'fadeIn 0.5s ease';
    }, 10);
}

// 선생님 메시지 저장
function saveTeacherMessage() {
    const message = document.getElementById('teacher-message').value;
    if (message.trim()) {
        localStorage.setItem('teacherMessage', message);
        alert('선생님의 메시지가 저장되었습니다! 💝');
    }
}

// 데이터 저장
function saveData() {
    localStorage.setItem('classroomEmotionData', JSON.stringify({
        students: state.students,
        emotionHistory: state.emotionHistory,
        lastUpdated: new Date().toISOString()
    }));
}

// 데이터 로드
function loadSavedData() {
    const saved = localStorage.getItem('classroomEmotionData');
    if (saved) {
        try {
            const data = JSON.parse(saved);

            // 같은 날짜의 데이터만 로드
            const lastUpdated = new Date(data.lastUpdated);
            const today = new Date();
            if (lastUpdated.toDateString() === today.toDateString()) {
                state.students = data.students;
                state.emotionHistory = data.emotionHistory;
            }
        } catch (error) {
            console.error('데이터 로드 실패:', error);
        }
    }

    // 선생님 메시지 로드
    const teacherMessage = localStorage.getItem('teacherMessage');
    if (teacherMessage) {
        document.getElementById('teacher-message').value = teacherMessage;
    }
}

// CSS 애니메이션 추가
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
        }
        to {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.8);
        }
    }
`;
document.head.appendChild(style);

// 초기 칭찬 메시지 표시
setTimeout(() => {
    showRandomPraise();
}, 1000);
