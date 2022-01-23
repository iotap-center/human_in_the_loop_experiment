let duration = 5000;
let timer = null;

// Setup
$( function() {
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
  //startTimer(data.timeout * 1000);
  if (data.links.next) {
      putSubsessionStep(compileResponses(), data.links.update)
        .then(data => fetchSubsessionStep(data.links.next))
        .then(presentSubsessionStep)
        .then(prepareNextStep);
  } else if (data.links.next_subsession) {
    putSubsessionStep(compileResponses(), data.links.update)
      .then(data => fetchSubsession(data.links.next_subsession))
      .then(fetchSubsessionStep)
      .then(presentSubsessionStep)
      .then(prepareNextStep);
  } else {
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
    setupForm(data);
    clearImages();
    addImages(data.images);
    themeRadioButtons();
    resolve(data);
  });
};

const compileResponses = function () {
  const fieldsets = document.getElementsByTagName("fieldset");
  const form = document.getElementById('step_data');
  const compilation = {};
  const items = [];
  
  for (let i = 0; i < fieldsets.length; i++) {
    items.push(buildResponseItem(fieldsets[i]));
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
  
  for (let i = 2; i < fieldset.elements.length; i++) {
    if (fieldset.elements[i].checked) {
      item.classification = i - 2;
      break;
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

const startTimer = function (update) {
  timer = setTimeout(tick(update), duration);
};

const tick = function (update) {
  return function() {
    clearTimeout(timer);
  };
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
  for (let i = 0; i < images.length; i++) {
    let image = images[i];
    addImage(image.image_url, image.image, image.stream, image.classification, image.labels, image.query);
  }
};

const addImage = function (imageURL, image, stream, prediction, classes, query) {
  const name = "radio-" + stream;
  const wrapper = document.getElementById("wrapper");
  
  const rootDiv = document.createElement("div");
  rootDiv.classList.add("grid-item");
  wrapper.appendChild(rootDiv);
  
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
};
