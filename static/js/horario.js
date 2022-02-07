var horario = {
    'Lunes': '',
    'Martes':'',
    'Miercoles':'',
    'Jueves':'',
    'Viernes':'',
    'Sabado':'',
    'Doming':'',
}

const form_horario =  document.querySelector('#horario')

const btn_horario =  document.querySelector('#btn-horario')
btn_horario.addEventListener('click',(e)=>{
    e.preventDefault();
    update_horario()
})

function update_horario(){

    var horario = {
        'Lunes': [form_horario['Lunes_inicio'].value , form_horario['Lunes_fin'].value],
        'Martes':[form_horario['Martes_inicio'].value , form_horario['Martes_fin'].value],
        'Miercoles':[form_horario['Miercoles_inicio'].value , form_horario['Miercoles_fin'].value],
        'Jueves':[form_horario['Jueves_inicio'].value , form_horario['Jueves_fin'].value],
        'Viernes':[form_horario['Viernes_inicio'].value , form_horario['Viernes_fin'].value],
        'Sabado':[form_horario['Sabado_inicio'].value , form_horario['Sabado_fin'].value],
        'Domingo':[form_horario['Domingo_inicio'].value , form_horario['Domingo_fin'].value]
    }

    let ban = true
    for(const i in horario){

        if(horario[i][0] == "" && horario[i][1] == ""){
            console.log('vacios')
        }
        else{

            if(horario[i][0] >= horario[i][1]){
                console.log('cagaste')
                show_alert()
                ban = false
                break
            } 
        }
    }

    if (ban){
            // enviamos el post
            console.log('aperro')
            axios({
                method: 'POST',
                url: '/usuarios/update/horario',
                data: horario
            })
            .then(resp => {
                console.log(resp)
                //obtengo la pantalla de carga
                pantalla = document.querySelector('.pantalla-carga')
                pantalla.classList.toggle('show')
            })
            .then(x => {
                console.log('se envio')
                window.location.href = '/dashboard/perfil';
            })
    }

    console.log(horario)
}


// cosas raras xd

function cerrado(id){

    let id_inicio = id + '_inicio'
    let id_fin = id + '_fin'
    console.log('closed')
    form_horario[id_inicio].value = "-adhawj:dwads--"

    //pintamos los forms    
    form_horario[id_inicio].classList.toggle('border-danger')
    form_horario[id_fin].classList.toggle('border-danger')

    // Cambiamos el valor del horario solo para  saber que esta cerrado
    form_horario[id_inicio].value = "cerrad:dwads--"
    form_horario[id_fin].value = "-cerrado:dwads--"

    //bloquear los campos de texto
}

