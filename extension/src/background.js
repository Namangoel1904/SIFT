// Background service worker for SIFT extension

const CONTEXT_MENU_ID = "sift-analyze";
const API_URL = "http://localhost:8000";

// Create context menu on installation
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: CONTEXT_MENU_ID,
    title: "Analyze with SIFT",
    contexts: ["selection"]
  });
  console.log("SIFT extension installed - context menu created");
});

// Handle context menu click
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === CONTEXT_MENU_ID && info.selectionText) {
    const selectedText = info.selectionText.trim();
    const url = info.pageUrl || tab.url;
    
    if (selectedText.length < 10) {
      console.warn("Selected text too short");
      return;
    }
    
    // Open sidebar
    chrome.tabs.sendMessage(tab.id, { action: "openSidebar" }).catch(() => {
      console.log("Content script not ready");
    });
    
    // Send analysis request
    chrome.tabs.sendMessage(tab.id, { action: "analyzeText", text: selectedText, url: url }).catch(() => {
      // If content script isn't ready, store in storage
      chrome.storage.local.set({
        pendingAnalysis: { text: selectedText, url: url }
      });
    });
    
    // Also send directly to storage for sidebar to pick up
    chrome.storage.local.set({
      pendingAnalysis: { text: selectedText, url: url }
    });
  }
});

// Handle extension icon click - open sidebar to home screen
chrome.action.onClicked.addListener((tab) => {
  // Inject content script if not already injected
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ['src/content-script.js']
  }).catch(() => {
    // Script may already be injected, try sending message
  });
  
  // Send message to open sidebar
  setTimeout(() => {
    chrome.tabs.sendMessage(tab.id, { action: "openSidebar" }).catch((error) => {
      console.log("SIFT: Content script not ready, retrying...", error);
      // Retry after a short delay
      setTimeout(() => {
        chrome.tabs.sendMessage(tab.id, { action: "openSidebar" }).catch(() => {
          console.error("SIFT: Failed to open sidebar");
        });
      }, 500);
    });
  }, 100);
});

// Listen for messages from content script or sidebar
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "analyze") {
    handleAnalyze(request.text, request.url)
      .then(result => {
        // Send result to sidebar
        chrome.storage.local.set({ analysisResult: result });
        sendResponse({ success: true, data: result });
      })
      .catch(error => {
        console.error("Analysis error:", error);
        chrome.storage.local.set({ 
          analysisError: error.message || "Analysis failed" 
        });
        sendResponse({ success: false, error: error.message });
      });
    return true; // Keep channel open for async response
  }
});

// Analyze text using backend API
async function handleAnalyze(text, url = null) {
  try {
    const response = await fetch(`${API_URL}/api/v1/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text, url })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to analyze text");
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

// Get API URL from storage (for user configuration)
async function getAPIUrl() {
  const result = await chrome.storage.sync.get(["apiUrl"]);
  return result.apiUrl || API_URL;
}
