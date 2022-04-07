
/*
const btn_comprar =  document.querySelector('#btn_comprar')


btn_comprar.addEventListener('click',async ()=>{
    const select_canditad = document.querySelector('#cantidad')
    let cantidad = select_canditad.value; 
    let path = window.location.pathname;
    let id_producto = path.substring(16,40)
    console.log('click')
    let pedido = {
        'id':id_producto,
        'cantidad':cantidad
    }

    axios({
        method: 'POST',
        url: '/panel/orden',
        data: pedido
    })
    .then(resp => {
        console.log(resp)
    })
    .then(x => {
        console.log('se envio')
        window.location.href = '/panel/orden';
    })

})

*/


function comprar_ahora(id_producto){
    console.log('precionamos comprar ahora')
    const select_canditad = document.querySelector('#cantidad')
    let cantidad = select_canditad.value; 

    let pedido = {
        'id':id_producto,
        'cantidad':cantidad
    }

    axios({
        method: 'POST',
        url: '/panel/orden',
        data: pedido
    })
    .then(resp => {
        console.log(resp)
    })
    .then(x => {
        console.log('se envio')
        window.location.href = '/compra';
    })
    console.log(pedido)
}

