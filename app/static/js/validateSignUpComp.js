const qSelector = (query) => document.querySelector(query);
const qSAll = (query) => document.querySelectorAll(query);

const form = qSelector("#signup_form");
form.addEventListener("submit", singUp);

function validateEmail(input) {
  const regex = /[^@]+[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}/gm;
  return regex.test(input.value);
}

function validatePass(input) {
  const passRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$/;
  return passRegex.test(input.value);
}

function validateName(input) {
  // console.log(input);

  // const nameRegex = /([\d+\W+])/gi;
  // return input.value.length >= 2 && !nameRegex.test(input.value);
  return input.value.length >= 2;
}

function singUp(e) {
  e.preventDefault();
  is_valid = true;
  // console.log(e.target);
  const fName = qSelector("#company_name");
  const pass = qSelector("#password");
  const confirm_pass = qSelector("#confirm_password");
  const email = qSelector("#email");
  const location = qSelector("#location");
  const desc = qSelector("#description");

  if (!validateName(fName)) {
    is_valid = false;
    const p = document.createElement("p");
    p.classList.add("errorMsg");
    p.style.cssText = "color: red; font-weight: bold;";
    p.innerHTML = `<i class="fas validation fa-exclamation-circle"></i>Invalid Name, You must provide a name greater than 2 characters long.`;
    if (fName.parentNode.children.length < 3) fName.parentNode.appendChild(p);
  }

  if (!validatePass(pass)) {
    is_valid = false;
    const p = document.createElement("p");
    p.classList.add("errorMsg");
    p.style.cssText = "color: red; font-weight: bold;";
    p.innerHTML = `<i class="fas validation fa-exclamation-circle"></i>Invalid Password, It should contain numbers, special characters,uppercase letters, lowercase letters and You must provide a password greater than 7 characters long.`;
    if (pass.parentNode.children.length < 3) pass.parentNode.appendChild(p);
  }

  if (confirm_pass.value != pass.value) {
    is_valid = false;
    const p = document.createElement("p");
    p.classList.add("errorMsg");
    p.style.cssText = "color: red; font-weight: bold;";
    p.innerHTML = `<i class="fas validation fa-exclamation-circle"></i>Your passwords don't match`;
    if (confirm_pass.parentNode.children.length < 3)
      confirm_pass.parentNode.appendChild(p);
  }

  if (!validateEmail(email)) {
    is_valid = false;
    const p = document.createElement("p");
    p.classList.add("errorMsg");
    p.style.cssText = "color: red; font-weight: bold;";
    p.innerHTML = `<i class="fas validation fa-exclamation-circle"></i>Invalid email format, correct format is example@example.com`;
    if (email.parentNode.children.length < 3) email.parentNode.appendChild(p);
  }

  if (desc.value.length <= 2) {
    is_valid = false;
    const p = document.createElement("p");
    p.classList.add("errorMsg");
    p.style.cssText = "color: red; font-weight: bold;";
    p.innerHTML = `<i class="fas validation fa-exclamation-circle"></i>You must provide a brief description`;
    if (desc.parentNode.children.length < 3) desc.parentNode.appendChild(p);
  }

  if (location === "" || location.value.length < 2) {
    const p = document.createElement("p");
    p.classList.add("errorMsg");
    p.style.cssText = "color: red; font-weight: bold; ";
    p.innerHTML = `<i class="fas validation fa-exclamation-circle"></i>You must provide a location`;
    if (location.parentNode.children.length < 4)
      location.parentNode.appendChild(p);
  }
  if (is_valid) {
    const errorMsgs = qSAll(".errorMsg");
    errorMsgs.forEach((msg) => msg.remove());
    console.log("is valid => ", is_valid);
  }
}
