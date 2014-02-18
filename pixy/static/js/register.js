/**
 * Created by kabary on 14/02/14.
 */
var formNode = document.getElementById("signup");
var fnameNode = document.getElementById("firstname");
var lnameNode = document.getElementById("lastname");
var suemailNode = document.getElementById("signupemail");
var initialPassNode = document.getElementById("initial");
var secondPassNode = document.getElementById("second");



formNode.addEventListener("submit",validate_signup,false);
fnameNode.addEventListener("blur",checkName,false);
lnameNode.addEventListener("blur",checkName,false);
suemailNode.addEventListener("blur",validate_email,false);
initialPassNode.addEventListener("blur",validate_password,false);
secondPassNode.addEventListener("blur",checkPasswords,false);



