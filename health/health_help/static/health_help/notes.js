 show();

let addBtn = document.getElementById("addBtn");
addBtn.addEventListener("click", function(e) {
  let addTxt = document.getElementById("addTxt");
  let notes = localStorage.getItem("notes");
  if (notes == null) {
    note_local = [];
  } else {
    note_local = JSON.parse(notes);
  }
  if (addTxt.value === ""){
      alert("Please provide valid input.")
  }
  else{
  note_local.push(addTxt.value);
  localStorage.setItem("notes", JSON.stringify(note_local));
  addTxt.value = "";

  show();
  }
});

function show() {
  let notes = localStorage.getItem("notes");
  if (notes == null) {
    note_local = [];
  } else {
    note_local = JSON.parse(notes);
  }
  let html = "";
  note_local.forEach(function(element, index) {
    html += `
            <div class="mx-auto card" style="width: 50rem;">
                    <div class="card-body">
                        <p class="card-text"> ${element}</p>
                        <button id="${index}"onclick="deleteNote(this.id)" class="btn btn-danger">Delete Note</button>
                    </div>
                </div>`;
  });
  let notesElm = document.getElementById("notes");
  if (note_local.length != 0) {
    notesElm.innerHTML = html;
  } else {
    notesElm.innerHTML = `<h3 class="text-danger fw-bold text-center"> No notes available! </h3>`;
  }
}

function deleteNote(index) {

  let notes = localStorage.getItem("notes");
  if (notes == null) {
    note_local = [];
  } else {
    note_local = JSON.parse(notes);
  }

  note_local.splice(index, 1);
  localStorage.setItem("notes", JSON.stringify(note_local));
  show();
}





//calorie count

var calorie = document.getElementById("calories-doc")
var calorie_requirement = localStorage.getItem("calorie")
if (calorie_requirement === null){
  calorie.innerHTML = "No calorie count available."
}
else
{
  calorie.innerHTML = `Calorie requirement is ${calorie_requirement} Kcal.`
}
