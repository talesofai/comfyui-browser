import { app } from "../../scripts/app.js";
import { $el, ComfyDialog } from "../../scripts/ui.js";
import { api } from "../../scripts/api.js";

const browserUrl = "./browser/web/index.html";

const localStorageKey = 'comfyui-browser';

// Glassmorphism + rounded-corner polish for the modal frame (parent page).
// Solid dark background: prevents any white box from showing through.
const modalFrameStyles = `
/* ComfyUI-Browser: glass modal frame */
#comfy-browser-dialog {
  border-radius: 20px !important;
  border: 1px solid rgba(255, 255, 255, 0.18);
  background: #111a16 !important;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.55), 0 2px 8px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
}
/* Bottom action row (Close / Browse in new tab / Side-Center):
   spaced like the card buttons for visual consistency */
#comfy-browser-dialog .comfy-modal-content > div {
  display: flex;
  gap: 8px;
  justify-content: center;
  align-items: center;
}
#comfy-browser-dialog button {
  border-radius: 0.625rem !important;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(255, 255, 255, 0.09);
  padding: 0.3rem 0.75rem;
  font-size: 0.85rem;
  font-weight: 600;
  line-height: 1.4;
  cursor: pointer;
  transition: background 0.15s ease, border-color 0.15s ease;
}
#comfy-browser-dialog button:hover {
  background: rgba(255, 255, 255, 0.18);
  border-color: rgba(255, 255, 255, 0.28);
}
`;

/* Rounded corners + glassmorphism for the browser app inside the
   (same-origin) iframe. Keep in sync with svelte/src/app.sass and the
   appended block in web/build/_app/immutable/assets/*.css.
   The app background is kept solid dark so no white can ever show through. */
const browserAppStyles = `
/* ComfyUI-Browser: rounded corners everywhere + glassmorphism */
:root,
html[data-theme="forest"] {
  --rounded-box: 1rem;
  --rounded-btn: 0.625rem;
  --rounded-badge: 9999px;
}

/* Solid dark app background: never white, regardless of theme or oklch
   support. (The modal frame is opaque too, so no white can ever appear.) */
html[data-theme="forest"],
body {
  background-color: #111a16 !important;
}

/* Square image thumbnails: the image fills the box so its corners reach the
   rounded clip (object-fit: contain letterboxes, leaving square corners). */
.grid > .bg-info-content > div.flex > div {
  height: auto !important;
  aspect-ratio: auto !important;
}
.grid > .bg-info-content img,
.grid > .bg-info-content video {
  height: auto !important;
  width: 100% !important;
}
/* Small side thumbnails (collections list): fill the tile so corners round */
ul > li.bg-info-content img,
ul > li.bg-info-content video {
  object-fit: cover !important;
}
/* Don't stretch tiles to equal heights when image ratios differ */
.grid.grid-cols-4 {
  align-items: start;
}

/* File tiles: rounded + glassy */
.bg-info-content {
  border-radius: 0.75rem !important;
  overflow: hidden !important;
  background: rgba(255, 255, 255, 0.07) !important;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Rounded image / video previews */
.bg-info-content img,
.bg-info-content video {
  border-radius: 0.5rem !important;
}

/* Info box: name / date / size (outputs grid) */
.grid > .bg-info-content > p {
  margin: 0 !important;
  padding: 0.2rem 0.5rem !important;
  background: rgba(0, 0, 0, 0.35) !important;
}
.grid > .bg-info-content > p.font-bold {
  border-radius: 0.5rem 0.5rem 0 0 !important;
  margin-top: 0.5rem !important;
}
.grid > .bg-info-content > p:last-of-type {
  border-radius: 0 0 0.5rem 0.5rem !important;
  margin-bottom: 0.5rem !important;
}

/* Collections: filename input & date/size chip */
.bg-info-content .input-bordered,
.bg-info-content .textarea {
  border-radius: 0.5rem !important;
}
.bg-info-content div > p.text-gray-500 {
  background: rgba(0, 0, 0, 0.35);
  border-radius: 0.5rem;
  padding: 0.15rem 0.5rem;
  display: inline-block;
}

/* Load / Save / Delete as rounded buttons */
.bg-info-content .btn-link {
  display: inline-flex !important;
  align-items: center;
  gap: 0.25rem;
  height: auto !important;
  padding: 0.3rem 0.75rem !important;
  border-radius: 0.625rem !important;
  border: 1px solid rgba(255, 255, 255, 0.14) !important;
  background: rgba(255, 255, 255, 0.09) !important;
  text-decoration: none !important;
  font-weight: 600;
  font-size: 0.8rem;
  line-height: 1.4 !important;
  transition: background 0.15s ease, border-color 0.15s ease;
}
.bg-info-content .btn-link:hover {
  background: rgba(255, 255, 255, 0.18) !important;
  border-color: rgba(255, 255, 255, 0.28) !important;
}
.bg-info-content .btn-link.text-error {
  background: rgba(255, 107, 107, 0.16) !important;
  border-color: rgba(255, 107, 107, 0.3) !important;
}
.bg-info-content .btn-link.text-error:hover {
  background: rgba(255, 107, 107, 0.3) !important;
}
/* Tidy the delete button spacing in the collections list */
.bg-info-content .ml-52 {
  margin-left: 0.5rem !important;
}

/* Navbar & drawer menus */
.menu,
.menu > li > * {
  border-radius: 0.625rem !important;
}
.menu.bg-base-200 {
  background: rgba(255, 255, 255, 0.06) !important;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

/* Top navbar buttons match the card buttons */
.menu.menu-horizontal > li > button {
  border-radius: 0.625rem !important;
  border: 1px solid rgba(255, 255, 255, 0.14) !important;
  background: rgba(255, 255, 255, 0.09) !important;
  padding: 0.3rem 0.75rem !important;
  margin: 0.25rem 0.15rem !important;
  font-weight: 600;
  font-size: 0.85rem;
  line-height: 1.4;
  color: inherit;
  transition: background 0.15s ease, border-color 0.15s ease;
}
.menu.menu-horizontal > li > button:hover {
  background: rgba(255, 255, 255, 0.18) !important;
  border-color: rgba(255, 255, 255, 0.28) !important;
}
.menu.menu-horizontal > li > button.active {
  background: rgba(255, 255, 255, 0.2) !important;
  border-color: rgba(255, 255, 255, 0.35) !important;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.15);
}

/* Inputs & textareas (undo hard-coded square corners) */
.input,
.input-bordered,
.textarea,
input[type="text"],
input[type="url"],
textarea {
  border-radius: 0.625rem !important;
}

/* Dropdowns */
.dropdown-content {
  border-radius: 0.75rem !important;
}

/* Dialogs (source editor / xyz plot) */
.modal-box {
  border-radius: 1.25rem !important;
  background: rgba(30, 41, 35, 0.85) !important;
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.12);
}

/* Toast alerts */
.alert {
  border-radius: 0.75rem !important;
  -webkit-backdrop-filter: blur(8px);
  backdrop-filter: blur(8px);
}

/* Breadcrumb path bar */
.breadcrumbs,
.breadcrumbs li > a {
  border-radius: 0.625rem;
}

/* Progress bars stay pill-shaped */
.progress {
  border-radius: 9999px !important;
}
`;

