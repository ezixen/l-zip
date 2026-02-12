// Auto-detect AI sites and auto-enable L-ZIP translation
(() => {
  // Firefox/Chrome compatibility
  const browserAPI = typeof browser !== 'undefined' ? browser : chrome;

  const AI_SITES = [
    'chat.openai.com',
    'chatgpt.com',
    'claude.ai',
    'gemini.google.com',
    'copilot.microsoft.com',
    'x.com/i/grok',
    'github.com/copilot',
    'ai.meta.com'
  ];

  let state = {
    enabled: false,
    autoEnabled: false,
    warned: false
  };

  function isAISite() {
    const hostname = window.location.hostname;
    const path = window.location.pathname;
    return AI_SITES.some(site => {
      const parts = site.split('/');
      if (parts.length === 1) {
        return hostname === site || hostname.endsWith('.' + site);
      } else {
        return (hostname === parts[0] || hostname.endsWith('.' + parts[0])) &&
               path.startsWith('/' + parts.slice(1).join('/'));
      }
    });
  }

  function warn() {
    if (state.warned) return;
    state.warned = true;
    console.log('[L-ZIP Auto] Enabled on', window.location.hostname);
  }

  function findInputs() {
    const inputs = [];
    
    // Common AI site patterns
    const selectors = [
      'textarea[placeholder*="message"]',
      'textarea[placeholder*="prompt"]',
      'textarea[id*="prompt"]',
      'textarea[class*="prompt"]',
      'div[contenteditable="true"][role="textbox"]',
      'div[contenteditable="true"]'
    ];
    
    selectors.forEach(selector => {
      document.querySelectorAll(selector).forEach(el => {
        if (!inputs.includes(el)) {
          inputs.push(el);
        }
      });
    });
    
    return inputs;
  }

  function getInputValue(el) {
    if (el.tagName === 'TEXTAREA' || el.tagName === 'INPUT') {
      return el.value;
    } else if (el.contentEditable === 'true') {
      return el.innerText || el.textContent;
    }
    return '';
  }

  function setInputValue(el, value) {
    if (el.tagName === 'TEXTAREA' || el.tagName === 'INPUT') {
      el.value = value;
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
    } else if (el.contentEditable === 'true') {
      el.innerText = value;
      el.dispatchEvent(new Event('input', { bubbles: true }));
    }
  }

  function translateInput(el) {
    const text = getInputValue(el);
    if (!text || text.trim() === '') return false;
    
    const translated = LZIPTranslator.compress(text);
    setInputValue(el, translated);
    return true;
  }

  function translateAll() {
    const inputs = findInputs();
    let translated = false;
    inputs.forEach(el => {
      if (translateInput(el)) {
        translated = true;
      }
    });
    return translated;
  }

  function handleKeydown(e) {
    if (!state.enabled) return;
    
    // Translate on Enter without Shift
    if (e.key === 'Enter' && !e.shiftKey) {
      setTimeout(() => {
        translateInput(e.target);
      }, 0);
    }
  }

  function attachListeners() {
    const inputs = findInputs();
    inputs.forEach(el => {
      el.removeEventListener('keydown', handleKeydown);
      el.addEventListener('keydown', handleKeydown);
    });
    
    // Re-attach when DOM changes
    const observer = new MutationObserver(() => {
      const newInputs = findInputs();
      newInputs.forEach(el => {
        el.removeEventListener('keydown', handleKeydown);
        el.addEventListener('keydown', handleKeydown);
      });
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  // Auto-enable on AI sites
  if (isAISite()) {
    state.enabled = true;
    state.autoEnabled = true;
    warn();
    attachListeners();
  }

  // Listen to popup messages
  browserAPI.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.type === 'getStatus') {
      sendResponse({
        enabled: state.enabled,
        autoEnabled: state.autoEnabled
      });
    } else if (msg.type === 'setEnabled') {
      state.enabled = Boolean(msg.enabled);
      if (state.enabled) {
        warn();
        attachListeners();
      }
      sendResponse({ enabled: state.enabled });
    } else if (msg.type === 'translateNow') {
      const ok = translateAll();
      sendResponse({ ok });
    }
    return true;
  });
})();
