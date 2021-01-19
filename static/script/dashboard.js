request = null;

// prepopulate the suggested courses
function handleSuggestions(response) {
    // clear the contents from before
    $('#courseHolder').empty();

    // Get suggestions
    suggestions = response;

    $('#courseHolderName').text('Suggestions')

    for ([i, deptnum] of suggestions.entries()) {
        let div = document.createElement('div');
        div.className = 'row';

        i++
        
        div.innerHTML = `
            <label id="suggestion-label${i}" for="suggestion${i}">Course #${i}:</label>
            <div class="input-group mb-3">
                <input class="form-control profile-input suggestion course" type="text" id="suggestion${i}" name="course${i}" value="${deptnum}" readonly autocomplete="off">
            <span class="input-group-btn">
                <button class="btn btn-primary remove-button" id="suggRemove${i}" title="Dislike this suggestion" onclick="removeSuggestion(this)" type="button"><span class="glyphicon glyphicon-remove" aria-hidden="true">
                </span></button>
            </span>
            </div>
        `  ;

        document.getElementById('courseHolder').appendChild(div);
      }
    getFirstDetails();
  }
  function populateSuggestions() {
    let url = "/suggestions"

    if (request != null) request.abort();

    request = $.ajax(
        {
            type: 'GET',
            url: url,
            success: handleSuggestions
        }
    );
   
}

function handleSuggestionResponse(response)
{
    // append new suggestion to bottom
    let deptNum = response

    if (deptNum != '') 
    {
        let div = document.createElement('div');
        div.className = 'row';
        
        div.innerHTML =`
            <label id="suggestion-label${maxSuggestions}" for="suggestion${maxSuggestions}">Course #${maxSuggestions}:</label>
            <div class="input-group mb-3">
                <input class="form-control profile-input suggestion course" type="text" id="suggestion${maxSuggestions}" name="course${maxSuggestions}" value="${deptNum}" readonly autocomplete="off">
            <span class="input-group-btn">
                <button class="btn btn-primary remove-button" id="suggRemove${maxSuggestions}" title="Dislike this suggestion" onclick="removeSuggestion(this)" type="button"><span class="glyphicon glyphicon-remove" aria-hidden="true">
                </span></button>
            </span>
            </div>
            `   ;

        document.getElementById('courseHolder').appendChild(div);

    }

    // after request is handled, reset click response
    var i = 1;
    $('#courseHolder > div').each(function() {
        if (i > 0) {
            $(this).find('button').each(function() {
                $this = $(this);
                $(this).attr('onclick', 'removeSuggestion(this)');
            })
        }
        i++;
    });
    $(".course").on("click", getDetails);
}



// disliked suggestion passed in event property
function refreshSuggestions(deptNum)
{
    let url = '/refresh?';

    // pass index of disliked suggestion
    if (deptNum != '') {
        deptNum = encodeURIComponent(deptNum);
        url += '&disliked_sugg=' + deptNum;
    }
    
    
    if (request != null)
        request.abort();
    
    request = $.ajax(
        {
            type: 'GET',
            url: url,
            success: handleSuggestionResponse
        }
    );
}

// ------------------------------------------------------------------

