/**
 * Efectos de pulido y optimización - Fase D
 * Skeleton screens, lazy loading, intersection observer
 */

document.addEventListener('DOMContentLoaded', function() {
  initLazyLoading();
  initSkeletonScreens();
  initSectionAnimations();
  optimizeAnimations();
});

/**
 * Lazy loading de imágenes con skeleton
 */
function initLazyLoading() {
  const lazyImages = document.querySelectorAll('img[loading="lazy"]');
  
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          
          // Agregar skeleton mientras carga
          img.parentElement.classList.add('loading-image');
          
          img.addEventListener('load', function() {
            img.parentElement.classList.remove('loading-image');
            img.classList.add('loaded');
          });
          
          observer.unobserve(img);
        }
      });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
  }
}

/**
 * Skeleton screens para productos
 */
function initSkeletonScreens() {
  // Detectar cuando se están cargando productos dinámicamente
  const productContainers = document.querySelectorAll('.row.g-4');
  
  productContainers.forEach(container => {
    // Si el contenedor está vacío, mostrar skeletons
    if (container.children.length === 0) {
      showSkeletonProducts(container);
    }
  });
}

function showSkeletonProducts(container, count = 8) {
  const skeletonHTML = `
    <div class="col-lg-3 col-md-4 col-sm-6 col-6">
      <div class="card skeleton-card">
        <div class="skeleton skeleton-image"></div>
        <div class="card-body">
          <div class="skeleton skeleton-title"></div>
          <div class="skeleton skeleton-text"></div>
          <div class="skeleton skeleton-text" style="width: 60%;"></div>
        </div>
      </div>
    </div>
  `;
  
  for (let i = 0; i < count; i++) {
    container.insertAdjacentHTML('beforeend', skeletonHTML);
  }
}

function hideSkeletonProducts() {
  const skeletons = document.querySelectorAll('.skeleton-card');
  skeletons.forEach(skeleton => {
    skeleton.closest('.col-lg-3, .col-md-4, .col-sm-6').remove();
  });
}

/**
 * Animaciones de entrada para secciones con Intersection Observer
 */
function initSectionAnimations() {
  const sections = document.querySelectorAll('section');
  
  if ('IntersectionObserver' in window) {
    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('section-visible');
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });
    
    sections.forEach(section => {
      section.classList.add('section-hidden');
      sectionObserver.observe(section);
    });
  }
}

/**
 * Optimizar animaciones según el dispositivo
 */
function optimizeAnimations() {
  // Detectar dispositivos de bajo rendimiento
  const isLowPerformance = 
    navigator.hardwareConcurrency < 4 || 
    /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent);
  
  if (isLowPerformance) {
    document.documentElement.classList.add('low-performance');
  }
  
  // Detectar preferencia de reducción de movimiento
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  
  if (prefersReducedMotion.matches) {
    document.documentElement.classList.add('reduced-motion');
  }
  
  // Escuchar cambios en la preferencia
  prefersReducedMotion.addEventListener('change', (e) => {
    if (e.matches) {
      document.documentElement.classList.add('reduced-motion');
    } else {
      document.documentElement.classList.remove('reduced-motion');
    }
  });
}

/**
 * Mostrar overlay de loading global
 */
function showLoadingOverlay(message = 'Cargando...') {
  const overlay = document.createElement('div');
  overlay.className = 'loading-overlay active';
  overlay.innerHTML = `
    <div class="loading-container">
      <div class="loading-spinner"></div>
      <div class="loading-text">${message}</div>
    </div>
  `;
  document.body.appendChild(overlay);
  return overlay;
}

function hideLoadingOverlay(overlay) {
  if (overlay) {
    overlay.classList.remove('active');
    setTimeout(() => overlay.remove(), 300);
  }
}

/**
 * Efecto de feedback al agregar al carrito (mejorado)
 */
document.addEventListener('click', function(e) {
  if (e.target.classList.contains('agregar-pedido-btn') || 
      e.target.closest('.agregar-pedido-btn')) {
    
    const button = e.target.classList.contains('agregar-pedido-btn') 
      ? e.target 
      : e.target.closest('.agregar-pedido-btn');
    
    // Efecto de éxito visual
    button.classList.add('success-feedback');
    
    setTimeout(() => {
      button.classList.remove('success-feedback');
    }, 600);
  }
});

/**
 * Smooth scroll mejorado para anchors
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const href = this.getAttribute('href');
    if (href !== '#' && href !== '#0') {
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    }
  });
});

// Exportar funciones para uso externo
window.showLoadingOverlay = showLoadingOverlay;
window.hideLoadingOverlay = hideLoadingOverlay;
window.showSkeletonProducts = showSkeletonProducts;
window.hideSkeletonProducts = hideSkeletonProducts;
