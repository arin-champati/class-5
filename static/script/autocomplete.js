currentFocus = -1;

function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
}

function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
    }
}

function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = $(".autocomplete-items");
    for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i]) {
            x[i].parentNode.removeChild(x[i]);
        }
    }  
}

function handleKeyPress(e) {
    var x = document.getElementById("autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
    } 
    else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
    } 
    else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
            /*and simulate a click on the "active" item:*/
            if (x) x[currentFocus].click();
        }
    } 
    else if (e.keyCode == 9) {
        // If the tab key is pressed, close all lists
        closeAllLists()
    }
}

currentEl = null;
request = null;
matchLen = 0;

// bold string returns the html for bolding a substring (case insensitive)
function boldString(str, find) {
    var reg = new RegExp('('+find+')', 'gi');
    return str.replace(reg, '<b>$1</b>');
  }

function handleResponse(response) {   

    closeAllLists();
    try {
        let values = response.values;   
        let input = response.input;

        div = document.createElement("DIV");
        div.setAttribute("id", "autocomplete-list");
        div.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        currentEl.parentNode.appendChild(div);
        /*for each item in the array...*/
        for (let [i, value] of values.entries()) {
            let courseEl = document.createElement("DIV");
            courseEl.setAttribute("id", "item" + i);
            courseEl.setAttribute("class", "autocomplete-item");

            courseEl.innerHTML += boldString(value, input)

            courseEl.innerHTML += "<input type='hidden' value='" + value + "'>";

            courseEl.addEventListener("click", function(e) {
                currentEl.value = this.getElementsByTagName("input")[0].value;

                closeAllLists();
            });

            div.append(courseEl);
        }
    }
    catch (e) {
        console.log("ERROR: " + e);
    }
}


function getCourseResults() {
    currentEl = this;
    let deptNum = this.value;
    matchLen = deptNum.length;
    currentFocus = -1;

    deptNum = deptNum ? encodeURIComponent(deptNum) : "";

    let url = "/courses?deptNum=" + deptNum.toUpperCase();

    if (request != null) request.abort();

    request = $.ajax(
        {
            type: 'GET',
            url: url,
            success: handleResponse
        }
    );
}

function getMajorResults() {
    currentEl = this;
    let major = this.value;
    matchLen = major.length;
    currentFocus = -1;

    major = major ? encodeURIComponent(major) : "";

    let url = "/majors?major=" + major.toLowerCase();

    if (request != null) request.abort();

    request = $.ajax({
        type: "GET",
        url: url,
        success: handleResponse
    })
}

function getYear() {
    currentEl = this;
    let year = this.value;
    matchLen = year.length;
    currentFocus = -1;

    year = year ? encodeURIComponent(year) : "";

    let d = new Date();
    let currentYear = d.getFullYear();
    let yearList = [];
    for (let i = 0; i < 6; i++) {
        let yearStr = String(currentYear + i);
        if (yearStr.includes(year)) {
            yearList.push(yearStr);

        }
    }

    states_dictionary={ 
        "CT":["alex","harry"], 
        "AK":["liza","alex"], 
        "TX":["fred", "harry"]
    };

    handleResponse({'input': year, 'values': yearList});
}

function getCertResults() {
    currentEl = this;
    let cert = this.value;
    matchLen = cert.length;
    currentFocus = -1;

    cert = cert ? encodeURIComponent(cert) : "";

    let url = "/certificates?certificate=" + cert.toLowerCase();

    if (request != null) request.abort();

    request = $.ajax({
        type: "GET",
        url: url,
        success: handleResponse
    })
}

function handleClick() {
    closeAllLists();
}


function setup() {
    $("#favorite").on("input", getCourseResults);
    $("#favorite").on("keydown", handleKeyPress);

    $("#search").on("input", getCourseResults);
    $("#search").on("keydown", handleKeyPress);
    
    $("#major").on("input", getMajorResults);
    $("#major").on("keydown", handleKeyPress);

    $("#year").on("input", getYear);
    $("#year").on("keydown", handleKeyPress);

    // because these are addable and removable, we need to
    // define it for the document
    $(document).on('input', '.likedCourse', getCourseResults);
    $(document).on('keydown', '.likedCourse', handleKeyPress);

    $(document).on('input', '.dislikedCourse', getCourseResults);
    $(document).on('keydown', '.dislikedCourse', handleKeyPress);

    $(document).on('input', '.certificate', getCertResults);
    $(document).on('keydown', '.certificate', handleKeyPress);
    
}

// on ready, setup
// $(setup);
$("document").ready(setup);
document.addEventListener("click", handleClick);