function getLocalConfig() {
  let localConfig = localStorage.getItem(localStorageKey);
  if (localConfig) {
    localConfig = JSON.parse(localConfig);
  } else {
    localConfig = {};
  }

  return localConfig;
}

function setLocalConfig(key, value) {
  let localConfig = getLocalConfig();
  localConfig[key] = value;
  localStorage.setItem(localStorageKey, JSON.stringify(localConfig));
}

class BrowserDialog extends ComfyDialog {
  constructor() {
    super();

    const localConfig = getLocalConfig();
    let modalStyle = {
      width: "70%",
      height: "80%",
      maxWidth: "100%",
      maxHeight: "100%",
      minWidth: "24%",
      minHeight: "24%",
      padding: "6px",
      zIndex: 1000,
      resize: 'auto',
      backgroundColor: "#111a16",
      borderRadius: "20px",
      overflow: "hidden",
      border: "1px solid rgba(255, 255, 255, 0.14)",
      boxShadow: "0 24px 64px rgba(0, 0, 0, 0.55)",
    };
    const cs = localConfig.modalStyles;
    if (cs) {
      modalStyle.left = cs.left;
      modalStyle.top = cs.top;
      modalStyle.transform = cs.transform;
      modalStyle.height = cs.height;
      modalStyle.width = cs.width;
    }

    const iframe = $el("iframe", {
      src: browserUrl + "?timestamp=" + Date.now(),
      style: {
        width: "100%",
        height: "100%",
        backgroundColor: "#111a16",
        border: "none",
      },
    });
    this.iframe = iframe;

    this.element = $el("div.comfy-modal", {
      id: "comfy-browser-dialog",
      parent: document.body,
      style: modalStyle,
    }, [
      $el("div.comfy-modal-content", {
        style: {
          width: "100%",
          height: "100%",
        },
      }, [
        iframe,
        ...this.createButtons(),
      ]),
		]);

    // Inject the rounded-corner polish and a refresh bridge into the browser
    // app once it loads (the iframe is same-origin, so its document is
    // directly accessible). The bridge makes sure the listing refreshes every
    // time the modal is shown, even if cross-window events are unreliable.
    iframe.addEventListener("load", () => {
      const doc = iframe.contentDocument || iframe.contentWindow?.document;
      if (doc?.head && !doc.getElementById("comfyui-browser-radius-style")) {
        const styleEl = doc.createElement("style");
        styleEl.id = "comfyui-browser-radius-style";
        styleEl.textContent = browserAppStyles;
        doc.head.appendChild(styleEl);
      }
      if (doc?.head && !doc.getElementById("comfyui-browser-refresh-bridge")) {
        const scriptEl = doc.createElement("script");
        scriptEl.id = "comfyui-browser-refresh-bridge";
        scriptEl.textContent = `
          (function() {
            function comfyuiBrowserRefresh() {
              try {
                window.dispatchEvent(new Event('comfyuiBrowserShow'));
                window.top.dispatchEvent(new Event('comfyuiBrowserShow'));
              } catch (e) {}
            }
            window.addEventListener('message', function(ev) {
              if (ev && ev.data && ev.data.type === 'comfyui-browser-refresh') {
                comfyuiBrowserRefresh();
              }
            });
          })();
        `;
        doc.head.appendChild(scriptEl);
      }
    });

    new ResizeObserver(
      this.onResize.bind(this)
    ).observe(this.element);
  }

