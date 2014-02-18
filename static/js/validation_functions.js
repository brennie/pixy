/**
 * Created by kabary on 15/02/14.
 */
// Java script validation

// Email validation
// There should be at least one character before the @ character
// There should be at least one dot after the @ character
// There should be at least one letter between the @ and the last dot.
// There should be at least two character after the last dot.
// There shouldn't exists two @ characters in the email
function validate_email(event)
{

    var email = event.currentTarget;
    validate_email_Implementation(email);


}

function validate_email_Implementation(email)
{

    var emailLength = email.value.length;
    // number of @'s characters
    var numberofats = 0;
    // advice the user when he do mistakes
    var advice;
    if(email.id == "email")
    {
          // login page (Homepage)
        advice = document.getElementById("advicebox");
    }
    else
    {
        // sign up page

        advice = document.getElementById("advicesignup");
    }

    // if the email is Empty , return false
    if(is_Empty(email.value))
    {
        if(email.id == "email")
        {
            advice.innerHTML = ("Please enter your Email");
            advice.style.visibility = "visible";
            //email.focus();
            return false;
        }
        else
        {

            advice.className = "signupAdvice2";
            advice.innerHTML = ("Please enter your Email");
            advice.style.visibility = "visible";
            return false;
        }
    }

    var atposition=email.value.indexOf("@");
    var dotposition=email.value.lastIndexOf(".");
    for(i = 0;i < emailLength;i++)
    {
        if(email.value[i] == '@')
            numberofats++;
    }

    if(spacesFound(email.value))
    {
        if(email.id == "email")
        {
            advice.innerHTML = ("No Spaces are allowed in an Email-format");
            advice.style.visibility = "visible";
        }
        else
        {
            advice.className ="signupAdvice2";
            advice.innerHTML = ("No Spaces are allowed in an Email-format");
            advice.style.visibility = "visible";
            return false;
        }

        //email.focus();
    }

    if (numberofats >1 || atposition<1 || dotposition<atposition+2 || dotposition+2>=emailLength)
    {
        if(email.id == "email")
        {
            advice.innerHTML = ("Invalid e-mail address Format");
            advice.style.visibility = "visible";
            //email.focus();
            return false;
        }
        else
        {
            advice.className = "signupAdvice2";
            advice.innerHTML = ("Invalid e-mail address Format");
            advice.style.visibility = "visible";
            return false;
        }
    }
    advice.style.visibility = "hidden";
    return true;
}

//Password validation
//It should be at least eight characters long
//It shouldn't contain a white space character
//In the sign up, the password should have at least one non-letter character
function validate_password(event)
{
    var pass = event.currentTarget;
    validate_password_Implementation(pass);

}

function validate_password_Implementation(pass)
{
    var passLength = pass.value.length;
    var advice;

    if(pass.id == "pass")
    {
        advice = document.getElementById("advicebox");
    }
    else
    {
        advice = document.getElementById("advicesignup");
    }
    // if password is empty return false
    if(passLength == 0)
    {
        if(pass.id == "pass")
        {
            advice.innerHTML = "Please Enter Your Password";
            advice.style.visibility = "visible";
            //pass.focus();
        }
        else
        {
            advice.className = "signupAdvice3";
            advice.innerHTML = "Please Enter Your Password";
            advice.style.visibility = "visible";

        }
        return false;
    }
    // if password is less than 8 characters, return false
    if(passLength < 8)
    {
        if(pass.id == "pass")
        {
            advice.innerHTML = "Password should be at least 8 characters long";
            advice.style.visibility = "visible";
            //pass.focus();
        }
        else
        {
            advice.className = "signupAdvice3";
            advice.innerHTML = "Password should be at least 8 characters long";
            advice.style.visibility = "visible";

        }
        return false;
    }
    // if password contain spaces ,return false
    if(spacesFound(pass.value))
    {
        if(pass.id == "pass")
        {
            advice.innerHTML = "Spaces are not allowed in the password";
            advice.style.visibility = "visible";
        }
        else
        {
            advice.className ="signupAdvice3";
            advice.innerHTML = "Spaces are not allowed in the password";
            advice.style.visibility = "visible";
        }
        return false;
    }
    // if the sign up password doesn't contain any non-letter character or if the password is all numbers,returns false
    if(pass.id == "initial")
    {
        if(pass.value.search(/[^A-Za-z]/) == -1 || pass.value.search(/[^0-9]/) == -1)
        {
            advice.className = "signupAdvice3";
            advice.innerHTML = "Password should be a Combination of letters and special characters or numbers ";
            advice.style.visibility = "visible";
            return false
        }


    }


    advice.style.visibility = "hidden";
    return true;

}


