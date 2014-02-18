var formNode;
var fnameNode;
var lnameNode;
var suemailNode;
var initialPassNode;
var secondPassNode;

window.addEventListener("load", function(e) {
	formNode = document.getElementById("signup");
	fnameNode = document.getElementById("firstname");
	lnameNode = document.getElementById("lastname");
	suemailNode = document.getElementById("signupemail");
	initialPassNode = document.getElementById("initial");
	secondPassNode = document.getElementById("second");

	formNode.addEventListener("submit",validate_signup,false);
	fnameNode.addEventListener("blur",checkName,false);
	lnameNode.addEventListener("blur",checkName,false);
	suemailNode.addEventListener("blur",validate_email,false);
	initialPassNode.addEventListener("blur",validate_password,false);
	secondPassNode.addEventListener("blur",checkPasswords,false);
});

