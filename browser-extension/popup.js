// Firefox/Chrome compatibility
const browserAPI = typeof browser !== 'undefined' ? browser : chrome;

function withActiveTab(callback) {
  browserAPI.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (!tabs || !tabs.length) {
      return;
    }
    callback(tabs[0]);
  });
}

function sendToTab(tabId, message, cb) {
  browserAPI.tabs.sendMessage(tabId, message, cb);
}

function setStatus(text) {
  const status = document.getElementById("status");
  status.textContent = "Status: " + text;
}

withActiveTab((tab) => {
  const toggle = document.getElementById("toggle");
  const translate = document.getElementById("translate");

  sendToTab(tab.id, { type: "getStatus" }, (resp) => {
    if (!resp) {
      setStatus("not available on this page");
      return;
    }
    toggle.checked = Boolean(resp.enabled);
    if (resp.autoEnabled) {
      setStatus("auto-enabled on AI site");
    } else {
      setStatus(resp.enabled ? "enabled" : "disabled");
    }
  });

  toggle.addEventListener("change", () => {
    sendToTab(tab.id, { type: "setEnabled", enabled: toggle.checked }, (resp) => {
      if (resp && resp.enabled) {
        setStatus("enabled");
      } else {
        setStatus("disabled");
      }
    });
  });

  translate.addEventListener("click", () => {
    sendToTab(tab.id, { type: "translateNow" }, (resp) => {
      if (!resp || !resp.ok) {
        setStatus("no input found");
        return;
      }
      setStatus("translated");
    });
  });
});
