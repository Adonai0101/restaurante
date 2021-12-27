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













// por lo pronto estas son funciones de shir :CC

function get_producto(id){
    let url = '/panel/api/producto/' 
    url = url + id
    axios.get(url)
    .then(resp => {
        let datos = resp.data
        localStorage.setItem('producto',JSON.stringify(datos))   
    }).
    catch(e => {
        console.log('algo salio mal')
    })
    
}


function get_vendedor(id){
    let url = '/panel/api/vendedor/' 
    url = url + id
    console.log(url)
    axios.get(url)
    .then(resp => {
        let datos = resp.data
        localStorage.setItem('vendedor',JSON.stringify(datos))   
    }).
    catch(e => {
        console.log('algo salio mal')
    })
    
}


function get_cliente(){
    axios.get('/panel/api/usuario')
    .then(resp => {
        let datos = resp.data
        localStorage.setItem('cliente',JSON.stringify(datos))
        // esto cambiarlo en el futuro
        //window.location.href = '/panel/orden'   
    }).
    catch(e => {
        console.log('algo salio mal')
    })
}


async function get_storage_vendedor(){
    let data = await JSON.parse(localStorage.getItem('producto'));
    return data;
}


