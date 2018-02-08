function SelectAll () {
    var SelAllChecbox = document.getElementById('selectall');
    var measChecboxes = document.getElementsByName('selectw');
    if (SelAllChecbox.checked) {
        for (var i = 0; i < measChecboxes.length; i++) {
            measChecboxes[i].checked = true;
        }
    } else {
        for (var i = 0; i < measChecboxes.length; i++) {
            measChecboxes[i].checked = false;
        }
    }
}

function ConfirmDelete() {
    var measChecboxes = document.getElementsByName('selectw');
    var nchecked = false;
    for (var i = 0; i < measChecboxes.length; i++) {
        if (measChecboxes[i].checked){
            nchecked = true;
            break;
        }
    }
    if (nchecked){
        return confirm('Are you sure you want to delete?');
    }
}

var buttons = document.getElementsByName("submitbtn");
var buttonsCount = buttons.length;

for (var i = 0; i < buttonsCount; i += 1) {
    buttons[i].onclick = function(e) {
        var measChecboxes = document.getElementsByName('selectw');
        var nchecked = false;
        for (var i = 0; i < measChecboxes.length; i++) {
            if (measChecboxes[i].checked){
                nchecked = true;
                break;
            }
        }
        if (nchecked){
            if (this.value == 'Delete') {
                return confirm('Are you sure you want to delete?');
            }
            return true;
        }
        return false;
    };
}