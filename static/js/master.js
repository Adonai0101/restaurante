

function delete_user(id) {
    let msj = 'Esto eliminara pro completo toda la informacion del usuario, una vez hecho esto no habra vuelta atras'
    let result = window.confirm(msj);


    if (result == true) {
        console.log('eliminando usuario')

        const loading = document.querySelector('#load')
        console.log(loading)
        loading.classList.add('activate')

        dato = {
            'id': id

        }

        axios({
            method: 'POST',
            url: '/master/delete/user',
            data: dato
        }).then(resp => {
            console.log(resp)
            location.reload()
        })
    }

    else {
        console.log('mas te vale perro')
    }

}


function delete_item(id) {
    console.log('eliminando item')
    const loading = document.querySelector('#load')
    console.log(loading)
    loading.classList.add('activate')

    dato = {
        'id': id
    }

    axios({
        method: 'POST',
        url: '/master/user/delete/item',
        data: dato
    }).then(resp => {
        console.log(resp)
        location.reload()
    })

}

function pagar(id) {

    let msj = '¿Estas seguro que quieres pagar un mes mas a este usuario?'
    let result = window.confirm(msj);
    if(result){
        dato = {
            'id': id
        }
    
        axios({
            method: 'POST',
            url: '/master/pago',
            data: dato
        }).then(resp => {
            console.log(resp)
            location.reload()
        })
    }

}