  createButtons() {
    const closeBtn = $el("button", {
      type: "button",
      textContent: "Close",
      onclick: () => this.close(),
    });
    const browseBtn = $el("a", {
      href: browserUrl,
      target: "_blank",
    }, [
      $el("button", {
        type: "button",
        textContent: "Browse in new tab",
      }),
    ]);
    const toggleSidePanelBtn = $el("button", {
      type: "button",
      textContent: "Side/Center",
      onclick: () => this.toggleSidePanel(),
    });
    return [
      $el("div", {
        style: {
          marginTop: '10px'
        }
      }, [
        closeBtn,
        browseBtn,
        toggleSidePanelBtn,
        /*$el("span", {*/
          /*textContent: "Tips: press 'B' to toggle me",*/
          /*style: {*/
            /*color: "var(--input-text)",*/
            /*right: 0,*/
            /*position: "absolute",*/
            /*lineHeight: "28.5px",*/
            /*marginRight: "2px",*/
          /*},*/
        /*}),*/
      ]),
    ];
  }

  onResize() {
    const e = this.element;
    setLocalConfig('modalStyles', {
      left: e.style.left,
      top: e.style.top,
      transform: e.style.transform,
      height: e.style.height,
      width: e.style.width,
    });
  }

  toggleSidePanel() {
    const e = this.element;
    if (e.style.left === '0px') {
      e.style.left = '';
      e.style.top = '';
      e.style.transform = '';
      e.style.height = '85%';
      e.style.width = '80%';
    } else {
      e.style.left = '0px';
      e.style.top = '0px';
      e.style.transform = 'translate(-10px, -10px)';
      e.style.height = '100%';
      e.style.width = '32%';
    }

    setLocalConfig('modalStyles', {
      left: e.style.left,
      top: e.style.top,
      transform: e.style.transform,
      height: e.style.height,
      width: e.style.width,
    });
  }

  close() {
    this.element.style.display = "none";
  }

  show() {
    this.element.style.display = "flex";
    dispatchEvent(new Event('comfyuiBrowserShow'));
    // Second, guaranteed refresh channel: message the iframe directly.
    this.iframe?.contentWindow?.postMessage(
      { type: 'comfyui-browser-refresh' },
      '*'
    );
  }

  toggle() {
    const e = this.element;
    if (e.style.display === "none") {
      this.show();
    } else {
      this.close();
    }
  }
}

function showToast(text, onClick) {
  const toastId = 'comfy-browser-toast';
  let toast = document.getElementById(toastId);
  if (! toast) {
    toast = $el("p", {
      id: toastId,
      textContent: '',
      onclick: onClick,
      style: {
        position: 'fixed',
        top: '70%',
        left: '34%',
        zIndex: 999,
        backgroundColor: 'var(--comfy-menu-bg)',
        fontSize: '42px',
        color: 'green',
        padding: '8px',
        border: 'green',
        borderStyle: 'solid',
        borderRadius: '0.5rem',
        display: 'none',
      }
    });
    document.body.appendChild(toast);
  }

  toast.textContent = text;
  toast.style.display = 'block';

  setTimeout(() => {
    toast.style.display = 'none';
  }, 2000);
}

