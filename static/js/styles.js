

/* 
const close_alert = document.querySelector('#close_alert')
close_alert.addEventListener('click',function(){
    hide_alert()
})

const btn_show = document.querySelector('#alerta')
btn_show.addEventListener('click',function(){ 
    show_alert()
})

*/


function show_alert(){
    const alert =  document.querySelector('.alert')
    alert.classList.remove('hide')
    alert.classList.add('show')
    alert.classList.add('showalert')

    setTimeout(hide_alert,2000)
}

function hide_alert(){
    const alert =  document.querySelector('.alert')
    alert.classList.remove('show')
    alert.classList.add('hide')
}





const btn_sidebar = document.querySelector('.nav-btn')
btn_sidebar.addEventListener('click',function(){
    const activar = document.querySelector('.sidebar')
    activar.classList.toggle('active')
    console.log('puchado')
})


const modal_close = document.querySelector('.modal_close')
modal_close.addEventListener('click',modal_show)


// activar o desactivar el modal
function modal_show(){
    const modal = document.querySelector('.modal')
    modal.classList.toggle('modal_show')
}




