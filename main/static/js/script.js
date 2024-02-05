


function login(){
   var obj_data ={
   email:document.getElementById('email').value,
   password:document.getElementById('password').value
}
console.log(obj_data)

       var settings = {
"url": "http://localhost:5000/login",
"method": "POST",
"timeout": 0,
"headers": {
"Content-Type": "application/json"
},
"data": JSON.stringify(obj_data),
};

$.ajax(settings).done(function (response) {
console.log(response)

if(response.status == "success")
{
setTimeout(function() {
window.location.href = "/home";
}, 1500);
success('success',response.message)
}
else{
success('error', response.message)
}
});
}





