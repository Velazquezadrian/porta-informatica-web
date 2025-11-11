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
  // Computadoras
  { test: n => /^pc\s*armada$/i.test(n), target: "computadoras", normalize: n => "PC Armada" },
  
  // Notebook
  { test: n => /^lenovo$/i.test(n), target: "notebook", normalize: n => "Lenovo" },
  { test: n => /^asus$/i.test(n), target: "notebook", normalize: n => "Asus" },
  { test: n => /^hp$/i.test(n), target: "notebook", normalize: n => "HP" },
  { test: n => /^dell$/i.test(n), target: "notebook", normalize: n => "Dell" },
  
  // Impresoras
  { test: n => /^laser$/i.test(n), target: "impresoras", normalize: n => "Laser" },
  { test: n => /^multifunci[oó]n$/i.test(n), target: "impresoras", normalize: n => "Multifunción" },
  { test: n => /^matricial$/i.test(n), target: "impresoras", normalize: n => "Matricial" },
  
  // Almacenamiento
  { test: n => /^(s[oó]lido|ssd)$/i.test(n), target: "almacenamiento", normalize: n => "SSD" },
  { test: n => /^(disco\s*duro|hdd)$/i.test(n), target: "almacenamiento", normalize: n => "Disco Duro" },
  { test: n => /^pendrive$/i.test(n), target: "almacenamiento", normalize: n => "Pendrive" },
  { test: n => /^(sd|tarjeta\s*sd)$/i.test(n), target: "almacenamiento", normalize: n => "Tarjeta SD" },
  { test: n => /^(portables?|discos?\s*externos?)$/i.test(n), target: "almacenamiento", normalize: n => "Discos Externos" },
  
  // Conectividad
  { test: n => /^router$/i.test(n), target: "conectividad", normalize: n => "Router" },
  { test: n => /^switch$/i.test(n), target: "conectividad", normalize: n => "Switch" },
  { test: n => /^extensores?\s*(wifi|de\s*rango)?$/i.test(n), target: "conectividad", normalize: n => "Extensores WiFi" },
  { test: n => /^(usb\s*wifi|adaptador\s*usb)$/i.test(n), target: "conectividad", normalize: n => "USB WiFi" },
  { test: n => /^(pci\s*wifi|placa\s*wifi)$/i.test(n), target: "conectividad", normalize: n => "PCI WiFi" },
  
  // Componentes de PC
  { test: n => /^procesadores?$/i.test(n), target: "componentes-cpu", normalize: n => "Procesadores" },
  { test: n => /^(motherboards?|mothers?)$/i.test(n), target: "componentes-cpu", normalize: n => "Motherboards" },
  { test: n => /^(memorias?(\s*ram)?|ram)$/i.test(n), target: "componentes-cpu", normalize: n => "Memorias RAM" },
  { test: n => /^(placas?\s*(de\s*)?video|gpu)$/i.test(n), target: "componentes-cpu", normalize: n => "Placas de Video" },
  { test: n => /^gabinetes?$/i.test(n), target: "componentes-cpu", normalize: n => "Gabinetes" },
  { test: n => /^fuentes?$/i.test(n), target: "componentes-cpu", normalize: n => "Fuentes" },
  { test: n => /^coolers?$/i.test(n), target: "componentes-cpu", normalize: n => "Coolers" },
  
  // Periféricos
  { test: n => /^mouse$/i.test(n), target: "perifericos", normalize: n => "Mouse" },
  { test: n => /^teclados?$/i.test(n), target: "perifericos", normalize: n => "Teclados" },
  { test: n => /^auriculares?$/i.test(n), target: "perifericos", normalize: n => "Auriculares" },
  { test: n => /^(webcam|c[aá]maras?\s*web)$/i.test(n), target: "perifericos", normalize: n => "Webcam" },
  { test: n => /^(parlantes?|altavoces?)$/i.test(n), target: "perifericos", normalize: n => "Parlantes" },
  { test: n => /^micr[oó]fonos?$/i.test(n), target: "perifericos", normalize: n => "Micrófonos" },
  { test: n => /^(joystick|gamepad)s?$/i.test(n), target: "perifericos", normalize: n => "Joystick" },
  
  // Insumos
  { test: n => /^cartuchos?$/i.test(n), target: "insumos", normalize: n => "Cartuchos" },
  { test: n => /^t[oó]ners?$/i.test(n), target: "insumos", normalize: n => "Tóners" },
  { test: n => /^(tintas?|botellas?\s*(de\s*)?tinta)$/i.test(n), target: "insumos", normalize: n => "Tintas" },
  
  // Gaming
  { test: n => /^(mouse\s*gamer|gaming\s*mouse)$/i.test(n), target: "gaming", normalize: n => "Mouse Gamer" },
  { test: n => /^(teclado\s*gamer|gaming\s*keyboard)$/i.test(n), target: "gaming", normalize: n => "Teclados Gamer" },
  { test: n => /^(auriculares?\s*gamer|gaming\s*headset)$/i.test(n), target: "gaming", normalize: n => "Auriculares Gamer" },
];

function addSubcategory(rawName){
  if(typeof rawName !== 'string') return false;
  const trimmed = rawName.trim();
  if(trimmed.length < 2) return false;
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

// Inicialización de subcategorías del menú
// Computadoras
addSubcategory('PC Armada');

// Notebook
addSubcategory('Lenovo');
addSubcategory('Asus');
addSubcategory('HP');
addSubcategory('Dell');

// Impresoras
addSubcategory('Laser');
addSubcategory('Multifunción');
addSubcategory('Matricial');

// Almacenamiento
addSubcategory('SSD');
addSubcategory('Disco Duro');
addSubcategory('Pendrive');
addSubcategory('Tarjeta SD');
addSubcategory('Discos Externos');

// Conectividad
addSubcategory('Router');
addSubcategory('Switch');
addSubcategory('Extensores WiFi');
addSubcategory('USB WiFi');
addSubcategory('PCI WiFi');

// Componentes de PC
addSubcategory('Procesadores');
addSubcategory('Motherboards');
addSubcategory('Memorias RAM');
addSubcategory('Placas de Video');
addSubcategory('Gabinetes');
addSubcategory('Fuentes');
addSubcategory('Coolers');

// Periféricos
addSubcategory('Mouse');
addSubcategory('Teclados');
addSubcategory('Auriculares');
addSubcategory('Webcam');
addSubcategory('Parlantes');
addSubcategory('Micrófonos');
addSubcategory('Joystick');

// Insumos
addSubcategory('Cartuchos');
addSubcategory('Tóners');
addSubcategory('Tintas');

// Gaming
addSubcategory('Mouse Gamer');
addSubcategory('Teclados Gamer');
addSubcategory('Auriculares Gamer');

renderMenu();

window.addSubcategory = addSubcategory;
