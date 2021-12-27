var datos_restaurantes = []

var datos_productos = []

function get_productos(){
    datos_productos = []
    axios.get('/panel/api/productos')
        .then(resp => {
            let datos = resp.data.datos
            for(let x in datos){
                datos_productos.push(datos[x])
            }
        })
        .catch(e =>{
            console.log('algo salio mal')
        })
}

function filtro_productos(){
    cont_buscador.innerHTML = ''

    const texto = buscador.value.toLowerCase();

    for (let x of datos_productos) {

        let nombre = x['nombre'].toLowerCase();
        let categoria = x['categoria'].toLowerCase();
        
        if (nombre.indexOf(texto) !== -1 || categoria.indexOf(texto) !== -1){
            cont_buscador.innerHTML += `
            <a href="/panel/producto/${x.id}">
                <div class="card">
                    <img class="card-img" src="${x.fotos[0]}" alt="">
                    <p class="card-title">${x.nombre}</p>
                </div>
            </a>
        `
        }
    }

    if (cont_buscador.innerHTML == '') {
        cont_buscador.innerHTML = `
            <h1 class="mb">☹</h1>
        `
    }

    if (texto == '') {
        cont_buscador.innerHTML = ''
    }
}

function render_restaurantes() {
    const render_rest = document.querySelector('#render_rest')
    datos_restaurantes = []
    axios.get('/panel/api/restaurantes')
        .then(resp => {
            let datos = resp.data.datos
            for (let x in datos) {
                datos_restaurantes.push(datos[x])

                render_rest.innerHTML += `
                <a href="/panel/restaurante/${datos[x].id}">
                    <div class="card">
                        <img class="card-img" src="${datos[x].foto}" alt="">
                        <p class="card-title">${datos[x].nombre}</p>
                    </div>
                </a>
            `
            }
        }).
        catch(e => {
            console.log('algo salio mal')
        })
}

function filtro_restaurantes(){
    cont_buscador.innerHTML = ''

    const texto = buscador.value.toLowerCase();

    for (let x of datos_restaurantes) {

        let nombre = x['nombre'].toLowerCase();
        
        if (nombre.indexOf(texto) !== -1){
            cont_buscador.innerHTML += `
            <a href="/restaurante/">
                <div class="card">
                    <img class="card-img" src="${x.foto}" alt="">
                    <p class="card-title">${x.nombre}</p>
                </div>
            </a>
        `
        }
    }

    if (cont_buscador.innerHTML == '') {
        cont_buscador.innerHTML = `
            <h1 class="mb">☹</h1>
        `
    }

    if (texto == '') {
        cont_buscador.innerHTML = ''
    }
}
