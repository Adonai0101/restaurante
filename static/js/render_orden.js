
const btn_pagar = document.querySelector('#btn_pagar')
btn_pagar.addEventListener('click', () => {

    let datos = {
        'domicilio': domicilio
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
            console.log('se envio')
            window.location.href = '/panel/compra/hecho';
        })

})

// lanzador del modal
const btn_otraDireccion = document.querySelector('#otra_direccion')
btn_otraDireccion.addEventListener('click', modal_show)


const btn_dom_modal = document.querySelector('#btn-dom-modal')
btn_dom_modal.addEventListener('click', (e) => {
    e.preventDefault()
    const new_dom = document.querySelector('#new_dom')
    domicilio = new_dom.value;
    dom.innerHTML = domicilio;
    modal_show()
    show_alert()
})


let domicilio = ""
const dom = document.querySelector('#domicilio')
domicilio = dom.innerHTML;
