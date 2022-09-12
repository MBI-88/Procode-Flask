'use strict'
let placeholder = document.getElementsByClassName('input-data')
for (let place of placeholder){
    if (place.id == 'name') {
        place.setAttribute('placeholder','Name')}
    else{
        place.setAttribute('placeholder','Password')
    }
}
 
document.addEventListener('click',function(event){
     if (event.target.className == 'flash-message'){
        event.target.hidden = true
     }
    let ul_error = document.getElementsByClassName('form-errors')
    for (let elem of ul_error){
        if (elem) {
            elem.hidden = true
        }
    }
    return 
},false)
