// Current folder
let currentFolder = document.querySelector('#current_folder');
const currentFolderName = document.querySelector('#current_folder_name');
const newFolder = document.querySelector('#new_folder');
const renameFolder = document.querySelector('#rename_folder');
const deleteFolder = document.querySelector('#delete_folder');

const projectId = currentFolder.getAttribute('project_id');
const folderId = currentFolder.getAttribute('folder_id');
const baseURL = `http://localhost:5000/projects/project`;

// Folder Modal
const folderModal = document.querySelector('#FolderModal');
const title = document.querySelector('#FolderModalLabel');
const modalFolder = bootstrap.Modal.getOrCreateInstance(folderModal);
const folderNameInput = document.querySelector('#folder_name');
const sendButtonModal = document.querySelector('#send_folder');

// Delete Modal
const deleteModal = document.querySelector('#deleteModal');
const modalDelete = bootstrap.Modal.getOrCreateInstance(deleteModal);

// Folder content
const folderShape = document.querySelector('.folder-shape');
const fileShape = document.querySelector('.file-shape');
const folderContentContainer = document.getElementById('children');

// Back to parent
const backButton = document.querySelector('#back_folder');

// Files
const inputElement = document.getElementById('file_upload');

inputElement.addEventListener('change', handleFiles, false);
async function handleFiles() {
  const folderId = currentFolder.getAttribute('folder_id');
  const fileList = this.files;
  const url = `${baseURL}/${projectId}/files/${folderId}/upload`;

  const formData = new FormData();
  for (let f of fileList) {
    formData.append('file', f);
  }

  try {
    const { data } = await axios({
      url: url,
      method: 'POST',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (data.success) {
      refreshFolderContent(folderId);
    } else {
      flashMessage(data.msg, data.category);
    }
  } catch (e) {
    console.log(e);
  }
}

const removeChilds = (parent) => {
  while (parent.lastChild) {
    parent.removeChild(parent.lastChild);
  }
};

const contentFolderResponse = async function (folderId) {
  try {
    const res = await axios.get(`${baseURL}/${projectId}/content/${folderId}`);

    return res;
  } catch (e) {
    console.log(folderId, ': contentFolderResponse');
    console.log(e);
  }
};

async function openFolder(event) {
  event.stopPropagation();
  event.stopImmediatePropagation();
  const folderId = this.getAttribute('folder_id');
  refreshFolderContent(folderId);
}

const flashMsg = document.querySelector('#flash_messages');

folderModal.addEventListener('shown.bs.modal', function (event) {
  folderNameInput.focus();
});

folderModal.addEventListener('hidden.bs.modal', function (event) {
  const msgLI = document.querySelector('#modal_msg');
  msgLI.textContent = '';
  folderNameInput.value = '';
});

newFolder.addEventListener('click', function (event) {
  event.preventDefault();
  event.stopImmediatePropagation();

  title.innerText = 'New Folder';
  sendButtonModal.innerText = 'New';
  modalFolder.show();
});

function renameFolderListener(event) {
  event.preventDefault();
  event.stopImmediatePropagation();

  title.innerText = 'Rename Folder';
  folderNameInput.value = currentFolderName.innerText;
  sendButtonModal.innerText = 'Rename';
  modalFolder.show();
}

renameFolder.addEventListener('click', renameFolderListener);

const deleteConfirmation = document.querySelector('#delete_confirmation');
deleteConfirmation.addEventListener('click', function (event) {
  event.stopImmediatePropagation();
  const result = folderResponse('DELETE');

  result
    .then(function (response) {
      const folderId = currentFolder.getAttribute('parent_id');

      const { success, msg, category } = response.data;
      modalDelete.hide();
      flashMessage(msg, category);
      if (success) {
        refreshFolderContent(folderId);
      }
    })
    .catch(function (error) {
      console.log(error);
    });
});

deleteFolder.addEventListener('click', function (event) {
  event.stopImmediatePropagation();
  modalDelete.show();
});

const folderResponse = async function (method, data = null) {
  const folderId = currentFolder.getAttribute('folder_id');

  try {
    const res = await axios({
      method: method,
      url: `${baseURL}/${projectId}/folder/${folderId}`,
      data: data,
    });

    return res;
  } catch (e) {
    console.log(folderId, ': Id folder resposnse');
    console.log(e);
  }
};

function flashMessage(msg, category) {
  const div = document.createElement('div');
  div.setAttribute(
    'class',
    `alert alert-${category} alert-dismissible fade show text-center`
  );
  div.setAttribute('role', 'alert');
  div.innerText = msg;

  const btn = document.createElement('button');
  btn.setAttribute('class', 'btn-close');
  btn.setAttribute('data-bs-dismiss', 'alert');
  btn.setAttribute('aria-label', 'Close');

  div.append(btn);
  flashMsg.append(div);
}

function refreshCurrentFolder(newName, folderId, parentId) {
  currentFolderName.innerText = newName;
  currentFolder.setAttribute('folder_id', folderId);
  currentFolder.setAttribute('parent_id', parentId);
}

async function refreshFolderContent(folderId) {
  const folder = await contentFolderResponse(folderId);

  removeChilds(folderContentContainer);

  if (folder.data.success) {
    const { name, id, parent_id, children, files } = folder.data.data;
    refreshCurrentFolder(name, id, parent_id);

    for (let child of children.sort((a, b) => (a.name > b.name ? 1 : -1))) {
      let folder = addChild(`${child.name}`, `${child.id}`, true);
      folder.addEventListener('click', openFolder);
      folderContentContainer.append(folder);
    }

    for (let file of files.sort((a, b) => (a.name > b.name ? 1 : -1))) {
      let f = addFile(`${file.name}`, `${file.id}`, true);
      folderContentContainer.appendChild(f);
    }
  }
}

async function sendFolder(event) {
  const newName = folderNameInput.value;

  const formData = new FormData();
  formData.append('name', newName);
  folderNameInput.value = '';

  if (newName !== '') {
    const method = sendButtonModal.innerText === 'New' ? 'POST' : 'PUT';
    const result = folderResponse(method, formData);

    result
      .then(function (response) {
        const { success, msg, category } = response.data;

        if (success) {
          modalFolder.hide();
          // flashMessage(msg, category);

          const folderId = currentFolder.getAttribute('folder_id');
          const parentId = currentFolder.getAttribute('parent_id');

          if (method === 'POST') {
            refreshFolderContent(folderId);
          } else {
            refreshCurrentFolder(newName, folderId, parentId);
          }
        } else {
          const msgLI = document.querySelector('#modal_msg');
          msgLI.textContent = msg;
        }
      })
      .catch(function (error) {
        console.log(error);
      });
  }
}

sendButtonModal.addEventListener('click', sendFolder);
folderNameInput.addEventListener('keypress', function (event) {
  if (event.keyCode === 13) {
    sendFolder(event)
  }
});

function addChild(name, folderId, clone = false) {
  let child = clone ? folderShape.cloneNode(true) : folderShape;
  child.setAttribute('folder_id', folderId);
  child.lastElementChild.innerText = name;

  return child;
}

function addFile(name, fileId, clone = false) {
  const file = clone ? fileShape.cloneNode(true) : fileShape;
  file.setAttribute('file_id', fileId);
  file.lastElementChild.innerText = name;

  return file;
}

backButton.addEventListener('click', backParentFolder);
function backParentFolder(event) {
  event.stopImmediatePropagation();
  currentFolder = document.querySelector('#current_folder');
  const folderId = currentFolder.getAttribute('parent_id');
  if (folderId !== 'null') {
    refreshFolderContent(folderId);
  }
}

window.onload = refreshFolderContent(folderId);
