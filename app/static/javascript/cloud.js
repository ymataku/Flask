const file = document.getElementById('file')
const icon = document.getElementById('icon')
// const file_label = document.getElementById('file_label') 
file.addEventListener('change',(Event)=>{
    // icon.style.display = "none";
    icon.innerHTML = Event.target.files[0].name
    // file_label.textContent = Event.target.files[0].name
    console.log(file_label)
})
