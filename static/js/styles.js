
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

//toggle loader
function loader_toggle(){
    const spinner_loader = document.querySelector('.loader')
    spinner_loader.classList.toggle('active')
}

//toggle btn-card
function btn_card_toggle(id){
    const menu = document.querySelector('#' + id)
    menu.classList.toggle('active')
}

// activar o desactivar el modal
function modal_show(){
    const modal = document.querySelector('.modal')
    modal.classList.toggle('modal_show')
}


//activat o desactivar el sidebar

function sidebar_toggle(){
    const activar = document.querySelector('.sidebar-fixed')
    activar.classList.toggle('active')
}


const btn_sidebar = document.querySelector('.nav-btn')
btn_sidebar.addEventListener('click',function(){
    const activar = document.querySelector('.sidebar')
    activar.classList.toggle('active')
})

function active_sidebar(){
    const activar = document.querySelector('.sidebar')
    activar.classList.toggle('active')
}











