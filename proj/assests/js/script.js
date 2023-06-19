function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}
function viynalmenu() {
  document.getElementById("myDropdownv").classList.toggle("show");
}
function cassestsmenu() {
  document.getElementById("myDropdownc").classList.toggle("show");
}
function postermenu() {
  document.getElementById("myDropdownp").classList.toggle("show");
}

function showmenu() {
  document.getElementById("mob-menu").classList.toggle("show");
}
function searchmenu() {
  document.getElementById("searchmenu").classList.toggle("show");
}
function searchmobmenu() {
  document.getElementById("searchmobmenu").classList.toggle("show");
}
function filterdrop() {
  document.getElementById("filtertool").classList.toggle("show");
}
function sortdrop() {
  
  document.getElementById("sorttool").classList.toggle("show");
}
function sortmobdrop() {
  document.getElementById("sortmobtl").classList.toggle("show");
}
function filtermobdrop() {
  document.getElementById("filtermobtl").classList.toggle("show");
}
// Close the dropdown menu if the user clicks outside of it
// window.onclick = function(event) {
//   if (!event.target.matches('.dropbtn')) {
//     var dropdowns = document.getElementsByClassName("dropdown-content");
    
//     var i;
//     for (i = 0; i < dropdowns.length; i++) {
//       var openDropdown = dropdowns[i];
//       if (openDropdown.classList.contains('show')) {
//         openDropdown.classList.remove('show');
//       }
//     }
   
//   }
// }
function changeImage(imageSrc) {
  var mainDiv = document.getElementById('main-img');
  mainDiv.innerHTML = '<img src="' + imageSrc + '" alt="Selected Image">';
}

