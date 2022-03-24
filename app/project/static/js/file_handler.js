const tree = document.querySelector('#tree');

window.onload = function () {
  const root = JSON.parse(tree.querySelector('#tree_root').value);
  addTreeView([{ id: root.id, name: root.name }], [], tree);
};

function addTreeView(children, files, folderContent) {
  for (let child of children) {
    const divWrapper = document.createElement('div');
    divWrapper.classList.add('folder_wrapper');
    divWrapper.setAttribute('id', child.id);
    divWrapper.addEventListener('click', expandCollapseToggler);

    const li = document.createElement('li');
    li.classList.add('folder');
    li.innerText = child.name;
    divWrapper.append(li);


    const ul = document.createElement('ul');
    ul.classList.add('folder_content');
    ul.classList.add('fa-ul');
    divWrapper.append(ul);

    folderContent.append(divWrapper);
  }

  for (let file of files) {
    const li = document.createElement('li');
    li.setAttribute('id', file.id);
    li.innerText = file.name;
    folderContent.append(li);
  }
}

async function expandCollapseToggler(event) {
  event.stopPropagation();
  const folderContent = this.querySelector('.folder_content');
  const content = event.target.parentElement.lastChild;
  if (folderContent.innerHTML === '') {
    const url = `${document.URL}/data/${this.id}`;
    try {
      const { data } = await axios.get(url);
      addTreeView(data.children, data.files, folderContent);
    } catch (e) {
      console.log('Error in getContent:', e);
    }
  } else {
    content.toggleAttribute('hidden');
  }
}
