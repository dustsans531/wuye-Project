// footer.js - 可复用的页脚组件

class FooterComponent {
    constructor() {
        this.footerElement = null;
        this.cssLink = null;
    }

    // 创建footer组件
    create() {
        // 创建footer HTML结构
        const footerHTML = `
        <footer class="footer">
            <div class="container">
                <div class="footer-content">
                    <div class="footer-logo">
                        <i class="fa fa-home"></i>
                        <span>智慧物业</span>
                        <p>打造智慧、安全、舒适的现代化社区</p>
                        <div class="footer-social">
                            <a href="#"><i class="fa fa-weixin"></i></a>
                            <a href="#"><i class="fa fa-weibo"></i></a>
                            <a href="#"><i class="fa fa-qq"></i></a>
                        </div>
                    </div>
                    
                    <div class="footer-links">
                        <h4>快速链接</h4>
                        <ul>
                            <li><a href="#home">首页</a></li>
                            <li><a href="#service">物业服务</a></li>
                            <li><a href="#notice">小区公告</a></li>
                            <li><a href="#fee">费用缴纳</a></li>
                            <li><a href="#contact">联系我们</a></li>
                        </ul>
                    </div>
                    
                    <div class="footer-links">
                        <h4>服务支持</h4>
                        <ul>
                            <li><a href="#">常见问题</a></li>
                            <li><a href="#">业主手册</a></li>
                            <li><a href="#">物业服务条款</a></li>
                            <li><a href="#">投诉建议</a></li>
                            <li><a href="#">紧急联系</a></li>
                        </ul>
                    </div>
                    
                    <div class="footer-contact">
                        <h4>联系方式</h4>
                        <p><i class="fa fa-map-marker"></i> 哈尔滨市宾西县宾西大学城9号哈尔滨信息工程学院</p>
                        <p><i class="fa fa-phone"></i> 010-8888-7777</p>
                        <p><i class="fa fa-envelope-o"></i> property@zhjy.com</p>
                    </div>
                </div>
                
                <div class="copyright">
                    <p>© 2023 智慧物业有限公司 版权所有 | 京ICP备12345678号</p>
                </div>
            </div>
        </footer>`;

        // 创建footer元素
        const tempContainer = document.createElement('div');
        tempContainer.innerHTML = footerHTML;
        this.footerElement = tempContainer.firstElementChild;

        // 创建CSS样式
        this.createStyles();

        // 初始化事件监听
        this.initEvents();

        return this.footerElement;
    }

    // 创建CSS样式
    createStyles() {
        // 检查是否已经存在样式
        if (document.getElementById('footer-styles')) {
            return;
        }

        // 创建样式链接
        this.cssLink = document.createElement('link');
        this.cssLink.id = 'footer-styles';
        this.cssLink.rel = 'stylesheet';
        this.cssLink.href = 'css/footer.css';
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
        if (!this.footerElement) return;

        // 为页脚中的链接添加平滑滚动效果
        const footerLinks = this.footerElement.querySelectorAll('a');
        
        footerLinks.forEach(link => {
            // 只处理内部链接（以#开头的链接）
            const href = link.getAttribute('href');
            if (href && href.startsWith('#')) {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    
                    const targetId = href;
                    const targetElement = document.querySelector(targetId);
                    
                    if (targetElement) {
                        window.scrollTo({
                            top: targetElement.offsetTop - 80, // 考虑导航栏高度
                            behavior: 'smooth'
                        });
                    }
                });
            }
        });
    }

    // 更新公司信息
    updateCompanyInfo(companyName, year) {
        if (!this.footerElement) return;
        const copyrightElement = this.footerElement.querySelector('.copyright p');
        if (copyrightElement) {
            copyrightElement.textContent = `© ${year || '2023'} ${companyName || '智慧物业有限公司'} 版权所有 | 京ICP备12345678号`;
        }
    }

    // 更新联系方式
    updateContactInfo(phone, email, address) {
        if (!this.footerElement) return;
        
        // 更新电话
        if (phone) {
            const phoneElement = this.footerElement.querySelector('.footer-contact p:nth-child(2)');
            if (phoneElement) {
                phoneElement.innerHTML = `<i class="fa fa-phone"></i> ${phone}`;
            }
        }
        
        // 更新邮箱
        if (email) {
            const emailElement = this.footerElement.querySelector('.footer-contact p:nth-child(3)');
            if (emailElement) {
                emailElement.innerHTML = `<i class="fa fa-envelope-o"></i> ${email}`;
            }
        }
        
        // 更新地址
        if (address) {
            const addressElement = this.footerElement.querySelector('.footer-contact p:nth-child(1)');
            if (addressElement) {
                addressElement.innerHTML = `<i class="fa fa-map-marker"></i> ${address}`;
            }
        }
    }
}

// 导出组件
window.FooterComponent = FooterComponent;