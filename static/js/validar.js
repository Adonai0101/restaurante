
const test = document.getElementById('test-usuario')
const btn_registro = document.getElementById('btn-registro')
const info = document.getElementById('text-info')

test.addEventListener('keyup',function(e){
    let x = test.value
    let len = x.length
    let ban = true

    if (x.charAt(0) == " " || x.charAt(len-1) == " "){
        desactivar()
        ban = true
    }
    else{
        activar()
        ban = false
    }

    if(ban == false){
        for (var i = 0; i < len; i++) {
            if(x.charAt(i) == " "){
                if( x.charAt(i + 1) == " "){
                    desactivar()
                    break
                }
                else{
                    activar()
                    break
                }
            }
        }
    }
})

function activar(){
    test.style.cssText = 'background-color: white; color: black;'; 
    info.innerHTML = 'Recuerda que el nombre de usuario es el mismo que el de tu negocio'
    info.style.cssText = 'color: lightslategray'; 
    btn_registro.disabled =  false
}

function desactivar(){
    test.style.cssText = 'border: solid red';  
    info.innerHTML = 'Cuidado con los "espacios", no puedes empesar ni terminar con espacios '
    info.style.cssText = 'color: red'; 
    btn_registro.disabled =  true 
}