function removeSuggestion(input) {

    const labelLength = maxSuggestions;

    // for each suggestion, turn off click
    let index = input.id;
    index = index.substring(labelLength);  // save index of disliked suggestion

    // get deptNum from corresponding input element
    let deptNum = $('#suggestion' + index).val();

    document.getElementById('courseHolder').removeChild(input.parentNode.parentNode.parentNode);

    let i = 1
    // for each suggestion
    $('#courseHolder > div').each(function() {
        if (i >= index && i <= maxSuggestions) {
            // for each label, change the label text and id
            $(this).find('label').each(function() {
                $(this).attr('id', 'suggestion-label' + i);
                $('#suggestion-label' + i).text('Course #' + i + ':');
            })

            // for each input, change the input id and name
            $(this).find('input').each(function() {
                $(this).attr('id', 'suggestion' + i);
                $(this).attr('name', 'course' + i);
            })
            

            // for each button, change the button id
            $(this).find('button').each(function() {
                $(this).attr('id', 'suggRemove' + i);

                // remove click signal response before request is handled
                $(this).attr('onclick', '');
            })
        }
        i++;
    });

    // tell user to refresh the page if we have only 1 element that we deleted
    if (i == 1) {
        let div = document.createElement('div');

        div.innerHTML = '<p>Refresh the page for more suggestions!</p>'

        document.getElementById('courseHolder').appendChild(div);
    }

    // grab new suggestion (if any remaining in cache) and append to bottom 
    refreshSuggestions(deptNum);
  }

// ------------------------------------------------------------------

let request_courses = null

// displays the first detail in the course list as the info bar
function getFirstDetails() {
    let currentEl = document.getElementsByName("course1")[0];
    if (currentEl) {
        let deptNum = currentEl.value;

        matchLen = deptNum.length;
        currentFocus = -1;

        deptNum = deptNum ? encodeURIComponent(deptNum) : "";

        let url = "/course-info?deptNum=" + deptNum.toUpperCase();

        if (request_courses != null) request_courses.abort();

        request_courses = $.ajax(
            {
                type: 'GET',
                url: url,
                success: handleCourseResponse
            }
        );
    }
}

// displays the current course in the info section
function getDetails() {
    currentEl = this;
    if (currentEl) {
        let deptNum = this.value;

        // if deptnum is null, we know that we have a link from the description page
        if ((deptNum == null | deptNum == '') && ($(this).prop("tagName") == 'A')) {
            currentEl = this;
            deptNum = currentEl.innerHTML;
        }

        // if deptnum is STILL null, we are searching with the search bar, and we need to get the value
        if (deptNum == null) {
            currentEl = document.getElementById("search")
            deptNum = currentEl.value
        }

        matchLen = deptNum.length;

        currentFocus = -1;

        deptNum = deptNum ? encodeURIComponent(deptNum) : "";

        let url = "/course-info?deptNum=" + deptNum.toUpperCase();

        if (request_courses != null) request_courses.abort();

        request_courses = $.ajax(
            {
                type: 'GET',
                url: url,
                success: handleCourseResponse
            }
        );
    }
}


function handleFilterResponse(response) {
    // clear the contents from before
    $('#courseHolder').empty();
    
    if (typeof response != 'object') {
        populateSuggestions();
    }
    else {
        courses = response.courses;
        let text = "";
        if (response && response.filter == 'mostliked') {
            text = 'Most Liked';
        }
        else if (response && response.filter == 'mostdisliked') {
            text = 'Most Disliked';
        }
        else if (response && response.filter == 'favorites') {
            text = 'Top Fifth';
        }

    n = Math.min(courses.length, maxCourses)

        // change title name
        $('#courseHolderName').text(text);

        for ([i, deptnum] of courses.entries()) {
            let div = document.createElement('div');
            div.className = 'row';

            i++
        
            div.innerHTML = `
            <label id="suggestion-label${i}" for="suggestion${i}">Course #${i}:</label>
            <div class="input-group mb-3 non-removable">
                <input class="form-control profile-input suggestion course" type="text" id="suggestion${i}" name="course${i}" value="${deptnum}" readonly autocomplete="off">
            </span>
            </div>
        `   ;

            document.getElementById('courseHolder').appendChild(div);
        }
      }

    // reinstantiate the onclick behavior for the course class
      $(".course").on("click", getDetails);

    //   also display the first details
      getFirstDetails()

}

function getFilter() {
    let filter = this.id;
    filter = filter ? encodeURIComponent(filter) : "";
    let url = '/filters?type=' + filter;

    if (request != null) request.abort();

    request = $.ajax(
        {
            type: 'GET',
            url: url,
            success: handleFilterResponse
        }
    );
}

