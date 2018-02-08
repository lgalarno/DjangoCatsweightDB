
function disableSelect(clicked_id){
    var splitID = clicked_id.split("-");
    var catID = splitID[splitID.length - 1];
    var cweigthID = 'cweigth-'.concat(catID);
    //var c = "{{ gamecategory|safe }}";
    if(document.getElementById(clicked_id).checked == true){
        document.getElementById(cweigthID).removeAttribute("disabled");
    }else{
        document.getElementById(cweigthID).setAttribute("disabled","disabled");
    }
}