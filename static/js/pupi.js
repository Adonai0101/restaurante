// sidebar toggle
const btnToggle = document.querySelector('.pupi-toggle-btn');

btnToggle.addEventListener('click', function () {
    console.log('clik')
    document.querySelector('.pupi-sidebar').classList.toggle('active');

});