const qr_menu = document.querySelector('#qrcode_menu')
const link_menu = document.querySelector('#link_menu')
var qrcode_menu = new QRCode(qr_menu, {
    width : 250,
    height : 250
});


qrcode_menu.makeCode(link_menu.href);


const qr_pedido = document.querySelector('#qrcode_pedido')
const link_pedido = document.querySelector('#link_pedido')
var qrcode_pedido = new QRCode(qr_pedido, {
    width : 250,
    height : 250
});

qrcode_pedido.makeCode(link_pedido.href);







// para imprimir el codigo qr
const btn = document.getElementById('btn_qr')

btn.addEventListener('click',function(){
	console.log('hey')
    var ficha = document.querySelector('#qrcode_menu');
	var ventimp = window.open(' ', 'popimpr');
	ventimp.document.write( ficha.innerHTML );
	ventimp.document.close();
	ventimp.print( );
	ventimp.close();
})



const btn_link = document.getElementById('btn_qrLink')

btn_link.addEventListener('click',function(){
	console.log('hey')
    var ficha =  document.querySelector('#qrcode_pedido');
	var ventimp = window.open(' ', 'popimpr');
	ventimp.document.write( ficha.innerHTML );
	ventimp.document.close();
	ventimp.print( );
	ventimp.close();
})