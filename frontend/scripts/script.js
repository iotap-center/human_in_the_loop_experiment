let step_duration = 5000;
let timer = null;

const welcomeMessage = `
<p>Thank you for agreeing to participate in this experiment on interactive machine learning!</p>
<p>During the experiment you will need to give your full attention to the task at hand. The data collected is done anonymously. Because of this, it is important that you don’t close the window (or tab) until the experiment is completely finished.</p>
<p>Your task is to teach the system to recognize cats and dogs. You will be shown images and are asked to tell the system whether the images contain cats or dogs by clicking a button. In some cases, the system has already made a guess and then one button is preselected. If you think that the guess is correct, you do not have to do anything.</p>
<p>Please use a web browser on a computer and not your mobile phone for these experiments. The experiment consists of different parts. After each part there is a break before the next part starts. For each part the number of images will increase. Even if you do not have time to annotate all, please continue. The total time of the experiment will be about 20-25 minutes.</p>
<p>In the first part of the experiment you will see 1 image at a time and you will have 3 seconds to provide input.</p>
<p>If you have any questions regarding the experiment before you start or after, you are welcome to contact Agnes at <a href="mailto:agnes.tegen@mau.se">agnes.tegen@mau.se</a></p>
`;

// Setup
$( async function() {
  await showMessageAndAwaitGo({end_message: welcomeMessage})
  .then(hideMessageAndStart);
  createNewSession()
    .then(fetchSteps)
    .then(fetchStep)
    .then(fetchSubsession)
    .then(fetchSubsessionStep)
    .then(presentSubsessionStep)
    .then(prepareNextStep);
} );

const createNewSession = function () {
  return new Promise( (resolve, reject) => {
    $.ajax({
      url: '/api/v1/sessions',
      method: 'post',
      success: function (data) {
        resolve(data.links.self);
      },
      error: function (error) {
        reject(error);
      }
    });
  })
};

const fetchSteps = function (link) {
  return new Promise( (resolve, reject) => {
    $.ajax({
      url: link.href,
      method: link.method,
      success: function (data) {
        resolve(data.links.first);
      },
      error: function (error) {
        reject(error);
      }
    });
  });
};

const fetchStep = function (link) {
  return new Promise( (resolve, reject) => {
    $.ajax({
      url: link.href,
      method: link.method,
      success: function (data) {
        resolve(data.subsessions[0]);
      },
      error: function (error) {
        reject(error);
      }
    });
  });
};

const fetchSubsession = function (link) {
  return new Promise( (resolve, reject) => {
    $.ajax({
      url: link.href,
      method: link.method,
      success: function (data) {
        resolve(data.subsession_steps[0]);
      },
      error: function (error) {
        reject(error);
      }
    });
  });
};

const fetchSubsessionStep = function (link) {
  return justFetch(link);
};

const justFetch = function (link) {
  return new Promise( (resolve, reject) => {
    $.ajax({
      url: link.href,
      method: link.method,
      success: function (data) {
        resolve(data);
      },
      error: function (error) {
        reject(error);
      }
    });
  });
};

const prepareNextStep = async function (data) {
  await sleep(step_duration);
  if (data.links.next) {
    putSubsessionStep(compileResponses(), data.links.update)
        .then(result => fetchSubsessionStep(data.links.next))
        .then(presentSubsessionStep)
        .then(prepareNextStep);
  } else if (data.links.next_subsession) {
    await putSubsessionStep(compileResponses(), data.links.update)
      .then(showMessageAndAwaitGo)
      .then(hideMessageAndStart)
      .then(result => fetchSubsession(data.links.next_subsession))
      .then(fetchSubsessionStep)
      .then(presentSubsessionStep)
      .then(prepareNextStep);
  } else {
    putSubsessionStep(compileResponses(), data.links.update)
      .then(showMessageAndStop);
  }
};

const putSubsessionStep = function (compilation, link) {
  return new Promise( (resolve, reject) => {
    $.ajax({
      url: link.href,
      method: link.method,
      data: JSON.stringify(compilation),
      contentType: "application/json",
      dataType: "json",
      success: function (data) {
        resolve(data);
      },
      error: function (error) {
        reject(error);
      }
    });
  });
};

const presentSubsessionStep = function (data) {
  return new Promise( (resolve, reject) => {
    step_duration = data.timeout * 1000;
    setupForm(data);
    clearImages();
    addImages(data.images);
    themeRadioButtons();
    resolve(data);
  });
};

const compileResponses = function () {
  const fieldsets = document.getElementsByTagName("fieldset");
  const compilation = {};
  const items = [];
  
  for (const fieldset of fieldsets) {
    items.push(buildResponseItem(fieldset));
  }
  compilation.images = items;
  return compilation;
};

