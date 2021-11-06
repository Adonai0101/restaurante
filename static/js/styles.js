

const btn_sidebar = document.querySelector('.nav-btn')
btn_sidebar.addEventListener('click',function(){
    const activar = document.querySelector('.sidebar')
    activar.classList.toggle('active')
    console.log('puchado')
})


