// Genera el objeto qrcode
var qrcode = new QRCode(document.getElementById("qrcode"), {
    width : 200,
    height : 200
});


const user_id =  document.getElementById('user_id').value
const menu_url = document.getElementById('menu_url')


var URLactual = window.location;
var codigo = URLactual.origin + "/menu/" + user_id

menu_url.innerHTML = codigo

qrcode.makeCode(codigo);

//agregando la url al 'ver menu' del formulario
document.getElementById("ver_menu").href = codigo;


// para imprimir el codigo qr
const btn = document.getElementById('btn_qr')

btn.addEventListener('click',function(){
    var ficha = document.getElementById('qrcode');
	var ventimp = window.open(' ', 'popimpr');
	ventimp.document.write( ficha.innerHTML );
	ventimp.document.close();
	ventimp.print( );
	ventimp.close();
})