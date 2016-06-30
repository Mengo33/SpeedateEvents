"use strict";

$("ul li").click(function (){
    console.log("click");
    $(this).addClass("is_active");
    $("ul li").removeClass("is_active");
});