function handleCourseResponse(response) {
    try {
        course_info = response;

        if (response != null) {
            $("#informationHolder").empty();

            // Display crosslisting and title
            let div = document.createElement('div');
            div.className = 'row';
            div.innerHTML = '<h4 id="crosslisting">' + course_info.course_details.deptnum + '</h4>';
            div.innerHTML += '<h4 id="title">' + course_info.course_details.title + '</h4>';
            document.getElementById('informationHolder').appendChild(div);

            // Display course stats
            div = document.createElement('div');
            div.setAttribute("id", "statistics");
            div.className = 'row';

            let total = course_info.course_numbers.num_liked + course_info.course_numbers.num_disliked;
            if (total == 0) {
                percentageLikes = 0;
                percentageDislikes = 0;
            }
            else {
                percentageLikes = ((course_info.course_numbers.num_liked / total) * 100).toFixed(0);
                percentageDislikes = ((course_info.course_numbers.num_disliked / total) * 100).toFixed(0);
            }


            // div.innerHTML = '<b>Statistics:</b>'
            // div.innerHTML += '<br>'

            // Create a div for the thumb icons
            thumbs = document.createElement('div');
            thumbs.setAttribute("id", "thumbs");
            
            thumbs.innerHTML += '<span title="Number of users who have liked this course" id="thumbs-up" ><i class="far fa-thumbs-up" aria-hidden="true"></i>' + ' ' + course_info.course_numbers.num_liked + '</span>'
            thumbs.innerHTML += '<span title="Number of users who have disliked this course" id="thumbs-down" ><i class="far fa-thumbs-down" aria-hidden="true"></i>' + ' ' + course_info.course_numbers.num_disliked + '</span>'

            div.append(thumbs);

            // Create a div for the bar graph

            bar = document.createElement('div');
            bar.setAttribute("id", "bar");

            // create div for percentage info hover
            bar.innerHTML += '<div id="percentage-info">' + percentageLikes + '%' + '&nbsp/&nbsp' + percentageDislikes + '%' + '</div>'
            bar.innerHTML += '<div id="liked">' + course_info.course_numbers.num_liked + '</div>';
            bar.innerHTML += '<div id="disliked">' + course_info.course_numbers.num_disliked + '</div>'

            div.append(bar);

            // if ($('#courseHolderName').text() == "Top Fifth Courses") {
            //     fifth = document.createElement('div');
            //     fifth.innerHTML = '<p class="subheading"><b>Number of 5th Course Favorites:</b></p>';
            //     fifth.innerHTML += course_info.course_numbers.num_fifth
            //     div.append(fifth);
            // }

            if (course_info.course_numbers.num_fifth > 0) {
                fifth = document.createElement('div');
                fifth.innerHTML = '<p title="Number of users with this course as their favorite fifth course" id="fav-fifth-likes" class="subheading"><b>5th Course <i class="far fa-heart"></i>\'s: </b>' + course_info.course_numbers.num_fifth + '</p>';
                // fifth.innerHTML += course_info.course_numbers.num_fifth 
                div.append(fifth);
            }

            document.getElementById('informationHolder').appendChild(div);

            // if there are no reviews, give both equal widths
            if (percentageLikes == 0 && percentageDislikes == 0){
                percentageLikes = 50;
                percentageDislikes = 50;
            }

            // if one is zero, still show some of it
            if (percentageLikes < 5) {
                percentageLikes = 5;
                percentageDislikes = 95;
            }

            if (percentageDislikes < 5) {
                percentageLikes = 95;
                percentageDislikes = 5;
            }

            document.getElementById('liked').style.width=percentageLikes.toString()+"%";
            document.getElementById('disliked').style.width=percentageDislikes.toString()+"%";


            // Display description
            div = document.createElement('div');
            div.setAttribute("id", "description");
            div.className = 'row';
            div.innerHTML = '<p class="subheading" id="last-offered"><b>Last Offered: </b></p>' + course_info.course_details.term;

            div.innerHTML += '<p class="subheading"><b>Description:</b></p>';
            div.innerHTML += course_info.course_details.description;
            document.getElementById('informationHolder').appendChild(div);

            div.innerHTML += '<p class="subheading"><b>Department: </b></p>' + course_info.course_details.department_name;

            
            // Display professors
            div = document.createElement('div');
            div.setAttribute("id", "professors");
            div.className = 'row';

            if (course_info.course_profs.length > 1) {
                div.innerHTML = '<p class="subheading"><b>Professors:</b></p>';
            }
            else if (course_info.course_profs.length == 1) {
                div.innerHTML = '<p class="subheading"><b>Professor:</b></p>';
            }

            for (prof of course_info.course_profs) {
                // we need to insert %20 in place of the spaces for princeton courses
                url_prof = prof.split(' ');
                url_prof = [url_prof[0], url_prof[url_prof.length - 1]];
                url_prof = url_prof.join('%20').toLowerCase()

                link = 'https://www.princetoncourses.com/?search=' + url_prof + '&semester=' + course_info.course_details.term_code + '&sort=commonName';
                
                div.innerHTML += '<a target="_blank" href="' + link +'">' + prof + '</a>';
                div.innerHTML += '<br>';
            }

            document.getElementById('informationHolder').appendChild(div);


            // Display what users also liked
            div = document.createElement('div');
            div.className = 'row';

            if (course_info.course_edges.length > 0) {
                div.innerHTML = '<p class="subheading"><b>Users also liked:</b></p>';
            }

            for ([i, deptnum] of course_info.course_edges.entries()) {
                i++
                // div.innerHTML += '<a class="course"">' + deptnum + '</a>';
                div.innerHTML += '<a class="course"">' + deptnum + '</a>';
                div.innerHTML += '<br>';
                document.getElementById('informationHolder').appendChild(div);
            }

            $(".course").on("click", getDetails);

            // Display course links
            div = document.createElement('div');
            div.setAttribute("id", "links");
            div.className = 'row';

            div.innerHTML = '<p class="subheading"><b>External Links:</b></p>';

            // princeton courses link
            deptnum = course_info.course_details.deptnum
            
            url_deptnum = deptnum.split(' ').join('%20').toLowerCase();
            link = 'https://www.princetoncourses.com/?search=' + url_deptnum + '&semester=' + course_info.course_details.term_code + '&sort=commonName'
            
            div.innerHTML += '<a target="_blank" href="' + link +'">' + 'Princeton Courses' + '</a>';
            div.innerHTML += '<br>';

            // registrar info link
            link = 'https://registrar.princeton.edu/course-offerings/course-details?term=' + course_info.course_details.term_code + '&courseid=' + course_info.course_details.courseid
            div.innerHTML += '<a target="_blank" href="' + link +'">' + 'Registrar' + '</a>';
            div.innerHTML += '<br>';

            // evaluations link
            link = 'https://registrarapps.princeton.edu/course-evaluation?courseinfo=' + course_info.course_details.courseid + '&terminfo=' + course_info.course_details.term_code
            div.innerHTML += '<a target="_blank" href="' + link +'">' + 'Evaluations' + '</a>';
            div.innerHTML += '<br>';

            document.getElementById('informationHolder').appendChild(div);
        }

    }
    catch (e) {
        console.log("ERROR: " + e);
    }

}

// ------------------------------------------------------------------

function setup()
{
    // populate suggestions on first load
    populateSuggestions();
    $(".course").on("click", getDetails);
    $(".filters").on("click", getFilter);
    // $("#search").on("keydown", function(e) {
    //     var key = e.which;
    //     // Enter
    //     if (key == 13) {
    //         getDetails(this);
    //     }
    // });
    $(document).on('click', '.autocomplete-item', getDetails);
}

$(setup);
