sidebar_foto = document.querySelector('#sidebar_img')
sidebar_name = document.querySelector('#sidebar_name')



function sidebar_get_cliente(){

    fetch('/panel/test')
    .then(res => res.json())
    .then(resp =>{
        sidebar_foto.src = resp.foto
        sidebar_name.innerHTML = resp.nombre
    })
    .catch(function(){
        console.log('o no')
    })
}



function sidebar_get_vendedor(){
    fetch('/dashboard/get/vendedor')
    .then(res => res.json())
    .then(resp =>{
        sidebar_foto.src = resp.foto
        sidebar_name.innerHTML = resp.nombre
    })
    .catch(function(e){
        console.log('me la pele wey')
        console.log(e)
    })
}