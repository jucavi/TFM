const tree = document.querySelector('#tree');
const baseURL = document.URL;

window.onload = function () {
  const root = tree.querySelector('li');
  root.addEventListener('click', expandCollapseToggler);
};

async function expandCollapseToggler(event) {
  event.stopPropagation();
  const id = event.target.parentNode.id;
  const content = event.target.parentNode.lastElementChild;

  if (content.innerHTML === '') {
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

// function createLink(name, url) {
//   const a = document.createElement('a');
//   a.innerText = name;
//   a.href = url;
//   a.classList.add('btn');
//   a.classList.add('btn-info');

//   return a;
// }

function addFolders(children, folderContent) {
  for (let child of children) {
    const divWrapper = document.createElement('div');
    divWrapper.classList.add('folder_wrapper');
    divWrapper.setAttribute('id', child.id);

    // const url = `${baseURL}/folder/${child.id}?name=${child.name}-newFolderJS`
    // const renameLink = createLink('Rename', '#');
    // const deleteLink = createLink('Delete', '#');
    // const addFolderLink = createLink('Add Folder', url);

    const li = document.createElement('li');
    li.classList.add('folder');
    li.innerText = child.name;
    li.addEventListener('click', expandCollapseToggler);
    divWrapper.append(li);

    // divWrapper.append(addFolderLink);
    // divWrapper.append(renameLink);
    // divWrapper.append(deleteLink);

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
  addFolders(children, folderContent);
  addFiles(files, folderContent);
}
