var formNode;
var suemailNode;

window.addEventListener("load", function(e) {
	formNode = document.getElementById("editInfo");
	suemailNode = document.getElementById("signupemail");

	formNode.addEventListener("editInfo",validate_profileEdit,false);
	suemailNode.addEventListener("blur",validate_email,false);
});

