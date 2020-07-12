import '../scss/reset.scss';
import '../scss/style.scss';


console.log('base page init 2020/05/15');

window.addEventListener('DOMContentLoaded', () => {
    // 初期化処理（こちらの方が早いかも）
    const preload = document.getElementsByClassName('preload');
    console.log(preload);
    Array.prototype.forEach.call(preload, (element) => {
        element.classList.remove('preload');
    });
})
