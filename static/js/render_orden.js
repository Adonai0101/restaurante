
const btn_pagar = document.querySelector('#btn_pagar')
btn_pagar.addEventListener('click', () => {


    const nota = document.querySelector('#nota')
    console.log(nota.value)

    let datos = {
        'domicilio': domicilio,
        'nota': nota.value
    }

    console.log(datos)
    
    //obtengo la pantalla de carga
    pantalla = document.querySelector('.pantalla-carga')
    pantalla.classList.toggle('show')

        axios({
            method: 'POST',
            url: '/panel/comprar',
            data: datos
        })
        .then(resp => {
            console.log(resp)

        })
        .then(x => {
            window.location.href = '/panel/compra/hecho';
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
