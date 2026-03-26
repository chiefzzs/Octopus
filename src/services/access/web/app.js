const { createApp, ref, reactive, computed, onMounted, watch, nextTick } = Vue;
const { ElMessage, ElMessageBox } = ElementPlus;

const App = {
    setup() {
        const activeTab = ref('chat');
        const ws = ref(null);
        const isConnected = ref(false);
        const isTyping = ref(false);
        const inputMessage = ref('');
        const messages = ref([]);
        const services = ref([
            { name: '接入服务', key: 'access', icon: '🚪', status: 'online', port: 8000 },
            { name: '控制服务', key: 'control', icon: '🎛️', status: 'online', port: 8001 },
            { name: '执行服务', key: 'execution', icon: '⚡', status: 'online', port: 8002 },
            { name: '能力服务', key: 'capability', icon: '🛠️', status: 'online', port: 8003 },
            { name: '实时服务', key: 'realtime', icon: '📡', status: 'online', port: 8004 }
        ]);
        const skills = ref([
            { id: 1, name: '文件操作', icon: '📄', desc: '文件读写、目录管理、格式转换', category: '内置' },
            { id: 2, name: '网络请求', icon: '🌐', desc: 'HTTP请求、API调用、数据抓取', category: '内置' },
            { id: 3, name: '系统操作', icon: '💻', desc: '系统命令、进程管理、环境变量', category: '内置' },
            { id: 4, name: '数据处理', icon: '📊', desc: '数据解析、数据转换、数据验证', category: '内置' },
            { id: 5, name: '通用工作流', icon: '🔄', desc: '工作流定义、流程执行', category: '插件' },
            { id: 6, name: '文档生成', icon: '📝', desc: '文档生成、格式化', category: '插件' }
        ]);
        const history = ref([
            { id: 1, title: '帮我整理项目文档', time: '2026-03-26 15:30', preview: '用户请求: 帮我整理一下项目的技术文档...' },
            { id: 2, title: '分析代码结构', time: '2026-03-26 14:20', preview: '用户请求: 分析一下src目录下的代码结构...' },
            { id: 3, title: '创建测试脚本', time: '2026-03-26 11:45', preview: '用户请求: 为执行服务创建单元测试脚本...' }
        ]);
        const messagesEnd = ref(null);

        const connectWebSocket = () => {
            try {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws`;
                ws.value = new WebSocket(wsUrl);

                ws.value.onopen = () => {
                    isConnected.value = true;
                    ElMessage.success('WebSocket连接成功');
                };

                ws.value.onmessage = (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        handleWebSocketMessage(data);
                    } catch (e) {
                        console.error('解析WebSocket消息失败:', e);
                    }
                };

                ws.value.onclose = () => {
                    isConnected.value = false;
                    ElMessage.warning('WebSocket连接已断开，正在尝试重连...');
                    setTimeout(connectWebSocket, 3000);
                };

                ws.value.onerror = (error) => {
                    console.error('WebSocket错误:', error);
                    isConnected.value = false;
                };
            } catch (error) {
                console.error('WebSocket连接失败:', error);
                setTimeout(connectWebSocket, 3000);
            }
        };

        const handleWebSocketMessage = (data) => {
            if (data.type === 'message') {
                isTyping.value = false;
                messages.value.push({
                    id: Date.now(),
                    role: 'assistant',
                    content: data.content,
                    timestamp: new Date().toLocaleTimeString()
                });
            } else if (data.type === 'typing') {
                isTyping.value = true;
            } else if (data.type === 'status') {
                updateServiceStatus(data.service, data.status);
            }
        };

        const updateServiceStatus = (serviceKey, status) => {
            const service = services.value.find(s => s.key === serviceKey);
            if (service) {
                service.status = status;
            }
        };

        const sendMessage = async () => {
            if (!inputMessage.value.trim()) return;

            const userMessage = {
                id: Date.now(),
                role: 'user',
                content: inputMessage.value,
                timestamp: new Date().toLocaleTimeString()
            };
            messages.value.push(userMessage);

            const messageToSend = inputMessage.value;
            inputMessage.value = '';
            isTyping.value = true;

            try {
                if (ws.value && isConnected.value) {
                    ws.value.send(JSON.stringify({
                        type: 'message',
                        content: messageToSend
                    }));
                } else {
                    const response = await fetch('/api/access/message', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ content: messageToSend })
                    });
                    const result = await response.json();
                    isTyping.value = false;
                    messages.value.push({
                        id: Date.now(),
                        role: 'assistant',
                        content: result.message || '已收到您的消息',
                        timestamp: new Date().toLocaleTimeString()
                    });
                }
            } catch (error) {
                console.error('发送消息失败:', error);
                isTyping.value = false;
                ElMessage.error('发送消息失败，请稍后重试');
            }
        };

        const handleKeyDown = (event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        };

        const checkServiceStatus = async () => {
            for (const service of services.value) {
                try {
                    const response = await fetch(`http://localhost:${service.port}/health`);
                    service.status = response.ok ? 'online' : 'offline';
                } catch (error) {
                    service.status = 'offline';
                }
            }
        };

        const loadHistoryItem = (item) => {
            activeTab.value = 'chat';
            ElMessage.info(`加载历史会话: ${item.title}`);
        };

        const showSkillDetail = (skill) => {
            ElMessageBox.alert(skill.desc, skill.name, {
                confirmButtonText: '确定'
            });
        };

        const scrollToBottom = () => {
            nextTick(() => {
                if (messagesEnd.value) {
                    messagesEnd.value.scrollIntoView({ behavior: 'smooth' });
                }
            });
        };

        watch(messages, () => {
            scrollToBottom();
        }, { deep: true });

        onMounted(() => {
            connectWebSocket();
            checkServiceStatus();
            setInterval(checkServiceStatus, 30000);
        });

        return {
            activeTab,
            isConnected,
            isTyping,
            inputMessage,
            messages,
            services,
            skills,
            history,
            messagesEnd,
            sendMessage,
            handleKeyDown,
            loadHistoryItem,
            showSkillDetail
        };
    },
    template: `
        <div class="main-container">
            <header class="header">
                <h1>
                    <span class="logo">🐙</span>
                    八爪鱼 - AI智能体执行框架
                </h1>
                <div class="header-right">
                    <div class="status-indicator">
                        <span :class="['status-dot', { offline: !isConnected }]"></span>
                        <span>{{ isConnected ? '已连接' : '未连接' }}</span>
                    </div>
                </div>
            </header>

            <div class="content">
                <aside class="sidebar">
                    <div class="sidebar-menu">
                        <div 
                            :class="['menu-item', { active: activeTab === 'chat' }]"
                            @click="activeTab = 'chat'"
                        >
                            <span class="icon">💬</span>
                            <span>智能对话</span>
                        </div>
                        <div 
                            :class="['menu-item', { active: activeTab === 'status' }]"
                            @click="activeTab = 'status'"
                        >
                            <span class="icon">📊</span>
                            <span>服务状态</span>
                        </div>
                        <div 
                            :class="['menu-item', { active: activeTab === 'skills' }]"
                            @click="activeTab = 'skills'"
                        >
                            <span class="icon">🛠️</span>
                            <span>技能管理</span>
                        </div>
                        <div 
                            :class="['menu-item', { active: activeTab === 'history' }]"
                            @click="activeTab = 'history'"
                        >
                            <span class="icon">📜</span>
                            <span>历史记录</span>
                        </div>
                    </div>
                </aside>

                <main class="main-content">
                    <div v-if="activeTab === 'chat'" class="chat-container">
                        <div class="chat-messages">
                            <div v-for="msg in messages" :key="msg.id" :class="['message', msg.role]">
                                <div class="message-header">
                                    <span>{{ msg.role === 'user' ? '👤 用户' : '🤖 八爪鱼' }}</span>
                                    <span style="font-size: 12px; opacity: 0.8;">{{ msg.timestamp }}</span>
                                </div>
                                <div class="message-content">{{ msg.content }}</div>
                            </div>
                            <div v-if="isTyping" class="message assistant">
                                <div class="message-header">
                                    <span>🤖 八爪鱼</span>
                                </div>
                                <div class="typing-indicator">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                            <div ref="messagesEnd"></div>
                        </div>

                        <div class="chat-input-container">
                            <div class="chat-input-wrapper">
                                <div class="chat-textarea">
                                    <textarea
                                        v-model="inputMessage"
                                        placeholder="输入您的消息... (按Enter发送)"
                                        rows="3"
                                        @keydown="handleKeyDown"
                                    ></textarea>
                                </div>
                                <button 
                                    class="send-button"
                                    :disabled="!inputMessage.trim()"
                                    @click="sendMessage"
                                >
                                    ➤
                                </button>
                            </div>
                        </div>
                    </div>

                    <div v-if="activeTab === 'status'" class="status-panel">
                        <div class="status-card">
                            <h3>
                                <span>🔧</span>
                                微服务状态
                            </h3>
                            <div v-for="service in services" :key="service.key" class="service-item">
                                <div class="service-name">
                                    <div :class="['service-icon', service.key]">{{ service.icon }}</div>
                                    <div class="service-info">
                                        <h4>{{ service.name }}</h4>
                                        <span>端口: {{ service.port }}</span>
                                    </div>
                                </div>
                                <div class="service-status">
                                    <span :class="['status-badge', service.status]">
                                        {{ service.status === 'online' ? '运行中' : '离线' }}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <div class="status-card">
                            <h3>
                                <span>📈</span>
                                系统概览
                            </h3>
                            <div style="color: #8c8c8c; font-size: 14px;">
                                <p>版本: v0.3.0 Beta</p>
                                <p>运行时间: 2小时 34分钟</p>
                                <p>已处理任务: 128</p>
                            </div>
                        </div>
                    </div>

                    <div v-if="activeTab === 'skills'" class="skills-panel">
                        <div class="skills-grid">
                            <div 
                                v-for="skill in skills" 
                                :key="skill.id" 
                                class="skill-card"
                                @click="showSkillDetail(skill)"
                            >
                                <div class="skill-card-header">
                                    <div class="skill-card-icon">{{ skill.icon }}</div>
                                    <div class="skill-card-title">
                                        <h4>{{ skill.name }}</h4>
                                        <span>{{ skill.category }}</span>
                                    </div>
                                </div>
                                <div class="skill-card-desc">{{ skill.desc }}</div>
                            </div>
                        </div>
                    </div>

                    <div v-if="activeTab === 'history'" class="history-panel">
                        <div v-if="history.length > 0" class="history-list">
                            <div 
                                v-for="item in history" 
                                :key="item.id" 
                                class="history-item"
                                @click="loadHistoryItem(item)"
                            >
                                <div class="history-item-header">
                                    <span class="history-item-title">{{ item.title }}</span>
                                    <span class="history-item-time">{{ item.time }}</span>
                                </div>
                                <div class="history-item-preview">{{ item.preview }}</div>
                            </div>
                        </div>
                        <div v-else class="empty-state">
                            <div class="empty-state-icon">📭</div>
                            <div class="empty-state-text">暂无历史记录</div>
                        </div>
                    </div>
                </main>
            </div>
        </div>
    `
};

const app = createApp(App);
app.use(ElementPlus);
app.mount('#app');
