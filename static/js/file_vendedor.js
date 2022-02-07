
const CLOUDINARY_URL = `https://api.cloudinary.com/v1_1/adonai0101/image/upload`
const CLOUDINARY_UPLOAD_PRESET = 'xn5pdxm9';

//para la foto de perfil

const perfil_uploader = document.getElementById('user_file')
const foto_perfil = document.getElementById('foto_perfil')

var perfil_foto = ''
var perfil_foto_key = ''

perfil_uploader.addEventListener('change', async (e) => {

    //obtengo la pantalla de carga
    pantalla = document.querySelector('.pantalla-carga')
    pantalla.classList.toggle('show')

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
            }
        }
    );

    perfil_foto = res.data.secure_url
    perfil_foto_key = res.data.public_id

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
        foto_perfil.src = perfil_foto
        pantalla.classList.toggle('show')
    })

})



const btn_active = document.querySelector('#active_file')
btn_active.addEventListener('click', (e) => {
    e.preventDefault()
    perfil_uploader.click()
})