const buildResponseItem = function (fieldset) {
  const item = {};
  item.image = fieldset.elements[0].value;
  item.stream = fieldset.elements[1].value;
  item.query = fieldset.elements[2].value == "true" ? true : false;
  item.classification = -1;
  
  let i = 0;
  for (const element of fieldset.elements) {
    if (element.type == 'radio') {
      if (element.checked) {
        item.classification = i;
        break;
      }
      i++;
    }

  }
  
  return item;
};

const justLog = function (data, message = false) {
  return new Promise( (resolve, reject) => {
    if (message) {
      console.log(message);
    }
    console.log(data);
    resolve(data);
  });
};

const sleep = function (duration) {
  return new Promise(resolve => setTimeout(resolve, duration));
};

const hideMessageAndStart = async function(data) {
  return new Promise((resolve, reject) => {
    const wrapper = document.getElementById("wrapper");
    wrapper.style.visibility = "visible";

    const splashMessage = document.getElementById("splash_message");
    splashMessage.style.visibility = "hidden";
    resolve(data);
  });
};

const showMessageAndAwaitGo = function(data) {
  return new Promise((resolve, reject) => {
    clearImages();
    const wrapper = document.getElementById("wrapper");
    wrapper.style.visibility = "hidden";

    const splashMessage = document.getElementById("splash_message");
    splashMessage.style.visibility = "visible";
    splashMessage.innerHTML = "";
  
    const infoContainer = document.createElement("div");
    infoContainer.classList.add("info-container")
    splashMessage.appendChild(infoContainer);
  
    const infoText = document.createElement("p");
    infoText.innerHTML = data.end_message;
    infoContainer.appendChild(infoText);
  
    const nextButton = document.createElement("button");
    nextButton.setAttribute("type", "button");
    nextButton.innerHTML = "I'm ready, let's start!";
    nextButton.onclick = resolve;
    infoContainer.appendChild(nextButton);
  });
};

const showMessageAndStop = function(data) {
  clearImages();
  const wrapper = document.getElementById("wrapper");
  wrapper.style.visibility = "hidden";

  const splashMessage = document.getElementById("splash_message");
  splashMessage.style.visibility = "visible";
  splashMessage.innerHTML = "";

  const infoContainer = document.createElement("div");
  infoContainer.classList.add("info-container")
  splashMessage.appendChild(infoContainer);

  const infoText = document.createElement("p");
  infoText.innerHTML = data.end_message;
  infoContainer.appendChild(infoText);
};

const themeRadioButtons = function () {
  $("input:radio").checkboxradio({
    icon: false
  });
};

const setupForm = function (data) {
  const form = document.getElementById("step_data");
  form.innerHTML = "";
  
  form.appendChild(createHiddenInput("session", data.session));
  form.appendChild(createHiddenInput("step", data.step));
  form.appendChild(createHiddenInput("subsession", data.subsession));
  form.appendChild(createHiddenInput("subsession_step", data.subsession_step));
};

const createHiddenInput = function (name, value) {
  const element = document.createElement("input");
  element.setAttribute("type", "hidden");
  element.setAttribute("name", name);
  element.setAttribute("value", value);
  return element;
};

const clearImages = function () {
  document.getElementById("wrapper").innerHTML = "";
};

const addImages = function (images) {
  for (const image of images) {
    addImage(image.image_url, image.image, image.stream, image.classification, image.labels, image.query);
  }
};

const addImage = function (imageURL, image, stream, prediction, classes, query) {
  const name = "radio-" + stream;
  const wrapper = document.getElementById("wrapper");
  
  const rootDiv = document.createElement("div");
  rootDiv.classList.add("grid-item");
  rootDiv.classList.add("item-container");
  wrapper.appendChild(rootDiv);
  
  if (query) {
    const imageDiv = document.createElement("div");
    imageDiv.classList.add("image-container");
    rootDiv.appendChild(imageDiv);
    
    const imageElement = document.createElement("img");
    imageElement.src = imageURL;
    imageDiv.appendChild(imageElement);
    
    const fieldset = document.createElement("fieldset");
    fieldset.classList.add("grid-container");
    rootDiv.appendChild(fieldset);
    
    fieldset.appendChild(createHiddenInput("image", image));
    fieldset.appendChild(createHiddenInput("stream", stream));
    fieldset.appendChild(createHiddenInput("query", query));
    
    for (let i = 0; i < classes.length; i++) {
      let label = document.createElement("label");
      let input = document.createElement("input");
      let labelText = document.createTextNode(classes[i]);
      let id = name + '-' + i;
      
      label.setAttribute("for", id);
      label.classList.add("grid-item");
      
      input.id = id;
      input.setAttribute("type", "radio");
      input.setAttribute("name", name);
      input.setAttribute("value", i);
      if (prediction == i) {
        input.checked = true;
      }
      
      label.appendChild(labelText);
      fieldset.appendChild(label);
      fieldset.appendChild(input);
    }
  } else {
    rootDiv.innerHTML = "[Image not displayed]";
  }
};
