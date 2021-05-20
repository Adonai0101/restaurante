
//agregar gregandoi nuevo producto
const add = document.querySelector('#add')

add.addEventListener('click', (event) => {
    event.preventDefault()

    const nombre = document.querySelector('#nombre').value
    const categoria = document.querySelector('#categoria').value
    const precio = document.querySelector('#precio').value
    const ingredientes = document.querySelector('#ingredientes').value

    dato = {
        'nombre': nombre,
        'categoria': categoria,
        'precio': precio,
        'ingredientes': ingredientes,
        'fotos': fotos,
        'publicID':fotos_publicID
    }

    axios({
        method: 'POST',
        url: '/productos/',
        data: dato
    }).then(resp => {
        $('.modal').modal('hide')
        location.reload()
    })
})


//delete one
function deleteOne(id) {
    Swal.fire({
        title: '¿Estas seguro?',
        text: "perderas todo registro de este producto!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, eliminalo!'
    }).then((result) => {
        if (result.isConfirmed) {

            dato = {
                'id': id,
            }

            axios({
                method: 'POST',
                url: '/productos/delete',
                data: dato
            }).then(resp => {
                Swal.fire(
                    'Eliminado!',
                    'tu producto ha sido eliminado.',
                    'success'
                )
                location.reload()
            })

        }
    })


}


//apartado para solo modificar un productos


function deleteImage(id, file, publicID) {
    console.log(file)
    console.log(id)
    console.log(publicID)

    Swal.fire({
        title: '¿Estas seguro?',
        text: "perderas todo registro de este producto!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, eliminalo!'
    }).then((result) => {
        if (result.isConfirmed) {

            dato = {
                'id': id,
                'filename': file,
                'publicID':publicID
            }
            axios({
                method: 'POST',
                url: '/productos/deleteimg',
                data: dato
            }).then(resp => {
                location.reload()
            })

        }
    })

}

function addImg(id){
    dato = {
        'id':id,
        'fotos': fotos,
        'publicID':fotos_publicID
    }

    axios({
        method: 'POST',
        url: '/productos/addimages',
        data: dato
    }).then(resp => {
        location.reload()
    })
}

function update_info(id){
  
    const nombre = document.querySelector('#nombre').value
    const categoria = document.querySelector('#categoria').value
    const precio = document.querySelector('#precio').value
    const ingredientes = document.querySelector('#ingredientes').value

    dato = {
        'id':id,
        'nombre': nombre,
        'categoria': categoria,
        'precio': precio,
        'ingredientes': ingredientes,
    }

    axios({
        method: 'POST',
        url: '/productos/updateinfo',
        data: dato
    }).then(resp => {
        console.log("enviado")
        console.log(id)
    })
}

