function redirect_login() {
    var login_page = '/html/login.html';
    window.location.href = login_page;
}

function redirect_signup() {
    var signup_page = '/html/signup.html';
    window.location.href = signup_page;
}

function redirect_profile() {
    var profile_page = '/html/profile.html';
    window.location.href = profile_page;
}


document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelectorAll('.slides');
    const sidebarTexts = document.querySelectorAll('.sidebar-text');
  

    function scrollToSlide(index) {
        if (slides[index]) {
            slides[index].scrollIntoView({ behavior: 'smooth' });
        }
    }
    
    sidebarTexts.forEach((sidebarText, index) => {
        sidebarText.addEventListener('click', function () {
            scrollToSlide(index);
        });
    });

    const sidebarText_default = sidebarTexts[0];
    sidebarText_default.style.color = '#ffffff';
    sidebarText_default.style.transform = 'scale(1.1)';

    window.addEventListener('scroll', function () {
        const scrollPosition = window.scrollY;
        slides.forEach((slide, index) => {
            const slideTop = slide.offsetTop;
            const slideBottom = slideTop + slide.clientHeight;
    
            if (scrollPosition >= slideTop -50  && scrollPosition < slideBottom) {
                sidebarTexts.forEach((sidebarText, sidebarIndex) => {
                    if(sidebarIndex === index) {
                        sidebarText.style.color = '#ffffff';
                        sidebarText.style.transform = 'scale(1.1)';
                    } else {
                        sidebarText.style.color = '#7e94a9';
                        sidebarText.style.transform = 'scale(1)';
                    }
                });
            }
        });
    });
});
  