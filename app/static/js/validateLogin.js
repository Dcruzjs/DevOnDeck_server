const qSelector = (query) => document.querySelector(query);
const qSAll = (query) => document.querySelectorAll(query);

const form = qSelector("#login_form");
form.addEventListener("submit", logIn);

function validateEmail(input) {
  const regex = /[^@]+[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}/gm;
  return regex.test(input.value);
}

function validatePass(input) {
  const passRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$/;
  return passRegex.test(input.value);
}

function logIn(e) {
  e.preventDefault();
  is_valid = true;
  // console.log(e.target);

  const email = qSelector("#email");
  const pass = qSelector("#password");

  if (!validatePass(pass)) {
    is_valid = false;
    const p = document.createElement("p");
    p.classList.add("errorMsg");
    p.style.cssText = "color: red; font-weight: bold;";
    p.innerHTML = `<i class="fas validation fa-exclamation-circle"></i>Invalid Password, It should contain numbers, special characters,uppercase letters, lowercase letters and You must provide a password greater than 7 characters long.`;
    if (pass.parentNode.children.length < 3) pass.parentNode.appendChild(p);
  }

  if (!validateEmail(email)) {
    is_valid = false;
    const p = document.createElement("p");
    p.classList.add("errorMsg");
    p.style.cssText = "color: red; font-weight: bold;";
    p.innerHTML = `<i class="fas validation fa-exclamation-circle"></i>Invalid email format, correct format is example@example.com`;
    if (email.parentNode.children.length < 3) email.parentNode.appendChild(p);
  }

  if (is_valid) {
    const errorMsgs = qSAll(".errorMsg");
    errorMsgs.forEach((msg) => msg.remove());
    console.log("is valid => ", is_valid);
  }
}
