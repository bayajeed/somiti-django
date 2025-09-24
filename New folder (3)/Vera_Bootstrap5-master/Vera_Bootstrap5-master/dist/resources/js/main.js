//Replace Text in Header
const checkReplace = document.querySelector('.replace-me');

if(checkReplace !== null){
    const replace = new ReplaceMe(checkReplace, {
        animation: 'animated fadIn',
        speed: 2000,
        separator: ',',
        loopCount: 'infinite',
        autoRun: true
    });
}

//adds style to navbar after nav at a certain position on screen
function navStyleOnScroll(){
    //targets HTML element
    const navbar = document.querySelector('#main-nav');

    window.addEventListener('scroll', () => {
        if(window.scrollY > 50){
            //adds background & shadow
            //navbar.classList.add('bg-dark');
            navbar.classList.add('border-bottom');
            navbar.classList.add('border-primary');
            navbar.classList.add('border-2');
            navbar.classList.add('fixed-top');

            
        }else{
            //removes background & shadow
            //navbar.classList.remove('bg-dark');
            navbar.classList.remove('border-bottom');
            navbar.classList.remove('border-primary');
            navbar.classList.remove('border-2');
            navbar.classList.remove('fixed-top');
        }
    });
}

//runs function after the page has loaded
document.addEventListener('DOMContentLoaded', navStyleOnScroll);