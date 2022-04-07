// Current folder
let currentFolder = document.querySelector('#current_folder');
const currentFolderName = document.querySelector('#current_folder_name');
const newFolder = document.querySelector('#new_folder');

// General
const projectId = currentFolder.getAttribute('project_id');
const folderId = currentFolder.getAttribute('folder_id');
const baseURL = `http://localhost:5000/projects/project`;

// Folder Modal
const folderModal = document.querySelector('#FolderModal');
const title = document.querySelector('#FolderModalLabel');
const modalFolder = bootstrap.Modal.getOrCreateInstance(folderModal);
const folderNameInput = document.querySelector('#folder_name');
const sendButtonFolderModal = document.querySelector('#send_folder');

// Delete Folder Modal
const deleteFolderModal = document.querySelector('#deleteFolderModal');
const modalDeleteFolder =
  bootstrap.Modal.getOrCreateInstance(deleteFolderModal);

// File Modal
const renameFileModal = document.querySelector('#FileModal');
const modalRenameFile = bootstrap.Modal.getOrCreateInstance(renameFileModal);
const sendButtonFileModal = document.querySelector('#send_file');
const fileNameInput = document.querySelector('#file_name');

// Delete File modal
const deleteFileModal = document.querySelector('#deleteFileModal');
const modalDeleteFile = bootstrap.Modal.getOrCreateInstance(deleteFileModal);

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
  const url = `${baseURL}/${projectId}/${folderId}/files/upload`;

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
  const folderMsgLi = document.querySelector('#folder_modal_msg');
  folderMsgLi.textContent = '';
  folderNameInput.value = '';
});

newFolder.addEventListener('click', function (event) {
  event.preventDefault();
  event.stopImmediatePropagation();

  title.innerText = 'New Folder';
  sendButtonFolderModal.innerText = 'New';
  modalFolder.show();
});

function renameFolderListener(event) {
  event.preventDefault();
  event.stopImmediatePropagation();

  title.innerText = 'Rename Folder';
  folderNameInput.value = this.getAttribute('data_name');
  const folderId = this.getAttribute('folder_id');
  const parentId = this.getAttribute('parent_id');

  sendButtonFolderModal.setAttribute('folder_id', folderId);
  sendButtonFolderModal.setAttribute('parent_id', parentId);
  sendButtonFolderModal.innerText = 'Rename';
  modalFolder.show();
}

const deleteFolderConfirmation = document.querySelector(
  '#delete_folder_confirmation'
);
deleteFolderConfirmation.addEventListener('click', function (event) {
  event.stopImmediatePropagation();

  const folderId = this.getAttribute('folder_id');
  const parentId = this.getAttribute('parent_id');

  const result = folderResponse('DELETE', folderId);

  result
    .then(function (response) {
      const { success, msg, category } = response.data;
      modalDeleteFolder.hide();
      flashMessage(msg, category);
      if (success) {
        refreshFolderContent(parentId);
      }
    })
    .catch(function (error) {
      console.log(error);
    });
});

function deleteFolderListener (event) {
  event.stopImmediatePropagation();

  const folderId = this.getAttribute('folder_id');
  const parentId = this.getAttribute('parent_id');

  deleteFolderConfirmation.setAttribute('folder_id', folderId);
  deleteFolderConfirmation.setAttribute('parent_id', parentId);

  modalDeleteFolder.show();
};

