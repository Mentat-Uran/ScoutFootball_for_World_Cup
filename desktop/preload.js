/* ScoutFootball Desktop — Preload Script */

const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("scoutDesktop", {
  version: process.env.npm_package_version || "1.0.3",
  platform: process.platform,
  isDesktop: true,

  // App info
  getAppVersion: () => ipcRenderer.invoke("get-app-version"),
  getPlatform: () => process.platform,

  // Update controls
  checkForUpdates: () => ipcRenderer.invoke("check-for-updates"),
  installUpdate: () => ipcRenderer.invoke("install-update"),

  // Window controls
  minimize: () => ipcRenderer.invoke("minimize-window"),
  maximize: () => ipcRenderer.invoke("maximize-window"),
  close: () => ipcRenderer.invoke("close-window"),

  // Logging
  log: (msg) => ipcRenderer.send("log", msg),
});

// Inject API base URL so frontend fetches go to the backend (port 8600),
// not the frontend static server (port 8601).
contextBridge.exposeInMainWorld("__SCOUTFOOTBALL_API__", "http://127.0.0.1:8600");
contextBridge.exposeInMainWorld("__SCOUTFOOTBALL_DESKTOP__", true);
