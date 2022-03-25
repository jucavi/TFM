const tree = document.querySelector('.tree');
const projectID = tree.id;
const baseURL = `http://localhost:5000/projects/project/${projectID}`;
let currentDirectoryID;

// Add folder
const newFolderAnchor = document.querySelector('#new_folder');
const newFolderModal = document.querySelector('#newFolderModal');
const title = document.querySelector('#newFolderModalLabel');
const modal = bootstrap.Modal.getOrCreateInstance(newFolderModal);
const folderNameInput = document.querySelector('#folder_name');

newFolderModal.addEventListener('shown.bs.modal', function (event) {
  folderNameInput.focus();
});

function removeAllChildNodes(parent) {
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
  }
}

const sendButton = document.querySelector('#send_folder');
sendButton.addEventListener('click', async function (event) {
  event.preventDefault();
  event.stopImmediatePropagation();

  const name = folderNameInput.value;
  const formData = new FormData();
  formData.append('name', name);
  folderNameInput.value = '';

  if (name !== '') {
    await axios.post(`${baseURL}/folder/${currentDirectoryID}`, formData);

    // open and rebuild tree
    const currentWrapper = document.getElementById(currentDirectoryID);
    const content = currentWrapper.lastElementChild;
    removeAllChildNodes(content);

    try {
      const { data } = await axios.get(`${baseURL}/data/${currentDirectoryID}`);
      addTreeView(data.children, data.files, content);
    } catch (e) {
      console.log('Error in getContent:', e);
    }

    // close modal
    modal.hide();
  }
});

newFolderAnchor.addEventListener('click', function (event) {
  event.preventDefault();
  event.stopImmediatePropagation();
  const currentWrapper = document.getElementById(currentDirectoryID);
  title.innerText = `/${currentWrapper.firstElementChild.innerText}/`;
  modal.show();
});

// Delete Folder
const deleteFolderAnchor = document.querySelector('#delete_folder');
deleteFolderAnchor.addEventListener('click', async function (event) {
  event.preventDefault();
  event.stopImmediatePropagation();
  const node = document.getElementById(currentDirectoryID);
  const content = node.parentElement;
  const parent = content.parentElement;

  alert(`Deleting ${node.firstElementChild.innerText}...`);

  const { data } = await axios.delete(
    `${baseURL}/folder/${currentDirectoryID}`
  );

  if (data.success == true) {
    console.log('deleted');
    try {
      currentDirectoryID = parent.id;
      const { data } = await axios.get(`${baseURL}/data/${currentDirectoryID}`);

      node.remove();
    } catch (e) {
      console.log('Error in getContent:', e);
    }
  }
});

// Expand Collapse Directory tree
window.onload = function () {
  const root = tree.querySelector('li');
  currentDirectoryID = root.parentNode.id;
  root.addEventListener('click', expandCollapseToggler);
};

async function expandCollapseToggler(event) {
  event.stopPropagation();
  const id = event.target.parentNode.id;
  currentDirectoryID = id;
  const content = event.target.parentNode.lastElementChild;

  if (content.textContent === '') {
    const url = `${baseURL}/data/${id}`;
    try {
      const { data } = await axios.get(url);
      addTreeView(data.children, data.files, content);
    } catch (e) {
      console.log('Error in getContent:', e);
    }
  } else {
    content.toggleAttribute('hidden');
  }
}

function addDirectory(children, folderContent) {
  for (let child of children) {
    const divWrapper = document.createElement('div');
    divWrapper.classList.add('folder_wrapper');
    divWrapper.setAttribute('id', child.id);

    const li = document.createElement('li');
    li.classList.add('folder');
    li.innerText = child.name;
    li.addEventListener('click', expandCollapseToggler);
    divWrapper.append(li);

    const ul = document.createElement('ul');
    ul.classList.add('folder_content');
    ul.classList.add('fa-ul');
    divWrapper.append(ul);

    folderContent.append(divWrapper);
  }
}

function addFiles(files, folderContent) {
  for (let file of files) {
    const li = document.createElement('li');
    li.setAttribute('id', file.id);
    li.innerText = file.name;
    folderContent.append(li);
  }
}

function addTreeView(children, files, folderContent) {
  addDirectory(children, folderContent);
  addFiles(files, folderContent);
}
