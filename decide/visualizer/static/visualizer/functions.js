

function cambiarModo(checkBox){
    var cuerpoweb = document.body;
    if(checkBox){
        cuerpoweb.classList.toggle("oscuro");
    }
    else if(!checkBox){
        cuerpoweb.classList.toggle("claro");
    }
}
