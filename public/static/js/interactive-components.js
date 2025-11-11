/**
 * Componentes Interactivos - Porta Informática
 * Barra de progreso, scroll to top, tooltips y quick view
 */

document.addEventListener('DOMContentLoaded', function() {
  initScrollProgress();
  initScrollToTop();
  initQuickView();
});

/**
 * Barra de progreso al hacer scroll
 */
function initScrollProgress() {
  // Crear barra de progreso
  const progressBar = document.createElement('div');
  progressBar.className = 'scroll-progress-bar';
  progressBar.style.width = '0%';
  document.body.appendChild(progressBar);

  // Actualizar al hacer scroll
  window.addEventListener('scroll', function() {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight - windowHeight;
    const scrolled = window.scrollY;
    const progress = (scrolled / documentHeight) * 100;
    
    progressBar.style.transform = `scaleX(${progress / 100})`;
  });
}

/**
 * Botón "Volver arriba" con smooth scroll
 */
function initScrollToTop() {
  // Crear botón
  const scrollBtn = document.createElement('button');
  scrollBtn.className = 'scroll-to-top';
  scrollBtn.innerHTML = '↑';
  scrollBtn.setAttribute('aria-label', 'Volver arriba');
  document.body.appendChild(scrollBtn);

  // Mostrar/ocultar según scroll
  window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
      scrollBtn.classList.add('show');
    } else {
      scrollBtn.classList.remove('show');
    }
  });

  // Scroll suave al hacer click
  scrollBtn.addEventListener('click', function() {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

/**
 * Quick View Modal para productos
 * DESACTIVADO - No se requiere popup emergente
 */
function initQuickView() {
  // Funcionalidad desactivada por solicitud del usuario
  return;
  
  // Crear modal y overlay
  const overlay = document.createElement('div');
  overlay.className = 'quick-view-overlay';
  
  const modal = document.createElement('div');
  modal.className = 'quick-view-modal';
  modal.innerHTML = `
    <button class="quick-view-close" aria-label="Cerrar">&times;</button>
    <div class="quick-view-content">
      <img src="" alt="" class="quick-view-image">
      <div class="quick-view-info">
        <h3 class="quick-view-title"></h3>
        <p class="quick-view-price"></p>
        <p class="quick-view-stock"></p>
        <p class="quick-view-description"></p>
        <a href="#" class="btn btn-primary quick-view-link">Ver detalles completos</a>
      </div>
    </div>
  `;
  
  document.body.appendChild(overlay);
  document.body.appendChild(modal);

  // Cerrar modal
  function closeModal() {
    modal.classList.remove('show');
    overlay.classList.remove('show');
  }

  overlay.addEventListener('click', closeModal);
  modal.querySelector('.quick-view-close').addEventListener('click', closeModal);

  // Detectar hover prolongado en cards de productos
  const productCards = document.querySelectorAll('.producto-card');
  let hoverTimer;

  productCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      // Solo activar si tiene atributo data-quick-view
      if (!card.hasAttribute('data-quick-view-enabled')) return;

      hoverTimer = setTimeout(function() {
        showQuickView(card);
      }, 800); // Mostrar después de 800ms de hover
    });

    card.addEventListener('mouseleave', function() {
      clearTimeout(hoverTimer);
    });
  });

  function showQuickView(card) {
    // Extraer datos del producto
    const img = card.querySelector('.producto-img');
    const title = card.querySelector('.card-title');
    const price = card.querySelector('.producto-precio');
    const link = card.querySelector('.btn-primary');
    
    if (!img || !title || !price) return;

    // Llenar modal
    modal.querySelector('.quick-view-image').src = img.src;
    modal.querySelector('.quick-view-image').alt = title.textContent;
    modal.querySelector('.quick-view-title').textContent = title.textContent;
    modal.querySelector('.quick-view-price').textContent = price.textContent;
    
    // Stock (si existe)
    const stock = card.querySelector('.stock-indicator');
    if (stock) {
      modal.querySelector('.quick-view-stock').textContent = stock.textContent;
    } else {
      modal.querySelector('.quick-view-stock').textContent = 'Disponible';
    }

    // Descripción (si existe en data attribute)
    const description = card.getAttribute('data-description') || 
                       'Haz clic en "Ver detalles" para más información.';
    modal.querySelector('.quick-view-description').textContent = description;

    // Link
    if (link) {
      modal.querySelector('.quick-view-link').href = link.href;
    }

    // Mostrar modal
    overlay.classList.add('show');
    modal.classList.add('show');
  }

  // Cerrar con ESC
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      closeModal();
    }
  });
}

/**
 * Inicializar tooltips personalizados
 * Uso: <span class="tooltip-custom" data-tooltip="Texto del tooltip">Elemento</span>
 */
function initTooltips() {
  const tooltipElements = document.querySelectorAll('[data-tooltip]');
  
  tooltipElements.forEach(element => {
    element.classList.add('tooltip-custom');
    
    const tooltipText = document.createElement('span');
    tooltipText.className = 'tooltiptext';
    tooltipText.textContent = element.getAttribute('data-tooltip');
    
    element.appendChild(tooltipText);
  });
}

// Auto-inicializar tooltips
document.addEventListener('DOMContentLoaded', initTooltips);
