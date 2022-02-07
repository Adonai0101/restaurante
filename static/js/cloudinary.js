const imagePreview = document.getElementById('img-preview');
const imageUploader = document.getElementById('img-uploader');
const imageUploadbar = document.getElementById('img-upload-bar');
const miniatura = document.getElementById('miniatura')


const CLOUDINARY_URL = `https://api.cloudinary.com/v1_1/adonai0101/image/upload`
const CLOUDINARY_UPLOAD_PRESET = 'xn5pdxm9';

//para la carga de todas las fotos del sistema

// estos dos arreglos los hago "globales" para que puedan ser leidos desde otro archivo js
var fotos = []
var fotos_publicID = []



/* Funcion definitiva para  siempre subir fotos con ella y no andar haciendo chingaderas*/
function upload_cloudimary(file) {
    // el file tiene que ir como parametro en la funcion
    const formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', CLOUDINARY_UPLOAD_PRESET);

    return axios({
        method: "post",
        url: CLOUDINARY_URL,
        data: formData,
        headers: { "Content-Type": "multipart/form-data" },
    })
        .then(function (response) {
            //handle success
            console.log(response);
            //guardamos los valores en los arreglos
            fotos.push(response.data.secure_url)
            fotos_publicID.push(response.data.public_id)
        })
        .catch(function (response) {
            //handle error
            console.log(response);
        });

}



/*
imageUploader.addEventListener('change', async (e) => {
    // console.log(e);
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', CLOUDINARY_UPLOAD_PRESET);

    if (fotos.length > 4) {

        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'has superado el numero máximo de imagenes permitidas'
        })

    }
    else {
        imageUploadbar.classList.add('bg-primary')
        // Send to cloudianry
        const res = await axios.post(
            CLOUDINARY_URL,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                onUploadProgress(e) {
                    let progress = Math.round((e.loaded * 100.0) / e.total);
                    progress = progress - 3
                    console.log(progress);

                    imageUploadbar.style.width = progress + "%";
                    imageUploadbar.innerHTML = progress
                }
            }
        );
        console.log(res);
        progress = 100

        //guardamos los valores en los arreglos
        fotos.push(res.data.secure_url)
        fotos_publicID.push(res.data.public_id)

        renderMiniatura()
        console.log(fotos)
        console.log(fotos_publicID)
        imageUploadbar.innerHTML = progress
        imageUploadbar.style.width = progress + "%";
        imageUploadbar.classList.add('bg-success')
    }

});
*/


function renderMiniatura() {
    miniatura.innerHTML = ''
    fotos.forEach(element => {
        miniatura.innerHTML += `
         <img src="${element}">
        `
    });
}


//-----------------------------


//para la foto de perfil

/*

const perfil_uploader = document.getElementById('user_file')
const foto_perfil = document.getElementById('foto_perfil')
const foto_bar = document.getElementById('file_bar')
var perfil_foto = ''
var perfil_foto_key = ''

perfil_uploader.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', CLOUDINARY_UPLOAD_PRESET);

    // Send to cloudianry
    const res = await axios.post(
        CLOUDINARY_URL,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            onUploadProgress(e) {
                console.log("..." + e)
                let progress = Math.round((e.loaded * 100.0) / e.total);
                progress = progress - 2
                console.log(progress);

                foto_bar.style.width = progress + "%";
                foto_bar.innerHTML = progress
            }
        }
    );

    console.log(res)
    perfil_foto = res.data.secure_url
    perfil_foto_key = res.data.public_id

    foto_perfil.src = perfil_foto

    //para el progressbar
    progress = 100
    foto_bar.style.width = progress + "%";
    foto_bar.innerHTML = progress

    dato = {
        'foto': perfil_foto,
        'foto_key': perfil_foto_key
    }

    axios({
        method: 'POST',
        url: '/usuarios/update_foto',
        data: dato
    }).then(resp => {
        console.log(resp)
    })

})

*/