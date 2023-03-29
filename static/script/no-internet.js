window.addEventListener("load", function (){
    if (navigator.onLine){
            document.getElementById("for-no").innerHTML = "";
    }else{
        changeVisibility();
    }
})

window.addEventListener("online", function (){
    document.getElementById("for-no").innerHTML = "";
})
window.addEventListener("offline", function (){
    changeVisibility();
})

function changeVisibility() {
    document.getElementById("for-no").innerHTML = "<br><h3 align='center' id='warning'>دسترسی به اینترنت ممکن نیست</h3><br>";
}