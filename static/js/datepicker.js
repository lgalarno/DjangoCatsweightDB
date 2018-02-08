window.onload=function() {
    var dp = document.getElementsByClassName("datepick");
    for (var i = 0; i < dp.length; i++) {
        dp[i].setAttribute("value", $.datepicker.formatDate('yy-mm-dd', new Date()));
    }
};

$('.datepick').each(function(){
    $(this).datepicker( {
        dateFormat: "yy-mm-dd",
    });
});