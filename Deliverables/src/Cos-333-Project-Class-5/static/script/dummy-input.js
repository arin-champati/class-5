// create a hidden input that will be used to detect if divs have been added or removed
function createDummyInput(holderID) {
    const div = document.createElement('div');
    div.className = 'hidden';
    div.innerHTML = `
        <div class="autocomplete hidden">
        <label id="dummy-label" for="dummy-input"></label>
        <div class="input-group mb-3 hidden">
            <input class="form-control profile-input hidden" type="text" id="dummy-input" name="dummy-input" value="nothing" readonly autocomplete="off">
        </div>
        </div>
    `
    document.getElementById(holderID).appendChild(div);
}

// send out an input signal after changing the value of the input
function dummyInputSignal(input) {
    // if there is no text in the input, then return
    if (input) {
        // handle if the input is an event
        if ('target' in input) {
            if (input.target.value.trim() == '') {
                return
            }
        }
        // handle if the input is a parent node
        else if ('value' in input.children[0]) {
            if (input.children[0].value.trim() =='') {
                return
            }
        }
    }
    if (document.getElementById('dummy-input')) {
        document.getElementById('dummy-input').value = 'changed'
        document.getElementById('dummy-input').dispatchEvent(new Event('input'));
    }
}

// return if the given id correlates to a dummy input
function isDummy(id) {
    return (id == 'dummy-input' | id=='dummy-label')
}