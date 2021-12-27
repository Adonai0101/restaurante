sidebar_foto = document.querySelector('#sidebar_img')
sidebar_name = document.querySelector('#sidebar_name')


fetch('/panel/test')
.then(res => res.json())
.then(resp =>{

    sidebar_foto.src = resp.foto
    sidebar_name.innerHTML = resp.nombre
})


.catch(function(){
    console.log('o no')
})