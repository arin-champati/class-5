//==================================================================
// profile.js
// Authors: Arin Champati & Chaz Bethel-Brescia
//==================================================================

// populate the disliked suggestions
// populate the disliked suggestions
function populateDislikedSuggestions() {

    // If there are no disliked suggestions, say a nice message and hide the button
    if (disliked_suggestions.length == 0) {
        const para = document.createElement('p');
        para.setAttribute('id', 'suggestion-message')
        // div.className = 'certificate-title';
        para.innerHTML = `You have no disliked suggestions :&nbsp)`
        document.getElementById('dislikedSuggestionHolder').appendChild(para);

        document.getElementById('clear-all').style.display = 'none';
    }

    // Otherwise we display the button
    else {
      document.getElementById('clear-all').style.display = 'inline-table';
    }


    // create a dummy input for the form to detect changes to the disliked suggestions
    createDummyInput('dislikedSuggestionHolder')

    // for each disliked suggestion, populate the list
    for ([i, course] of disliked_suggestions.entries()) {
        const div = document.createElement('div');
        div.className = 'row';

        i++
        
        div.innerHTML = `
        <div class="autocomplete">
            <label id="disliked-suggestion-label${i}" for="disliked_suggestions${i}">Disliked Suggestion #${i}:</label>
            <div class="input-group mb-3">
                <input class="form-control profile-input disliked-suggestion" type="text" id="disliked-suggestion${i}" name="disliked-suggestion${i}"value="${course}" readonly autocomplete="off">
                <span class="input-group-btn">
                    <button class="btn btn-primary remove-button"  title="Remove this disliked suggestion" onclick='removeDislikedSuggestion(this)' type="button"><span class="glyphicon glyphicon-remove" aria-hidden="true">
                </span></button>
                </span>
            </div>
            </div>
        `  ;
        document.getElementById('dislikedSuggestionHolder').appendChild(div);
    }
}

// ------------------------------------------------------------------

function removeDislikedSuggestion(input) {
    // the total is subtracted by two because we take into account the extra dummy input and we are removing one
    let total = $("#dislikedSuggestionHolder > div").length - 2;


    document.getElementById('dislikedSuggestionHolder').removeChild(input.parentNode.parentNode.parentNode.parentNode);
    var i = 0, name, $this;

    // for each liked course
    $('#dislikedSuggestionHolder > div').each(function() {
    if (i > 0) {
        // for each label, change the label text and id
        $(this).find('label').each(function() {
        $this = $(this);

        // dont change the dummy label
        if (!isDummy($(this).attr('id'))) {
            $(this).attr('id', 'disliked-suggestion-label' + i);
            $('#disliked-suggestion-label' + i).text('Disliked Suggestion #' + i + ':');
        }
        })

        // for each input, change the input id
        $(this).find('input').each(function() {
            $this = $(this);

            // dont change the dummy input
            if (!isDummy($(this).attr('id'))) {
                $(this).attr('id', 'disliked-suggestion' + i);
            }   
        })
    }
    i++;
    });


    // display a message if we have nothing in the holder
    if (total == 0) {
        const para = document.createElement('p');
        para.setAttribute('id', 'suggestion-message')
        para.innerHTML = 'You have no disliked suggestions :&nbsp)';
        para.innerHTML += '<br>'
        para.innerHTML += 'Remember to save your changes!';
        document.getElementById('dislikedSuggestionHolder').appendChild(para);
    }

    // if we reach 0 items, dont show the clear all button
    if (total == 0) {
        document.getElementById('clear-all').style.display = 'none';
      }
      
    dummyInputSignal(input.parentNode.parentNode)
}

// ------------------------------------------------------------------

// clear all disliked suggestions
function clearDislikedSuggestions(input) {

    // empty disliked suggestions
    $('#dislikedSuggestionHolder').empty();

    document.getElementById('clear-all').style.display = 'none';

    // document.getElementById('dislikedSuggestionHolder').removeChild(input.parentNode.parentNode.parentNode.parentNode);

    const para = document.createElement('p');
    para.setAttribute('id', 'suggestion-message')
    // div.className = 'certificate-title';
    para.innerHTML = 'You have no disliked suggestions :&nbsp)';
    para.innerHTML += '<br>'
    para.innerHTML += 'Remember to save your changes!';
    document.getElementById('dislikedSuggestionHolder').appendChild(para);

    dummyInputSignal(null)
}

// ------------------------------------------------------------------

