/**
 * Created by kabary on 19/02/14.
 */
var descriptionNode = document.getElementById("description");
var titleNode = document.getElementById("title");
var formNode = document.getElementById("upload");



titleNode.addEventListener("keydown",countingOne,true);
descriptionNode.addEventListener("keydown",countingTwo,true);
formNode.addEventListener("submit",validate_image,false);



