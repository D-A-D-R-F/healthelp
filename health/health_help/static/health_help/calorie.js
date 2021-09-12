var form = document.getElementById("calorie-form");
    form.onsubmit  = function counter () {
    var weight = document.getElementById("weight-inp").value;
    var gender = document.getElementById("gender").value;
    var height = document.getElementById("height").value;
    var age = document.getElementById("age").value;
    var activity = document.getElementById("activity").value;

    if (gender === "male"){
        var formula_men = 10 * weight + 6.25 * height - 5* age + 5
        var calorie_men = 0
        if (activity === "sedentary"){
            calorie_men = formula_men * 1.2
        }
        else if (activity === "light"){
            calorie_men = formula_men * 1.375
        }
        else if (activity === "moderate"){
            calorie_men = formula_men * 1.55
        }
        else if (activity === "very"){
            calorie_men = formula_men * 1.725
        }

        store_men = localStorage.setItem("calorie" , calorie_men)
    }
    else if (gender === "female"){
        var formula_women = 10 * weight + 6.25 * height - 5* age - 161
        var calorie_women = 0
        if (activity === "sedentary"){
            calorie_women = formula_women * 1.2
        }
        else if (activity === "light"){
            calorie_women = formula_women * 1.375
        }
        else if (activity === "moderate"){
            calorie_women = formula_women * 1.55
        }
        else if (activity === "very"){
            calorie_women = formula_women * 1.725
        }
        store_women = localStorage.setItem("calorie" , calorie_women)
    }  
}

var set_calorie = document.getElementById("calorie-intake")
if(localStorage.getItem("calorie") !== null){

set_calorie.innerHTML = `Your daily calorie intake should be ${localStorage.getItem("calorie")}`

}
else{
    set_calorie.innerHTML = ""

}

var cal = document.getElementById("cal").innerHTML
alert(cal)