// add a certificate after prepopulating
function addCertificate() {
    const div = document.createElement('div');
//   max_certificates = max_preference;
    div.className = 'row';

    // get the total number of certificates being shown,
    // get the id of the last inputted course
    let total = $("#certificateHolder > div").length - 1

    // if the total is 0, we need to add a dummy certificate that is hidden to allow for appending
    if (total == 0) {
    i = 0
    div.innerHTML = `
        <div class="autocomplete hidden">
        <div class="input-group mb-3">
            <input class="form-control profile-input certificate" type="text" id="certificate${i}" name="certificate${i}" placeholder="Enter a certificate" autocomplete="off">
            <span class="input-group-btn">
            <button class="btn btn-primary remove-button"  title="Remove this certificate" onclick='removeCertificate(this)' type="button"><span class="glyphicon glyphicon-remove" aria-hidden="true">
            </span></button>
            </span>
        </div>
        </div>
    `  ;
    document.getElementById('certificateHolder').appendChild(div);
    }

    let lastid = $("#certificateHolder input:last").attr("id");
    let split_id = lastid.split("certificate");
    i = Number(split_id[1]) + 1;

    if (i <= max_certificates) {
        div.innerHTML = `
        <div class="autocomplete">
        <div class="input-group mb-3">
            <input class="form-control profile-input certificate" type="text" id="certificate${i}" name="certificate${i}" placeholder="Enter a certificate" autocomplete="off">
            <span class="input-group-btn">
            <button class="btn btn-primary remove-button"  title="Remove this certificate" onclick='removeCertificate(this)' type="button"><span class="glyphicon glyphicon-remove" aria-hidden="true">
            </span></button>
            </span>
        </div>
        </div>
    `  ;

    document.getElementById('certificateHolder').appendChild(div);
    }
}

// ------------------------------------------------------------------

// prepopulate the certificates
function populateCertificates() {

    // create a dummy input for the form to detect changes to the disliked suggestions
    createDummyInput('certificateHolder')

    // Set the certificate title
    const para = document.createElement('p');
    para.setAttribute('id', 'cert-title')
    // div.className = 'certificate-title';
    para.innerHTML = `<b>Intended Certificates:</b>`
    document.getElementById('certificateHolder').appendChild(para);

    for ([i, certificate] of certificates.entries()) {
    const div = document.createElement('div');
    div.className = 'row';

    i++
    
    // only make the first min_preference number required
    div.innerHTML = `
    <div class="autocomplete">
        <div class="input-group mb-3">
            <input class="form-control profile-input certificate" type="text" id="certificate${i}" name="certificate${i}" placeholder="Enter a certificate" value="${certificate}" autocomplete="off">
        <span class="input-group-btn">
            <button class="btn btn-primary remove-button"  title="Remove this certificate" onclick='removeCertificate(this)' type="button"><span class="glyphicon glyphicon-remove" aria-hidden="true">
            </span></button>
            </span>
        </div>
    </div>
    `  ;
    document.getElementById('certificateHolder').appendChild(div);
    }
}

// ------------------------------------------------------------------

function removeCertificate(input) {
    let total = $("#certificateHolder > div").length - 1

    document.getElementById('certificateHolder').removeChild(input.parentNode.parentNode.parentNode.parentNode);
    var i = 0, name, $this;

    // for each certificate
    $('#certificateHolder > div').each(function() {
    if (i > 0) {
        // for each input, change the input id
        $(this).find('input').each(function() {

            // don't change if the dummy input
            if (!isDummy($(this).attr('id'))) {
                $this = $(this);
                $(this).attr('id', 'certificate' + i);
            }
        })
    }
    i++;

    });
    dummyInputSignal(input.parentNode.parentNode)
}

// ------------------------------------------------------------------

