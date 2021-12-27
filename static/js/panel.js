
//modificacion de datos de perfil
const bnt_perfil = document.getElementById('btn-perfil')

bnt_perfil.addEventListener('click',(e) =>{
    e.preventDefault()
    const form = document.getElementById('perfil-form')

    dato = {
        'nombre':form['nombre'].value,
        'telefono':form['telefono'].value,
        'domicilio':form['domicilio'].value,
        'foto': foto,
        'foto_id': foto_key
    }

    axios({
        method: 'POST',
        url: '/clientes/update',
        data: dato
    }).then(resp => {
        console.log('se envio')
        
    })

})

//subida de foto de perfil
const uploader = document.getElementById('uploader') 
uploader.addEventListener('change', async(e) => {

    //obtengo la pantalla de carga
    pantalla = document.querySelector('.pantalla-carga')
    pantalla.classList.toggle('show')

    //cargamos el archivo
    const file = e.target.files[0];
    await upload_file(file);

    const foto_perfil= document.getElementById('foto_perfil')
    foto_perfil.src = foto

    //se envian los nuevos datos
    dato = {
        'foto' : foto,
        'foto_key': foto_key 
    }

    axios({
        method: 'POST',
        url: '/clientes/update/foto',
        data: dato
    }).then(resp => {
        pantalla.classList.toggle('show')
    })
    
})