


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

if(response.status == "success"){
   console.log(response.staff_status)
   if (response.staff_status == "Administrator") {
      sessionStorage.setItem('userData', JSON.stringify(response));
      setTimeout(function() {
         window.location.href = "/home";
      }, 1500);
      success('success', response.message);
   } else {
      sessionStorage.setItem('userData', JSON.stringify(response));
      setTimeout(function() {
         window.location.href = "/user";
      }, 1500);
      success('success', response.message);
   }
 } else{
success('error', response.message)
}
});
}

document.addEventListener('DOMContentLoaded', function() {
   var userDataString = sessionStorage.getItem('userData');
   if (userDataString) {
      var userData = JSON.parse(userDataString);
      var username = userData.name;
      var staffStatus = userData.staff_status;
      document.getElementById('profile_name').innerText = username;
      document.getElementById('profile_status').innerText = staffStatus;
   } else {
      // Handle the case where userData is not found in sessionStorage
   }
})

function logout() {
   fetch('/logout')
       .then(response => {
           if (response.headers.get('Clear-Session-Storage') === 'true') {
               sessionStorage.clear();  // Clear session storage
               // Redirect to the login page or perform other actions
               window.location.href = '/';  // Example redirect
           }
       })
       .catch(error => {
           console.error('Logout error:', error);
           // Handle logout error
       });
}