app.registerExtension({
  name: "ComfyUI.Browser",
  init() {
  },
  async setup() {
    // Rounded modal frame (parent page).
    $el("style", {
      textContent: modalFrameStyles,
      parent: document.head,
    });

    const browserDialog = new BrowserDialog();

    document.addEventListener('keydown', (event) => {
      if (event.key === 'b') {
        if (event.target.matches('input, textarea')) {
          return;
        }

        browserDialog.toggle();
        event.preventDefault();
      }
    });
 //  add event listener for ctrl+i
    document.addEventListener('keydown', (event) => {
      if (event.ctrlKey && event.key === 'i') {
        browserDialog.toggle();
        event.preventDefault();
      }
    })
    app.ui.menuContainer.appendChild(
      $el("div.comfy-list", {
        style: {
          width: "100%",
          "border-style": "none",
          "margin-bottom": "none",
        }
      }, [
        $el("button", {
          id: "comfyui-browser-button",
          textContent: "Browser",
          title: "Browse and manage your outputs and collections",
          style: {
            "font-size": "20px",
            color: "red !important",
            //color: "var(--descrip-text) !important",
            width: "80%",
          },
          onclick: () => { browserDialog.show() },
        }),
        $el("button", {
          id: "comfyui-browser-collect-button",
          textContent: "💾",
          title: "Save workflow to collections",
          style: {
            width: "20%",
            "font-size": "17px",
          },
          onclick: (e) => {
            const saveBtn = e.target;
            const originBtnStyle = saveBtn.style.cssText;

            let filename = "workflow.json";
            const promptFilename = app.ui.settings.getSettingValue(
              "Comfy.PromptFilename",
              true,
            );
            if (promptFilename) {
              filename = prompt("Collect workflow as:", filename);
              if (!filename) return;
              if (!filename.toLowerCase().endsWith(".json")) {
                filename += ".json";
              }
            }
            app.graphToPrompt().then(async p => {
              const json = JSON.stringify(p.workflow, null, 2); // convert the data to a JSON string
              const res = await api.fetchApi("/browser/collections/workflows", {
                method: "POST",
                body: JSON.stringify({
                  filename: filename,
                  content: json,
                }),
              });
              if (res.ok) {
                saveBtn.style = originBtnStyle + "border-color: green;";
                showToast(
                  'Saved. Click me to open.',
                  () => { browserDialog.show() },
                );
              } else {
                saveBtn.style = originBtnStyle + "border-color: red;";
              }
              setTimeout(() => {
                saveBtn.style = originBtnStyle;
              }, 1000);
            });
          },
        }),
      ])
    );

    try{
      // new menu based features
      // browser and save to collection button into new style menu
      let cbGroup = new (await import("../../scripts/ui/components/buttonGroup.js")).ComfyButtonGroup(
        new(await import("../../scripts/ui/components/button.js")).ComfyButton({
          action: () => {
            if(browserDialog)
              browserDialog.show();
          },
          tooltip: "Browse and manage your outputs and collections",
          content: "📚",
          // content: "🪟",
          // content: "Browser",
          // icon: "table",// cloud, folder, folder-open, table, database, server
					// classList: "comfyui-button comfyui-menu-mobile-collapse primary"
					classList: "comfyui-button comfyui-menu-mobile-collapse "
        }).element,
        new(await import("../../scripts/ui/components/button.js")).ComfyButton({
          action: (e) => {
            const saveBtn = e.target;
            const originBtnStyle = saveBtn.style.cssText;

            let filename = "workflow.json";
            const promptFilename = app.ui.settings.getSettingValue(
              "Comfy.PromptFilename",
              true,
            );
            if (promptFilename) {
              filename = prompt("Collect workflow as:", filename);
              if (!filename) return;
              if (!filename.toLowerCase().endsWith(".json")) {
                filename += ".json";
              }
            }
            app.graphToPrompt().then(async p => {
              const json = JSON.stringify(p.workflow, null, 2); // convert the data to a JSON string
              const res = await api.fetchApi("/browser/collections/workflows", {
                method: "POST",
                body: JSON.stringify({
                  filename: filename,
                  content: json,
                }),
              });
              if (res.ok) {
                saveBtn.style = originBtnStyle + "border-color: green;";
                showToast(
                  'Saved. Click me to open.',
                  () => { browserDialog.show() },
                );
              } else {
                saveBtn.style = originBtnStyle + "border-color: red;";
              }
              setTimeout(() => {
                saveBtn.style = originBtnStyle;
              }, 1000);
            });
          },
          tooltip: "Save workflow to collections",
          content: "💾",
          classList: "comfyui-button comfyui-menu-mobile-collapse "
        }).element
      );
      app.menu?.settingsGroup.element.before(cbGroup.element);

    }catch(exception){
      console.log('ComfyUI-Browser could not load new menu based features.');
    }
  },
});
