
function cloud_fill(){
    document.getElementById("icon").src="/static/icons/cloud-fill.svg";
}
function cloud(){
    document.getElementById("icon").src="/static/icons/cloud.svg";
}
function dark() {
    var state = false;
   var element = document.body;
   element.classList.toggle("dark-mode");
   state =! state;
}
if (state === true){
       document.getElementById("mode").src="/static/icons/moon.svg";
}
if(state === false){
    document.getElementById("mode").src="/static/icons/moon-fill.svg";
}