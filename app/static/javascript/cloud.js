const file = document.getElementById('file')
const icon = document.getElementById('icon')
file.addEventListener('change',(Event)=>{
    icon.innerHTML = Event.target.files[0].name
    console.log(file_label)
})
