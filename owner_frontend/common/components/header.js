// header.js - 可复用的页头组件

class HeaderComponent {
    constructor() {
        this.headerElement = null;
        this.cssLink = null;
        this.mobileMenuBtn = null;
        this.mobileNav = null;
    }

    // 创建header组件
    create() {
        // 创建header HTML结构
        const headerHTML = `
        <header class="navbar">
            <div class="container">
                <div class="logo">
                    <i class="fa fa-home"></i>
                    <span>智慧物业</span>
                </div>
                
                <!-- 桌面导航 -->
                <nav class="main-nav">
                    <a href="#home" class="active">首页</a>
                    <a href="#service">服务</a>
                    <a href="#notice">公告</a>
                    <a href="#fee">缴费</a>
                    <a href="#contact">联系</a>
                </nav>
                
                <!-- 用户区域 -->
                <div class="user-area">
                    <button class="ring"><i class="fa fa-bell-o"></i></button>
                    <div class="user-tx">
                        <img src="img/yhtx.jpg" alt="用户头像">
                        <span>业主您好</span>
                    </div>
                    <!-- 移动端菜单按钮 -->
                    <button class="mobile-menu-btn">
                        <i class="fa fa-bars"></i>
                    </button>
                </div>
            </div>
            
            <!-- 移动端导航菜单 -->
            <div class="mobile-nav">
                <a href="#home">首页</a>
                <a href="#service">服务</a>
                <a href="#notice">公告</a>
                <a href="#fee">缴费</a>
                <a href="#contact">联系</a>
            </div>
        </header>`;

        // 创建header元素
        const tempContainer = document.createElement('div');
        tempContainer.innerHTML = headerHTML;
        this.headerElement = tempContainer.firstElementChild;

        // 创建CSS样式
        this.createStyles();

        // 初始化事件监听
        this.initEvents();

        return this.headerElement;
    }

    // 创建CSS样式
    createStyles() {
        // 检查是否已经存在样式
        if (document.getElementById('header-styles')) {
            return;
        }

        // 创建样式链接
        this.cssLink = document.createElement('link');
        this.cssLink.id = 'header-styles';
        this.cssLink.rel = 'stylesheet';
        this.cssLink.href = 'css/header.css';
        document.head.appendChild(this.cssLink);

        // 创建Font Awesome链接
        if (!document.querySelector('link[href*="font-awesome"]')) {
            const fontAwesomeLink = document.createElement('link');
            fontAwesomeLink.rel = 'stylesheet';
            fontAwesomeLink.href = 'https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css';
            document.head.appendChild(fontAwesomeLink);
        }
    }

    // 初始化事件
    initEvents() {
        if (!this.headerElement) return;

        // 获取DOM元素
        this.mobileMenuBtn = this.headerElement.querySelector('.mobile-menu-btn');
        this.mobileNav = this.headerElement.querySelector('.mobile-nav');

        // 移动端菜单切换
        if (this.mobileMenuBtn && this.mobileNav) {
            this.mobileMenuBtn.addEventListener('click', () => {
                this.mobileNav.classList.toggle('active');
            });
        }

        // 导航栏滚动效果
        const navbar = this.headerElement;
        let lastScrollTop = 0;
        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            // 导航栏高度变化
            if (scrollTop > 100) {
                navbar.style.padding = '8px 0';
            } else {
                navbar.style.padding = '0';
            }
            
            lastScrollTop = scrollTop;
        });

        // 导航栏链接平滑滚动
        const navLinks = this.headerElement.querySelectorAll('nav a, .mobile-nav a');
        
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                
                // 关闭移动菜单（如果打开）
                if (this.mobileNav && this.mobileNav.classList.contains('active')) {
                    this.mobileNav.classList.remove('active');
                }
                
                const targetId = link.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80, // 考虑导航栏高度
                        behavior: 'smooth'
                    });
                    
                    // 更新活跃链接
                    navLinks.forEach(navLink => {
                        navLink.classList.remove('active');
                    });
                    link.classList.add('active');
                }
            });
        });
    }

    // 更新用户信息
    updateUserInfo(username) {
        if (!this.headerElement) return;
        const userTextElement = this.headerElement.querySelector('.user-tx span');
        if (userTextElement) {
            userTextElement.textContent = username || '业主您好';
        }
    }

    // 更新用户头像
    updateUserAvatar(avatarUrl) {
        if (!this.headerElement) return;
        const avatarElement = this.headerElement.querySelector('.user-tx img');
        if (avatarElement && avatarUrl) {
            avatarElement.src = avatarUrl;
        }
    }
}

// 导出组件
window.HeaderComponent = HeaderComponent;