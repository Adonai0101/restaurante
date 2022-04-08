
//boton de "agregar al carrito"
function agregar_carrito(id_vendedor,id_producto){

    const select_canditad = document.querySelector('#cantidad')
    let cantidad = select_canditad.value; 

    let item = {
        'id_vendedor':id_vendedor,
        'id_producto':id_producto,
        'cantidad':cantidad
    }

    axios({
        method: 'POST',
        url: '/carrito/add',
        data: item
    })
    .then(resp => {
        console.log(resp)
    })
    .then(x => {
        console.log("se agrego bien vvergas")
        show_alert()
    })
}

function render_all(){
    url = "/carrito/list" 
    axios({
        method: 'GET',
        url: url
    })
    .then(resp => {
        console.log(resp.data['lista_carrito'])
        const lista = resp.data['lista_carrito']
        lista.forEach(element => render_paquete(element));
    })
}

function render_paquete(id){
    url = "/carrito/" + id
    axios({
        method: 'GET',
        url: url
    })
    .then(resp => {
        data = resp.data['paquete']
        let id_carrito = id
        //console.log(data)
        console.log(data.productos)
        const item = data.productos[0]
        //console.log(item,)

        const contenedor = document.querySelector('.main-container')
        const paquete_body = document.querySelector('.paquete_body')
        contenedor.innerHTML += `
                <div class="paquete mb">
                <div class="paquete-header">
                    <p>Vendedor: <span>${data.nombre_vendedor}</span></p>
                </div>
                <div class="paquete_body ">
                ${data.productos.map(val => `
                    <div class="h-card mb">
                        <img src="${val.foto_producto}" alt="">
                        <div class="pd">
                            <p>${val.nombre_producto}</p>
                            <p>Cantidad : ${val.cantidad}</p>
                            <P>Precio: $${val.precio}</P>
                            <button onclick="delete_item('${id_carrito}','${val.id_producto}')" class="btn btn-secondary">Eliminar</button>
                        </div>
                    </div>               
                `).join('')}

                </div>

                <div class="paquete_footer">
                    <p>Precio con envio: <span>$${data.total}</span></p>
                    <button class="btn btn-dark" onclick="comprar(data)">Comprar pedido</button>
                </div>
                
            </div>
        `
    })
}

function comprar(obj){
    console.log('estamos testeando')
    console.log(obj)

    axios({
        method: 'POST',
        url: '/carrito/comprar',
        data: obj
    })
    .then(resp => {
        console.log(resp)
    })
    .then(x => {
        console.log('correcto se envio esta shirt')
        //window.location.href = '/compra';
    })
    .then(a =>{
        console.log('--')
        setTimeout(function(){
            console.log("I am the third log after 1 seconds");
            window.location.href = '/compra';
        },1000);
    })
}

function delete_item(id_carrito,id_producto){
    console.log("estamos en delete")

    let item = {
        'id_carrito':id_carrito,
        'id_producto':id_producto
    }
    axios({
        method: 'POST',
        url: '/carrito/delete',
        data: item
    })
    .then(resp => {
        console.log(resp)
        window.location.href = '/panel/carrito';
    })

}