// add a liked course after prepopulating the list
function addLikedCourse() {
    const div = document.createElement('div');

    div.className = 'row';

    // get the total number of liked courses being shown,
    // get the id of the last inputted course
    let total = $("#likedCourseHolder > div").length
    let lastid = $("#likedCourseHolder input:last").attr("id");
    let split_id = lastid.split("liked");
    i = Number(split_id[1]) + 1;

    if (i <= max_preference) {
    // only make the first min_preference required
    if (i <= min_preference) {
        div.innerHTML = `
        <div class="autocomplete">
            <label id="liked-label${i}" for="liked${i}">Liked Course #${i}:</label>
            <div class="input-group mb-3">
                <input class="form-control profile-input likedCourse" id="liked${i}" Course" type="text" name="liked${i}" placeholder="Enter a liked course" required autocomplete="off">
                <span class="input-group-btn">
                <button class="btn btn-primary remove-button"  title="Remove this liked course" onclick='removeLiked(this)' type="button"><span class="glyphicon glyphicon-remove" aria-hidden="true">
                </span></button>
                </span>
            </div>
            </div>
        `  ;
    }
    else {
        div.innerHTML = `
        <div class="autocomplete">
            <label id="liked-label${i}" for="liked${i}">Liked Course #${i}:</label>
            <div class="input-group mb-3">
                <input class="form-control profile-input likedCourse" id="liked${i}" Course" type="text" name="liked${i}" placeholder="Enter a liked course" autocomplete="off">
                <span class="input-group-btn">
                <button class="btn btn-primary remove-button"  title="Remove this liked course" onclick='removeLiked(this)' type="button"><span class="glyphicon glyphicon-remove" aria-hidden="true">
                </span></button>
                </span>
            </div>
            </div>
        `  ;
    }
    document.getElementById('likedCourseHolder').appendChild(div);

    }
}

// ------------------------------------------------------------------
// prepopulate the liked courses
function populateLikedCourses() {

    createDummyInput('likedCourseHolder')

    for ([i, course] of liked.entries()) {
    const div = document.createElement('div');
    div.className = 'row';

    i++
    
    // only make the first min_preference number required
    if (i <= min_preference) {
        div.innerHTML = `
        <div class="autocomplete">
            <label id="liked-label${i}" for="liked${i}">Liked Course #${i}:</label>
            <div class="input-group mb-3">
                <input class="form-control profile-input likedCourse" type="text" id="liked${i}" name="liked${i}" placeholder="Enter a liked course" value="${course}" required autocomplete="off">
            <span class="input-group-btn">
                <button class="btn btn-primary remove-button"  title="Remove this liked course" onclick='removeLiked(this)' type="button"><span class="glyphicon glyphicon-remove" aria-hidden="true">
                </span></button>
                </span>
            </div>
        </div>
    `  ;
    }
    else {
    div.innerHTML = `
        <div class="autocomplete">
            <label id="liked-label${i}" for="liked${i}">Liked Course #${i}:</label>
            <div class="input-group mb-3">
                <input class="form-control profile-input likedCourse" type="text" id="liked${i}" name="liked${i}" placeholder="Enter a liked course" value="${course}" required autocomplete="off">
            <span class="input-group-btn">
                <button class="btn btn-primary remove-button"  title="Remove this liked course" onclick='removeLiked(this)' type="button"><span class="glyphicon glyphicon-remove" aria-hidden="true">
                </span></button>
                </span>
            </div>
        </div>
    `  ;
    }
    document.getElementById('likedCourseHolder').appendChild(div);
    }
}

// ------------------------------------------------------------------

function removeLiked(input) {
    // we subtract 2 because of the dummy input and that we are removing one
    let total = $("#likedCourseHolder > div").length - 2;

    if (total >= min_preference) { 

    document.getElementById('likedCourseHolder').removeChild(input.parentNode.parentNode.parentNode.parentNode);
    var i = 0, name, $this;

    // for each liked course
    $('#likedCourseHolder > div').each(function() {
        if (i > 0) {
        // for each label, change the label text and id
        $(this).find('label').each(function() {
            $this = $(this);

            if(!isDummy($(this).attr('id'))) {
                $(this).attr('id', 'liked-label' + i);
                $('#liked-label' + i).text('Liked Course #' + i + ':');
            }
        })

        // for each input, change the input id
        $(this).find('input').each(function() {
            $this = $(this);
            if(!isDummy($(this).attr('id'))) {
                $(this).attr('id', 'liked' + i);

                // we need to set the first min_preference to required
                if (i <= min_preference) {
                $(this).attr('required', 'true');
                }
            }
        })
        }
        i++;
    });

    dummyInputSignal(input.parentNode.parentNode)
    }
}

// ------------------------------------------------------------------