const folderResponse = async function (method, folderId, data = null) {
  try {
    const res = await axios({
      method: method,
      url: `${baseURL}/${projectId}/folders/${folderId}`,
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
      let folder = addChild(`${child.name}`, `${child.id}`,  id, true);
      folder.addEventListener('click', openFolder);
      folderContentContainer.append(folder);
    }

    for (let file of files.sort((a, b) => (a.name > b.name ? 1 : -1))) {
      let f = addFile(`${file.name}`, `${file.id}`, true);
      folderContentContainer.appendChild(f);
    }
  }
}

async function sendFolder() {
  const newName = folderNameInput.value;

  const formData = new FormData();
  formData.append('name', newName);
  folderNameInput.value = '';

  if (newName !== '') {
    const method = sendButtonFolderModal.innerText === 'New' ? 'POST' : 'PUT';
    const folderId = method === 'POST'  ? currentFolder.getAttribute('folder_id') : sendButtonFolderModal.getAttribute('folder_id');
    let result = folderResponse(method, folderId, formData);

    result
      .then(function (response) {
        const { success, msg, category } = response.data;

        if (success) {
          modalFolder.hide();
          // flashMessage(msg, category);

          const folderId = currentFolder.getAttribute('folder_id');
          const parentId = currentFolder.getAttribute('parent_id');

          // if (method === 'POST') {
            refreshFolderContent(folderId);
          // } else {
          //   refreshCurrentFolder(newName, folderId, parentId);
          // }
        } else {
          const folderMsgLi = document.querySelector('#folder_modal_msg');
          folderMsgLi.textContent = msg;
        }
      })
      .catch(function (error) {
        console.log(error);
      });
  }
}

sendButtonFolderModal.addEventListener('click', sendFolder);
folderNameInput.addEventListener('keypress', function (event) {
  if (event.keyCode === 13) {
    sendFolder();
  }
});

function addChild(name, folderId, parentId, clone = false) {
  let child = clone ? folderShape.cloneNode(true) : folderShape;
  child.setAttribute('folder_id', folderId);

  child.children[0].children[0].classList.add('folder-bg')
  child.lastElementChild.innerText = name;

  let linkBtns = child.querySelectorAll('button');
  const rename = linkBtns[0];
  rename.setAttribute('folder_id', folderId);
  rename.setAttribute('parent_id', parentId);
  rename.setAttribute('data_name', name);

  rename.addEventListener('click', renameFolderListener);

  const remove = linkBtns[1];
  remove.setAttribute('folder_id', folderId);
  remove.setAttribute('parent_id', parentId);
  remove.addEventListener('click', deleteFolderListener)

  return child;
}

function sendFile(event) {
  const newName = fileNameInput.value;

  const folderId = sendButtonFileModal.getAttribute('folder_id');
  const fileId = sendButtonFileModal.getAttribute('file_id');

  const url = `${baseURL}/${projectId}/${folderId}/files/${fileId}`;

  const formData = new FormData();
  formData.append('name', newName);

  if (newName !== '') {
    const method = 'PUT';
    const result = fileResponse(url, method, formData);

    result
      .then(function (response) {
        const { success, msg, category } = response.data;

        if (success) {
          fileNameInput.value = '';
          modalRenameFile.hide();
          // flashMessage(msg, category);

          refreshFolderContent(folderId);
        } else {
          const fileMsgLi = document.querySelector('#file_modal_msg');
          fileMsgLi.textContent = msg;
        }
      })
      .catch(function (error) {
        console.log(error);
      });
  }
}

sendButtonFileModal.addEventListener('click', sendFile);
fileNameInput.addEventListener('keypress', function (event) {
  if (event.keyCode === 13) {
    sendFile(event);
  }
});

renameFileModal.addEventListener('shown.bs.modal', function (event) {
  fileNameInput.focus();
});

renameFileModal.addEventListener('hidden.bs.modal', function (event) {
  const fileMsgLi = document.querySelector('#file_modal_msg');
  fileMsgLi.textContent = '';
  fileNameInput.value = '';
});

const fileResponse = async function (url, method, data = null) {
  try {
    const res = await axios({
      url: url,
      method: method,
      data: data,
    });

    return res;
  } catch (e) {
    console.log(e);
  }
};

async function renameFileListener(event) {
  event.preventDefault();
  event.stopImmediatePropagation();
  fileNameInput.value = this.getAttribute('data_name');

  const folderId = this.getAttribute('folder_id');
  const fileId = this.getAttribute('file_id');

  sendButtonFileModal.setAttribute('folder_id', folderId);
  sendButtonFileModal.setAttribute('file_id', fileId);

  modalRenameFile.show();
}

const deleteFileConfirmation = document.querySelector('#delete_file_confirmation');
deleteFileConfirmation.addEventListener('click', function (event) {
  event.stopImmediatePropagation();

  const folderId = this.getAttribute('folder_id');
  const fileId = this.getAttribute('file_id');

  const url = `${baseURL}/${projectId}/${folderId}/files/${fileId}`;
  const result = fileResponse(url, 'DELETE');

  result
    .then(function (response) {
      const { success, msg, category } = response.data;
      modalDeleteFile.hide();
      flashMessage(msg, category);
      if (success) {
        refreshFolderContent(folderId);
      }
    })
    .catch(function (error) {
      console.log(error);
    });
});

function deleteFileListener(event) {
  event.preventDefault();
  event.stopImmediatePropagation();

  const folderId = this.getAttribute('folder_id');
  const fileId = this.getAttribute('file_id');

  deleteFileConfirmation.setAttribute('folder_id', folderId);
  deleteFileConfirmation.setAttribute('file_id', fileId);

  modalDeleteFile.show();
}

function addFile(name, fileId, clone = false) {
  const file = clone ? fileShape.cloneNode(true) : fileShape;
  const folderId = currentFolder.getAttribute('folder_id');
  file.children[0].children[0].classList.add('file-bg');

  // file.setAttribute('file_id', fileId);
  file.lastElementChild.innerText = name;

  let linkBtns = file.querySelectorAll('button');
  const rename = linkBtns[0];
  rename.setAttribute('data_name', name);
  rename.setAttribute('folder_id', folderId);
  rename.setAttribute('file_id', fileId);

  rename.addEventListener('click', renameFileListener);

  const remove = linkBtns[1];
  remove.setAttribute('folder_id', folderId);
  remove.setAttribute('file_id', fileId);
  remove.addEventListener('click', deleteFileListener);

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
