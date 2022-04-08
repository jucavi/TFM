const tree = document.querySelector('.tree');
const projectID = tree.id;
const baseURL = `http://localhost:5000/projects/project/${projectID}`;
let currentDirectoryID;

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
    const currentWrapper = document.getElementById(currentDirectoryID);
    if (this.innerText === 'Update') {
      await axios.put(`${baseURL}/folder/${currentDirectoryID}`, formData);
      const content = currentWrapper.parentNode;
      // console.log(content)
      try {
        const { data } = await axios.get(
          `${baseURL}/data/${content.parentNode.id}`
        );
        // open and rebuild tree
        removeAllChildNodes(content);
        addTreeView(data.children, data.files, content);
      } catch (e) {
        console.log('Error in getContent:', e);
      }
    } else {
      await axios.post(`${baseURL}/folder/${currentDirectoryID}`, formData);
      const content = currentWrapper.lastElementChild;
      try {
        const { data } = await axios.get(
          `${baseURL}/data/${currentDirectoryID}`
        );
        // open and rebuild tree
        removeAllChildNodes(content);
        addTreeView(data.children, data.files, content);
      } catch (e) {
        console.log('Error in getContent:', e);
      }
    }
  }
  // close modal
  modal.hide();
});

// Add folder
const newFolderAnchor = document.querySelector('#new_folder');
const newFolderModal = document.querySelector('#FolderModal');
const title = document.querySelector('#FolderModalLabel');
const modal = bootstrap.Modal.getOrCreateInstance(newFolderModal);
const folderNameInput = document.querySelector('#folder_name');

newFolderModal.addEventListener('shown.bs.modal', function (event) {
  folderNameInput.focus();
});

newFolderAnchor.addEventListener('click', function (event) {
  event.preventDefault();
  event.stopImmediatePropagation();
  const currentWrapper = document.getElementById(currentDirectoryID);
  title.innerText = `/${currentWrapper.firstElementChild.innerText}/<New folder>`;
  sendButton.innerText = 'Create';
  modal.show();
});

// Renamefolder
const renameFolderAnchor = document.querySelector('#rename_folder');
renameFolderAnchor.addEventListener('click', async function (event) {
  event.preventDefault();
  event.stopImmediatePropagation();
  const currentWrapper = document.getElementById(currentDirectoryID);
  title.innerText = `Reneame /${currentWrapper.firstElementChild.innerText}/`;
  folderNameInput.value = currentWrapper.firstElementChild.innerText;
  sendButton.innerText = 'Update';
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
  root.addEventListener('dblclick', openFiles);
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
    li.addEventListener('dblclick', openFiles);
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

// View files
const go = document.querySelector('#files');
function openFiles(event) {
  event.stopPropagation();
  go.href = go.href.replace('folder_id', currentDirectoryID);
  window.open(go.href, '_self');
}