// add a disliked course after prepopulating the list
function addDislikedCourse() {
    const div = document.createElement('div');

    div.className = 'row';

    // get the total number of disliked courses being shown,
    // get the id of the last inputted course
    let lastid = $("#dislikedCourseHolder input:last").attr("id");
    let split_id = lastid.split("disliked");
    i = Number(split_id[1]) + 1;
    

    if (i <= max_preference) {
    // only make the first min_preference required
    if (i <= min_preference) {
        div.innerHTML = `
        <div class="autocomplete">
            <label id="disliked-label${i}" for="disliked${i}">Disliked Course #${i}:</label>
            <div class="input-group mb-3">
                <input class="form-control profile-input dislikedCourse" id="disliked${i}" Course" type="text" name="disliked${i}" placeholder="Enter a disliked course" required autocomplete="off">
                <span class="input-group-btn">
                <button class="btn btn-primary remove-button"  title="Remove this disliked course" onclick='removeDisliked(this)' type="button"><span class="glyphicon glyphicon-remove" aria-hidden="true">
                </span></button>
                </span>
            </div>
            </div>
        `  ;
    }
    else {
        div.innerHTML = `
        <div class="autocomplete">
            <label id="disliked-label${i}" for="disliked${i}">Disliked Course #${i}:</label>
            <div class="input-group mb-3">
                <input class="form-control profile-input dislikedCourse" id="disliked${i}" Course" type="text" name="disliked${i}" placeholder="Enter a disliked course" autocomplete="off">
                <span class="input-group-btn">
                <button class="btn btn-primary remove-button"  title="Remove this disliked course" onclick='removeDisliked(this)' type="button"><span class="glyphicon glyphicon-remove" aria-hidden="true">
                </span></button>
                </span>
            </div>
            </div>
        `  ;
    }
    document.getElementById('dislikedCourseHolder').appendChild(div);
    }
}

// ------------------------------------------------------------------

// prepopulate the disliked courses
function populateDislikedCourses() {

    createDummyInput('dislikedCourseHolder')

    for ([i, course] of disliked.entries()) {
    const div = document.createElement('div');
    div.className = 'row';

    i++
    // only make the first min_preference number required
    if (i <= min_preference) {
        div.innerHTML = `
        <div class="autocomplete">
            <label id="disliked-label${i}" for="disliked${i}">Disliked Course #${i}:</label>
            <div class="input-group mb-3">
                <input class="form-control profile-input dislikedCourse" type="text" id="disliked${i}" name="disliked${i}" placeholder="Enter a disliked course" value="${course}" required autocomplete="off">
            <span class="input-group-btn">
                <button class="btn btn-primary remove-button"  title="Remove this disliked course" onclick='removeDisliked(this)' type="button"><span class="glyphicon glyphicon-remove" aria-hidden="true">
                </span></button>
                </span>
            </div>
        </div>
    `  ;        
    }
    else {
    div.innerHTML = `
        <div class="autocomplete">
            <label id="disliked-label${i}" for="disliked${i}">Disliked Course #${i}:</label>
            <div class="input-group mb-3">
                <input class="form-control profile-input dislikedCourse" type="text" id="disliked${i}" name="disliked${i}" placeholder="Enter a disliked course" value="${course}" required autocomplete="off">
            <span class="input-group-btn">
                <button class="btn btn-primary remove-button"  title="Remove this disliked course" onclick='removeDisliked(this)' type="button"><span class="glyphicon glyphicon-remove" aria-hidden="true">
                </span></button>
                </span>
            </div>
        </div>
    `  ;
    }
    document.getElementById('dislikedCourseHolder').appendChild(div);
    }
}

// ------------------------------------------------------------------

function removeDisliked(input) {
    // we subtract 2 because of the dummy input and that we are removing one
    let total = $("#dislikedCourseHolder > div").length - 2

    if (total >= min_preference) { 

    document.getElementById('dislikedCourseHolder').removeChild(input.parentNode.parentNode.parentNode.parentNode);
    var i = 0, name, $this;

    // for each disliked course
    $('#dislikedCourseHolder > div').each(function() {
        if (i > 0) {
        // for each label, change the label text and id
        $(this).find('label').each(function() {
            $this = $(this);

            if (!isDummy($(this).attr('id'))) {
                $(this).attr('id', 'disliked-label' + i);
                $('#disliked-label' + i).text('Disliked Course #' + i + ':');
            }
        })

        // for each input, change the input id
        $(this).find('input').each(function() {
            $this = $(this);

            if (!isDummy($(this).attr('id'))) {
                $(this).attr('id', 'disliked' + i);

                // we need to set the first min_preference to required
                if (i <= min_preference) {
                $(this).attr('required', 'true');
                }
            }

        })
        }
        i++;
    });

    dummyInputSignal(input.parentNode.parentNode)
    }
}

// ------------------------------------------------------------------

// on ready, populate everything
$(populateDislikedCourses);
$(populateLikedCourses);
$(populateCertificates);
$(populateDislikedSuggestions);

// this will add the dummy input signal to newly added inputs
$(document).on('input', dummyInputSignal);