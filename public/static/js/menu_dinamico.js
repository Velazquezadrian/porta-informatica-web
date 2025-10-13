/* Menú dinámico de categorías y subcategorías
   - Genera dropdowns a partir de reglas
   - Evita duplicados
   - Excluye 'Tablets'
   - Expone addSubcategory en window
*/

const CATEGORIES = [
  { name: "Computadoras", key: "computadoras" },
  { name: "Notebook", key: "notebook" },
  { name: "Impresoras", key: "impresoras" },
  { name: "Almacenamiento", key: "almacenamiento" },
  { name: "Conectividad", key: "conectividad" },
  { name: "Componentes de PC", key: "componentes-cpu" },
  { name: "Periféricos", key: "perifericos" },
  { name: "Insumos", key: "insumos" },
  { name: "Gaming", key: "gaming" }
];

const CATEGORY_BUCKETS = Object.fromEntries(CATEGORIES.map(c => [c.key, new Set()]));

const SUBCATEGORY_RULES = [
  { test: n => n === "PC Armada", target: "computadoras", normalize: n => n },
  { test: n => n === "mouse", target: "perifericos", normalize: n => "Mouse" },
];

function addSubcategory(rawName){
  if(typeof rawName !== 'string') return false;
  const trimmed = rawName.trim();
  if(trimmed.length < 3) return false;
  for(const rule of SUBCATEGORY_RULES){
    if(rule.test(trimmed)){
      const bucket = CATEGORY_BUCKETS[rule.target];
      const norm = rule.normalize ? rule.normalize(trimmed) : trimmed;
      if(!bucket.has(norm)){
        bucket.add(norm);
        renderMenu();
        return true;
      }
      return false;
    }
  }
  return false; // ignorado
}

function slugify(str){
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g,'')
            .toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
}

function renderMenu(){
  const ul = document.getElementById('menu-categorias');
  if(!ul) return;
  ul.innerHTML = '';
  CATEGORIES.forEach(cat => {
    const subs = Array.from(CATEGORY_BUCKETS[cat.key]);
    const ddId = `dd-${cat.key}`;
    const li = document.createElement('li');
    li.className = 'nav-item dropdown';
    
    // Construir items del dropdown
    let dropdownItems = `<li><a class="dropdown-item fw-bold" href="/?categoria=${cat.name}">Ver todos</a></li>`;
    if(subs.length > 0){
      dropdownItems += '<li><hr class="dropdown-divider"></li>';
      dropdownItems += subs.map(s => `<li><a class=\"dropdown-item\" href=\"/c/${cat.key}/${slugify(s)}\">${s}</a></li>`).join('');
    }
    
    li.innerHTML = `
      <a class="nav-link dropdown-toggle" href="#" id="${ddId}" role="button" data-bs-toggle="dropdown" aria-expanded="false">${cat.name}</a>
      <ul class="dropdown-menu" aria-labelledby="${ddId}">
        ${dropdownItems}
      </ul>`;
    ul.appendChild(li);
  });
  enhanceAccessibility(ul);
}

function enhanceAccessibility(root){
  root.querySelectorAll('.dropdown').forEach(drop => {
    const toggle = drop.querySelector('.dropdown-toggle');
    const menu = drop.querySelector('.dropdown-menu');
    if(!toggle || !menu) return;
    toggle.addEventListener('keydown', e => {
      if(e.key === 'ArrowDown'){
        e.preventDefault();
        const first = menu.querySelector('.dropdown-item');
        if(first) first.focus();
      }
    });
    menu.addEventListener('keydown', e => {
      const items = Array.from(menu.querySelectorAll('.dropdown-item'));
      const idx = items.indexOf(document.activeElement);
      if(e.key === 'ArrowDown'){
        e.preventDefault();
        (items[idx+1] || items[0]).focus();
      } else if(e.key === 'ArrowUp'){
        e.preventDefault();
        (items[idx-1] || items[items.length-1]).focus();
      } else if(e.key === 'Escape'){
        toggle.focus();
        const inst = bootstrap.Dropdown.getInstance(toggle);
        if(inst) inst.hide();
      }
    });
  });
}

// Semillas iniciales
addSubcategory('PC Armada');
addSubcategory('mouse');
// Ejemplos ignorados / inconsistentes
addSubcategory('CPU Armadas'); // ignorado ahora
addSubcategory('cpu armada');  // ignorado
addSubcategory('CPU armadas'); // ignorado
addSubcategory('Mouse');       // ignorado (regla exige mouse minúscula)

renderMenu();

window.addSubcategory = addSubcategory;
