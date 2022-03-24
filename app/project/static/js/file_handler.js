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

  for (let file of files) {
    const li = document.createElement('li');
    li.setAttribute('id', file.id);
    li.innerText = file.name;
    folderContent.append(li);
  }
}

async function expandCollapseToggler(event) {
  event.stopPropagation();
  const id = event.target.parentNode.id;
  const content = event.target.parentNode.lastChild

  if (content.innerHTML === '') {
    const url = `${document.URL}/data/${id}`;
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
