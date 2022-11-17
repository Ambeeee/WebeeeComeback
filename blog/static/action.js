//ACCOUNT MENU

let icon = document.getElementById("ICON");
function open_menu(){
    let am = document.getElementById("AM");
    am.classList.toggle("dNone");
};

//REVEAL PASSWORD
function reveal_pw(){
    let pw = document.getElementById("PW");
    pw.classList.toggle("dNone");
};

//NEW FIELDS
let add_body = document.getElementById("+body");
let add_img = document.getElementById("+img");
let add_cit = document.getElementById("+cit");

let to_add = {"body": 2, "img": 1, "cit": 1};

function add_to_editor(what="body"){
    num = to_add[what];
    id = document.getElementById(what + num.toString());
    id.classList.toggle("dNone")
    to_add["body"]++;
    to_add["img"]++;
    to_add["cit"]++;
    return to_add
}
