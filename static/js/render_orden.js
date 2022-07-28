
const btn_pagar = document.querySelector('#btn_pagar')
btn_pagar.addEventListener('click', () => {

    const nota = document.querySelector('#nota')

    let datos = {
        'domicilio': domicilio,
        'nota': nota.value
    }

    //Desactivamos el btn para que no pueda ser accionado mas de una vez
    btn_pagar.disabled = true;
    btn_pagar.classList.add('btn-dis')

    console.log(datos)
    console.log('estoy aqui')

        axios({
            method: 'POST',
            url: '/compra/',
            data: datos
        })
        .then(resp => {
            console.log('terminamois de hacer el pedido alv')
            console.log(resp)
            
        })
        .then(x => {
            window.location.href = '/panel/compra/hecho'
        })
})


const btn_dom_modal = document.querySelector('#btn-dom-modal')
btn_dom_modal.addEventListener('click', (e) => {
    e.preventDefault()

    const new_dom = document.querySelector('#new_dom')
    domicilio = new_dom.value;
    

    if(domicilio.length < 6){
        console.log("no se puede giardar esta shit")

        const alert = document.querySelector('.alert')
        
        alert.classList.remove('done')
        alert.classList.add('danger')

        alert.innerHTML = `
            <i class='bx bx-x alert-icon'></i>
            <p>Domicilio incorrecto</p>
        `
        modal_show()
        show_alert()


    }
    else{

        const alert = document.querySelector('.alert')
        
        alert.classList.remove('danger')
        alert.classList.add('done')

        alert.innerHTML = `
            <i class='bx bx-check-circle alert-icon'></i>
            <p>Nuevo domicilio</p>
        `

        dom.innerHTML = domicilio;
        modal_show()
        show_alert()
    }

})


let domicilio = ""
const dom = document.querySelector('#domicilio')
domicilio = dom.innerHTML;