//Function that detects if spaces are found in a string
//returns true if spaces are found
//returns false if there were no spaces
function spacesFound(str)
{

    if(str.search(/[\s]/) != -1)
    {
        return true;
    }


    return false;
}

//Name validation
//Function that validates the first and last name format
//If there are leading or trailing spaces , they are cut off
//returns false if the names is empty ,or names contains non-letter characters
//else returns true
function checkName(event)
{

    var name = event.currentTarget;
    checkNameImplementation(name);



}



function checkNameImplementation(name)
{

    var advice = document.getElementById("advicesignup");
    if(is_Empty(name.value))
    {

        if(name.id == "firstname")
        {
            advice.className = "signupAdvice";
            advice.innerHTML = "Please Enter your First Name";
            advice.style.visibility = "visible";
        }
        else
        {
            advice.className = "signupAdvice1";
            advice.innerHTML = "Please Enter your Last Name";
            advice.style.visibility = "visible";
        }
        return false;
        //name.focus();

    }
    // if the name contains special characters or digits , returns false
    if(name.value.search(/[^A-Za-z\s]/) != -1)
    {
        if(name.id == "firstname")
        {
            advice.className = "signupAdvice";
            advice.innerHTML = " Valid names does not contain special characters or digits";
            advice.style.visibility = "visible";
        }
        else
        {
            advice.className = "signupAdvice1";
            advice.innerHTML = " Valid names does not contain special characters or digits";
            advice.style.visibility = "visible";

        }
        return false;
    }


    else
    {
        name.value = removeLTSpaces(name.value);
        advice.style.visibility = "hidden";
        return true;
    }

}

//Function to check if a string is empty or null
function is_Empty(str)
{

    if((str == null ) || (str == ""))
        return true;
    return false;


}

//Function to remove leading and trailing spaces
function removeLTSpaces(str)
{
    var newstr;
    newstr = str.replace(/^\s*/, "").replace(/\s*$/, "");
    newstr = newstr.replace(/\s{2,}/, " ");
    return newstr;
}



//Confirms password validation
//If empty , return false
//If it's not equal to the initial password returns false
//else returns true
function checkPasswords(event)
{

    var sec = event.currentTarget;
    checkPasswords_Implementation(sec);


}

function checkPasswords_Implementation(sec)
{
    var advice = document.getElementById("advicesignup");
    var init = document.getElementById("initial");
    if(init.value != "" && sec.value == "")
    {
        advice.className ="signupAdvice4";
        advice.innerHTML = "Please Confirm Password";
        advice.style.visibility = "visible";
        return false;
    }
    if(init.value != sec.value)
    {
        advice.className = "signupAdvice4";
        advice.innerHTML = "Passwords don't match";
        advice.style.visibility = "visible";
        return false;
    }
    return true;
    advice.style.visibility = "hidden";
}

// when the user submit the sign up form, check that it is valid
function validate_signup(event)
{


    var suForm = event.currentTarget;
    var fnameNode = document.getElementById("firstname");
    var lnameNode = document.getElementById("lastname");
    var suemailNode = document.getElementById("signupemail");
    var genderNode = document.getElementById("gender");
    var initialPassNode = document.getElementById("initial");
    var secondPassNode = document.getElementById("second");
    var genderNode = document.getElementById("gender");
    var dayNode = document.getElementById("day");



    if(checkNameImplementation(fnameNode) == false)
    {
        fnameNode.focus();
        event.preventDefault();

    }

    else if(checkNameImplementation(lnameNode) == false)
    {
        lnameNode.focus();
        event.preventDefault();

    }
    else if(validate_email_Implementation(suemailNode) == false)
    {
        suemailNode.focus();
        event.preventDefault();
    }

    else if(validate_password_Implementation(initialPassNode) == false)
    {
        initialPassNode.focus();
        event.preventDefault();
    }

    else if(checkPasswords_Implementation(secondPassNode) == false)
    {
        secondPassNode.focus();
        event.preventDefault();
    }

    else
    {
        alert("The Form is now valid");
    }
}
