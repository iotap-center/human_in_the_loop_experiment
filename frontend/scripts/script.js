const duration = 5000;
let timer = null;

// Setup
$( function() {
  createNewSession()
    .then(fetchStep)
    .then(presentStep);
} );

const createNewSession = function () {
  return new Promise( (resolve, reject) => {
    $.ajax({
      url: '/api/v1/sessions',
      method: 'post',
      success: function (data) {
        resolve(data.links.first);
      },
      error: function (error) {
        reject(error);
      }
    });
  })
};

const fetchStep = function (link) {
  return new Promise( (resolve, reject) => {
    $.ajax({
      url: link.href,
      metod: link.method,
      success: function (data) {
        resolve(data);
      },
      error: function (error) {
        reject(error);
      }
    });
  });
};

const putStep = function (compilation, link) {
  return new Promise( (resolve, reject) => {
    $.ajax({
      url: link.href,
      method: link.method,
      data: JSON.stringify(compilation),
      contentType: "application/json",
      dataType: "json",
      success: function (data) {
        resolve(data.links.next);
      },
      error: function (error) {
        reject(error);
      }
    });
  });
};

const compileResponses = function () {
  const fieldsets = document.getElementsByTagName("fieldset");
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
  item.image = fieldset.elements[1].value;
  item.subsession = fieldset.elements[0].value;
  item.classification = -1;
  
  for (let i = 2; i < fieldset.elements.length; i++) {
    if (fieldset.elements[i].checked) {
      item.classification = i - 2;
      break;
    }
  }
  
  return item;
};

const justLog = function (data) {
  console.log(data);
};

const startTimer = function (update) {
  timer = setTimeout(tick(update), duration);
};

const tick = function (update) {
  return function() {
    clearTimeout(timer);
    putStep(compileResponses(), update)
      .then(fetchStep)
      .then(presentStep)
      .catch(justLog);
  };
};

const presentStep = function (data) {
  startTimer(data.links.update);
  clearImages();
  addImages(data.images);
  setColumns(calculateColumns(data.images));
  themeRadioButtons();
};

const themeRadioButtons = function () {
  $("input:radio").checkboxradio({
    icon: false
  });
};

const setColumns = function (columns) {
  if (Number.isInteger(columns)) {
    $("#wrapper").css("grid-template-columns", repeatColumns(columns));
  }
};

const repeatColumns = function (columns) {
  return "auto ".repeat(columns).trim();
};

const calculateColumns = function (images) {
  // Due to new layout stuff, this will mostly return 3. Remove later!
  if (images.length == 1) {
    return 1;
  }
  return 3;
}

const clearImages = function () {
  document.getElementById("wrapper").innerHTML = "";
};

const addImages = function (images) {
  for (let i = 0; i < images.length; i++) {
    let image = images[i];
    addImage(image.image_url, image.image, image.subsession, image.prediction, image.labels);
  }
};

const addImage = function (imageURL, image, subsession, prediction, classes) {
  const name = "radio-" + subsession;
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
  fieldset.style.gridTemplateColumns = repeatColumns(classes.length);
  rootDiv.appendChild(fieldset);
  
  const subsessionField = document.createElement("input");
  subsessionField.setAttribute("type", "hidden");
  subsessionField.setAttribute("name", "subsession");
  subsessionField.setAttribute("value", subsession);
  fieldset.appendChild(subsessionField);
  
  const imageField = document.createElement("input");
  imageField.setAttribute("type", "hidden");
  imageField.setAttribute("name", "image");
  imageField.setAttribute("value", image);
  fieldset.appendChild(imageField);
  
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
