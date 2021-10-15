const qSelector = (query) => document.querySelector(query);
const qSAll = (query) => document.querySelectorAll(query);

const form = qSelector("#position_form");
form.addEventListener("submit", validatePosition);

function validatePosition(e) {
  e.preventDefault();
  is_valid = true;

  const position_name = qSelector("#position_name");
  const skills = qSAll("input:checked");
  const location = qSelector("#location");
  const description = qSelector("#description");

  if (position_name.value.length < 2) {
    is_valid = false;
    const p = document.createElement("p");
    p.classList.add("errorMsg");
    p.style.cssText = "color: red; font-weight: bold;";
    p.innerHTML = `<i class="fas validation fa-exclamation-circle"></i>Invalid input, You must provide an input greater than 2 characters long.`;
    if (position_name.parentNode.children.length < 3)
      position_name.parentNode.appendChild(p);
  }
  if (location.value.length < 2) {
    is_valid = false;
    const p = document.createElement("p");
    p.classList.add("errorMsg");
    p.style.cssText = "color: red; font-weight: bold;";
    p.innerHTML = `<i class="fas validation fa-exclamation-circle"></i>Invalid input, You must provide a valid location.`;
    if (location.parentNode.children.length < 4)
      location.parentNode.appendChild(p);
  }

  if (skills.length < 1) {
    is_valid = false;
    const skillsContainer = qSelector("#skills");
    const p = document.createElement("p");
    p.classList.add("errorMsg");
    p.style.cssText = "color: red; font-weight: bold;";
    p.innerHTML = `<i class="fas validation fa-exclamation-circle"></i>You must provide at least 1 skill requiered to match the position.`;
    if (skillsContainer.children.length < 6) skillsContainer.appendChild(p);
  }
  if (description.value.length < 2) {
    is_valid = false;
    console.log(description);
    const p = document.createElement("p");
    p.classList.add("errorMsg");
    p.style.cssText = "color: red; font-weight: bold;";
    p.innerHTML = `<i class="fas validation fa-exclamation-circle"></i>Invalid input, You must provide a valid description; at least 2 characters long.`;
    if (description.parentNode.children.length < 3)
      description.parentNode.appendChild(p);
  }

  if (is_valid) {
    const errorMsgs = qSAll(".errorMsg");
    errorMsgs.forEach((msg) => msg.remove());
    console.log("is valid => ", is_valid);
  }
}
