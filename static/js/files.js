
const CLOUDINARY_URL = `https://api.cloudinary.com/v1_1/adonai0101/image/upload`;
const CLOUDINARY_UPLOAD_PRESET = 'xn5pdxm9';

var foto = ''
var foto_key = ''

async function  upload_file(file) {
    console.log('subida de archivos')

    //const file = e.target.files[0];
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
                // inicar animacion
            }
        }
    );

    // terminar animacion

    foto = res.data.secure_url
    foto_key = res.data.public_id

    console.log(foto)
    console.log(foto_key)

}