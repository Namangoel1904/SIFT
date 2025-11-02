// Content script for SIFT extension - handles text selection and sidebar injection

// Suppress errors from page scripts trying to access extension elements
const originalErrorHandler = window.onerror;
window.onerror = function(message, source, lineno, colno, error) {
  // Suppress mCustomScrollbar errors from page scripts
  if (message && typeof message === 'string' && message.includes('mCustomScrollbar')) {
    console.log('SIFT: Suppressed page script error:', message);
    return true; // Prevent error from being logged
  }
  // Call original error handler if it exists
  if (originalErrorHandler) {
    return originalErrorHandler.call(this, message, source, lineno, colno, error);
  }
  return false;
};

// Also catch unhandled promise rejections
window.addEventListener('error', (event) => {
  if (event.message && event.message.includes('mCustomScrollbar')) {
    event.stopPropagation();
    event.preventDefault();
    return false;
  }
}, true);

let selectedText = "";
let sidebarVisible = false;
let sidebarContainer = null;

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getSelection") {
    sendResponse({ text: selectedText, url: window.location.href });
    return true;
  }
  
  if (request.action === "clearSelection") {
    selectedText = "";
    sendResponse({ success: true });
    return true;
  }

  if (request.action === "openSidebar") {
    openSidebar();
    sendResponse({ success: true });
    return true;
  }

  if (request.action === "closeSidebar") {
    closeSidebar();
    sendResponse({ success: true });
    return true;
  }

  if (request.action === "analyzeText") {
    openSidebar();
    // The sidebar will pick up the analysis request from storage
    sendResponse({ success: true });
    return true;
  }
});

// Store selected text when user selects
document.addEventListener("mouseup", () => {
  const selection = window.getSelection();
  selectedText = selection.toString().trim();
});

// Also handle text selection via keyboard
document.addEventListener("keyup", (e) => {
  if (e.ctrlKey || e.metaKey || e.shiftKey) {
    const selection = window.getSelection();
    selectedText = selection.toString().trim();
  }
});

function createSidebar() {
  if (sidebarContainer) {
    // Sidebar already exists, just return it
    return sidebarContainer;
  }

  // Create sidebar in isolated context to prevent page script interference
  try {
    // Create overlay background with isolation
    const overlay = document.createElement('div');
    overlay.id = 'sift-overlay';
    overlay.setAttribute('data-sift-extension', 'true');
    overlay.setAttribute('data-no-scrollbar-init', 'true');
    overlay.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 2147483647;
    display: none;
    isolation: isolate;
    pointer-events: auto;
  `;

  // Prevent page scripts from accessing overlay with jQuery
  // Add property that page scripts might check for
  Object.defineProperty(overlay, 'mCustomScrollbar', {
    value: undefined,
    writable: false,
    configurable: false,
    enumerable: false
  });

  // Close on overlay click
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      closeSidebar();
    }
  });

  // Create sidebar container with isolation
  sidebarContainer = document.createElement('div');
  sidebarContainer.id = 'sift-sidebar';
  sidebarContainer.setAttribute('data-sift-extension', 'true');
  sidebarContainer.setAttribute('data-no-scrollbar-init', 'true');
  sidebarContainer.style.cssText = `
    position: fixed;
    top: 0;
    right: 0;
    width: 25%;
    min-width: 380px;
    max-width: 520px;
    height: 100vh;
    background: white;
    box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
    z-index: 2147483648;
    transform: translateX(100%);
    transition: transform 0.3s ease-out;
    overflow: hidden;
    isolation: isolate;
    pointer-events: auto;
  `;

  // Prevent page scripts from accessing sidebar with jQuery
  Object.defineProperty(sidebarContainer, 'mCustomScrollbar', {
    value: undefined,
    writable: false,
    configurable: false,
    enumerable: false
  });
  
  // Prevent jQuery from selecting our elements
  // Override common jQuery selectors if they exist
  if (window.$ || window.jQuery) {
    const originalJQ = window.$ || window.jQuery;
    // This won't fully prevent access but helps
    try {
      // Make our elements non-selectable by common patterns
      sidebarContainer.classList.add('sift-extension-element');
      overlay.classList.add('sift-extension-element');
    } catch (e) {
      // Ignore
    }
  }

  // Create iframe for React UI with proper isolation
  const iframe = document.createElement('iframe');
  iframe.id = 'sift-sidebar-iframe';
  // Remove sandbox attribute to allow full functionality
  // The iframe is already isolated by being in extension context
  iframe.style.cssText = `
    width: 100%;
    height: 100%;
    border: none;
    isolation: isolate;
  `;
  iframe.src = chrome.runtime.getURL('ui/index.html');
  
  // Add data attributes to prevent page scripts from targeting our elements
  iframe.setAttribute('data-sift-extension', 'true');
  iframe.setAttribute('data-no-scrollbar-init', 'true');

    sidebarContainer.appendChild(iframe);
    overlay.appendChild(sidebarContainer);
    document.body.appendChild(overlay);

    // Listen for close messages from iframe
    window.addEventListener('message', (e) => {
      if (e.data && e.data.action === 'closeSidebar') {
        closeSidebar();
      }
    });

    return sidebarContainer;
  } catch (error) {
    console.error('SIFT: Error creating sidebar:', error);
    return null;
  }
}

function openSidebar() {
  if (sidebarVisible) {
    return;
  }

  try {
    const container = createSidebar();
    const overlay = document.getElementById('sift-overlay');
    
    if (!overlay || !container) {
      console.error('SIFT: Failed to create sidebar elements');
      return;
    }
    
    overlay.style.display = 'block';
    
    // Use requestAnimationFrame for smoother animation
    requestAnimationFrame(() => {
      container.style.transform = 'translateX(0)';
    });
    
    sidebarVisible = true;
    
    // Prevent body scroll when sidebar is open
    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    document.body.setAttribute('data-sift-overflow', originalOverflow);
  } catch (error) {
    console.error('SIFT: Error opening sidebar:', error);
  }
}

function closeSidebar() {
  if (!sidebarVisible || !sidebarContainer) {
    return;
  }

  try {
    const container = sidebarContainer;
    const overlay = document.getElementById('sift-overlay');
    
    container.style.transform = 'translateX(100%)';
    
    setTimeout(() => {
      if (overlay) {
        overlay.style.display = 'none';
      }
      // Restore original overflow style
      const originalOverflow = document.body.getAttribute('data-sift-overflow');
      document.body.style.overflow = originalOverflow || '';
      document.body.removeAttribute('data-sift-overflow');
      sidebarVisible = false;
    }, 300);
  } catch (error) {
    console.error('SIFT: Error closing sidebar:', error);
    sidebarVisible = false;
  }
}

// Listen for extension icon click
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "toggleSidebar") {
    if (sidebarVisible) {
      closeSidebar();
    } else {
      openSidebar();
    }
    sendResponse({ success: true });
    return true;
  }
});
