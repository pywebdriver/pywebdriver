"use strict";

const STEPS = [
  "welcome",
  "network",
  "drivers",
  "driver_config",
  "ssl",
  "service",
  "summary",
];

window.APP_STATE = {
  locale: "es",
  bootstrap: null,
  state: null,
  driversMeta: [],
  hardware: { win32_printers: [], com_ports: [], usb_devices: [] },
  currentStep: 0,
  options: { generate_ssl: false, install_service: true, autostart: true },
  applied: false,
};

const apiReady = new Promise((resolve) => {
  if (window.pywebview && window.pywebview.api) {
    resolve();
  } else {
    window.addEventListener("pywebviewready", () => resolve());
  }
});

async function callApi(method, ...args) {
  await apiReady;
  const result = await window.pywebview.api[method](...args);
  if (!result || !result.ok) {
    const message = (result && result.error) || t("error_generic");
    throw new Error(message);
  }
  return result.data;
}

function $(sel) {
  return document.querySelector(sel);
}

function el(tag, attrs, children) {
  const node = document.createElement(tag);
  if (attrs) {
    Object.entries(attrs).forEach(([key, value]) => {
      if (key === "class") node.className = value;
      else if (key === "html") node.innerHTML = value;
      else if (key.startsWith("on") && typeof value === "function") {
        node.addEventListener(key.slice(2).toLowerCase(), value);
      } else if (typeof value === "boolean") {
        if (value) node.setAttribute(key, "");
      } else if (value !== null && value !== undefined) {
        node.setAttribute(key, value);
      }
    });
  }
  (children || []).forEach((child) => {
    if (child === null || child === undefined) return;
    if (typeof child === "string") node.appendChild(document.createTextNode(child));
    else node.appendChild(child);
  });
  return node;
}

function setLanguage(lang) {
  window.APP_STATE.locale = lang;
  window.APP_STATE.state.locale = lang;
  document.querySelectorAll("[data-lang]").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.lang === lang);
  });
  $("#app-title").textContent = t("app_title");
  renderSidebar();
  renderStep();
}

function renderSidebar() {
  const list = $("#steps-list");
  list.innerHTML = "";
  STEPS.forEach((step, idx) => {
    const li = el("li", {
      class:
        idx === window.APP_STATE.currentStep
          ? "active"
          : idx < window.APP_STATE.currentStep
          ? "done"
          : "",
    }, [
      el("span", { class: "step-num" }, [String(idx + 1)]),
      el("span", {}, [t("step_" + step)]),
    ]);
    list.appendChild(li);
  });
}

function setFooter({ backLabel, nextLabel, backDisabled, nextDisabled, nextHandler, backHandler, hideBack, hideNext }) {
  const back = $("#btn-back");
  const next = $("#btn-next");
  back.textContent = backLabel || t("back");
  next.textContent = nextLabel || t("next");
  back.disabled = !!backDisabled;
  next.disabled = !!nextDisabled;
  back.style.display = hideBack ? "none" : "";
  next.style.display = hideNext ? "none" : "";
  back.onclick = backHandler || (() => goStep(window.APP_STATE.currentStep - 1));
  next.onclick = nextHandler || (() => goStep(window.APP_STATE.currentStep + 1));
}

function goStep(idx) {
  if (idx < 0 || idx >= STEPS.length) return;
  window.APP_STATE.currentStep = idx;
  renderSidebar();
  renderStep();
}

function renderStep() {
  const step = STEPS[window.APP_STATE.currentStep];
  const main = $("#main-content");
  main.innerHTML = "";
  switch (step) {
    case "welcome":
      renderWelcome(main);
      break;
    case "network":
      renderNetwork(main);
      break;
    case "drivers":
      renderDrivers(main);
      break;
    case "driver_config":
      renderDriverConfig(main);
      break;
    case "ssl":
      renderSsl(main);
      break;
    case "service":
      renderService(main);
      break;
    case "summary":
      renderSummary(main);
      break;
  }
}

function renderWelcome(main) {
  main.appendChild(
    el("div", { class: "welcome" }, [
      el("h2", {}, [t("welcome_title")]),
      el("p", {}, [t("welcome_text")]),
      el("p", { class: "subtitle" }, [t("choose_language")]),
      el("div", { class: "lang-cards" }, [
        el("div", {
          class: "lang-card" + (window.APP_STATE.locale === "es" ? " selected" : ""),
          onclick: () => { setLanguage("es"); renderStep(); },
        }, ["Espanol"]),
        el("div", {
          class: "lang-card" + (window.APP_STATE.locale === "en" ? " selected" : ""),
          onclick: () => { setLanguage("en"); renderStep(); },
        }, ["English"]),
      ]),
    ])
  );
  setFooter({ backDisabled: true });
}

function renderNetwork(main) {
  const flask = window.APP_STATE.state.flask;
  main.appendChild(el("h2", {}, [t("network_title")]));
  main.appendChild(el("p", { class: "subtitle" }, [t("network_subtitle")]));

  const form = el("div", {});
  form.appendChild(field({
    label: t("host"),
    hint: t("host_hint"),
    input: el("input", {
      type: "text",
      value: flask.host || "127.0.0.1",
      oninput: (e) => { flask.host = e.target.value; },
    }),
  }));
  form.appendChild(field({
    label: t("port"),
    input: el("input", {
      type: "number",
      value: flask.port || 8069,
      min: 1,
      max: 65535,
      oninput: (e) => { flask.port = parseInt(e.target.value, 10) || 8069; },
    }),
  }));
  form.appendChild(field({
    label: t("cors"),
    hint: t("cors_hint"),
    input: el("input", {
      type: "text",
      value: flask.cors_origins || "*",
      oninput: (e) => { flask.cors_origins = e.target.value; },
    }),
  }));
  const debugWrap = el("label", { class: "toggle" }, [
    el("input", {
      type: "checkbox",
      checked: !!flask.debug,
      onchange: (e) => { flask.debug = e.target.checked; },
    }),
    el("span", {}, [t("debug")]),
  ]);
  form.appendChild(debugWrap);

  main.appendChild(form);
  setFooter({});
}

function renderDrivers(main) {
  main.appendChild(el("h2", {}, [t("drivers_title")]));
  main.appendChild(el("p", { class: "subtitle" }, [t("drivers_subtitle")]));

  const enabled = new Set(window.APP_STATE.state.application.drivers);
  window.APP_STATE.driversMeta.forEach((driver) => {
    const checkbox = el("input", {
      type: "checkbox",
      checked: enabled.has(driver.key),
      onchange: (e) => {
        if (e.target.checked) enabled.add(driver.key);
        else enabled.delete(driver.key);
        window.APP_STATE.state.application.drivers = Array.from(enabled);
      },
    });
    const card = el("div", {
      class: "driver-card" + (driver.recommended ? " recommended" : ""),
    }, [
      checkbox,
      el("div", { class: "driver-info" }, [
        el("div", { class: "driver-name" }, [driver.label[window.APP_STATE.locale]]),
        el("div", { class: "driver-desc" }, [driver.description[window.APP_STATE.locale]]),
      ]),
    ]);
    main.appendChild(card);
  });
  setFooter({});
}

function renderDriverConfig(main) {
  main.appendChild(el("h2", {}, [t("driver_config_title")]));
  main.appendChild(el("p", { class: "subtitle" }, [t("driver_config_subtitle")]));

  const detectBtn = el("button", {
    class: "btn",
    onclick: async () => {
      detectBtn.disabled = true;
      detectBtn.textContent = t("detecting");
      try {
        window.APP_STATE.hardware = await callApi("detect_hardware");
      } catch (err) {
        showAlert(main, "error", err.message);
      }
      renderStep();
    },
  }, [t("detect_hardware")]);
  main.appendChild(detectBtn);

  const enabled = window.APP_STATE.state.application.drivers;
  const configurable = window.APP_STATE.driversMeta.filter(
    (d) => enabled.includes(d.key) && d.fields && d.fields.length > 0
  );

  if (configurable.length === 0) {
    main.appendChild(el("p", { class: "subtitle" }, [t("no_drivers_selected")]));
    setFooter({});
    return;
  }

  configurable.forEach((driver) => {
    main.appendChild(renderDriverSection(driver));
  });

  setFooter({});
}

function renderDriverSection(driver) {
  const lang = window.APP_STATE.locale;
  const section = el("div", { class: "driver-section" }, [
    el("h3", {}, [driver.label[lang]]),
  ]);
  const grid = el("div", { class: "fields-grid" });
  section.appendChild(grid);

  const driverState = window.APP_STATE.state.drivers[driver.key] || {};
  window.APP_STATE.state.drivers[driver.key] = driverState;

  const renderFields = () => {
    grid.innerHTML = "";
    driver.fields.forEach((fieldDef) => {
      if (fieldDef.depends_on) {
        const [depKey, depVal] = Object.entries(fieldDef.depends_on)[0];
        if (driverState[depKey] !== depVal) return;
      }
      const current = driverState[fieldDef.key] !== undefined
        ? driverState[fieldDef.key]
        : fieldDef.default;
      driverState[fieldDef.key] = current;

      let input;
      if (fieldDef.type === "select" || fieldDef.datasource) {
        input = el("select", {});
        const options = collectOptions(fieldDef);
        if (fieldDef.allow_auto && !options.includes("auto")) options.unshift("auto");
        if (!options.includes(String(current)) && current) {
          options.push(String(current));
        }
        options.forEach((opt) => {
          const o = el("option", { value: opt }, [opt]);
          if (String(current) === String(opt)) o.setAttribute("selected", "");
          input.appendChild(o);
        });
        input.addEventListener("change", (e) => {
          driverState[fieldDef.key] = e.target.value;
          renderFields();
        });
      } else if (fieldDef.type === "number") {
        input = el("input", {
          type: "number",
          value: current,
          step: fieldDef.step || 1,
          oninput: (e) => { driverState[fieldDef.key] = e.target.value; },
        });
      } else if (fieldDef.type === "password") {
        input = el("input", {
          type: "password",
          value: current,
          oninput: (e) => { driverState[fieldDef.key] = e.target.value; },
        });
      } else {
        input = el("input", {
          type: "text",
          value: current,
          oninput: (e) => { driverState[fieldDef.key] = e.target.value; },
        });
      }

      grid.appendChild(field({
        label: fieldDef.label[lang],
        input,
      }));
    });
  };
  renderFields();
  return section;
}

function collectOptions(fieldDef) {
  if (fieldDef.options) return fieldDef.options.slice();
  const ds = fieldDef.datasource;
  const hw = window.APP_STATE.hardware;
  if (ds === "win32_printers") return hw.win32_printers.map((p) => p.name);
  if (ds === "com_ports") return hw.com_ports.map((p) => p.device);
  if (ds === "usb_devices")
    return hw.usb_devices.map((d) => `${d.vendor_id}:${d.product_id} ${d.product}`);
  return [];
}

function field({ label, input, hint }) {
  const wrap = el("div", { class: "field" });
  if (label) wrap.appendChild(el("label", {}, [label]));
  wrap.appendChild(input);
  if (hint) wrap.appendChild(el("div", { class: "hint" }, [hint]));
  return wrap;
}

function renderSsl(main) {
  main.appendChild(el("h2", {}, [t("ssl_title")]));
  main.appendChild(el("p", { class: "subtitle" }, [t("ssl_subtitle")]));

  const flask = window.APP_STATE.state.flask;
  const ssl = window.APP_STATE.bootstrap.ssl;

  if (ssl.cert && ssl.key) {
    main.appendChild(el("div", { class: "alert success" }, [
      `${t("ssl_existing")} ${ssl.cert} / ${ssl.key}`,
    ]));
    flask.sslcert = ssl.cert;
    flask.sslkey = ssl.key;
  }

  const status = el("div", {});
  main.appendChild(status);

  const genBtn = el("button", { class: "btn primary" }, [t("ssl_generate")]);
  genBtn.onclick = async () => {
    genBtn.disabled = true;
    genBtn.innerHTML = `<span class="spinner"></span>${t("ssl_generating")}`;
    try {
      const res = await callApi("generate_ssl");
      flask.sslcert = res.cert;
      flask.sslkey = res.key;
      window.APP_STATE.bootstrap.ssl = res;
      status.innerHTML = "";
      status.appendChild(el("div", { class: "alert success" }, [t("ssl_generated")]));
    } catch (err) {
      status.innerHTML = "";
      status.appendChild(el("div", { class: "alert error" }, [err.message]));
    }
    genBtn.disabled = false;
    genBtn.textContent = t("ssl_generate");
  };
  main.appendChild(genBtn);

  const skipWrap = el("label", { class: "toggle" }, [
    el("input", {
      type: "checkbox",
      checked: !flask.sslcert,
      onchange: (e) => {
        if (e.target.checked) {
          flask.sslcert = "";
          flask.sslkey = "";
        }
      },
    }),
    el("span", {}, [t("ssl_skip")]),
  ]);
  main.appendChild(skipWrap);

  setFooter({});
}

function renderService(main) {
  main.appendChild(el("h2", {}, [t("service_title")]));
  main.appendChild(el("p", { class: "subtitle" }, [t("service_subtitle")]));

  const status = window.APP_STATE.bootstrap.service_status;
  const pillClass =
    status.toLowerCase().includes("running") ? "running"
    : status === "not_installed" ? "stopped"
    : status.toLowerCase().includes("stop") ? "stopped"
    : "unknown";
  main.appendChild(el("p", {}, [
    `${t("service_current")} `,
    el("span", { class: `status-pill ${pillClass}` }, [
      t("status_" + (status === "not_installed" ? "not_installed" : pillClass === "running" ? "running" : pillClass === "stopped" ? "stopped" : "unknown"))
    ]),
  ]));

  const opts = window.APP_STATE.options;
  main.appendChild(el("label", { class: "toggle" }, [
    el("input", {
      type: "checkbox",
      checked: opts.install_service,
      onchange: (e) => { opts.install_service = e.target.checked; },
    }),
    el("span", {}, [t("service_install")]),
  ]));
  main.appendChild(el("label", { class: "toggle" }, [
    el("input", {
      type: "checkbox",
      checked: opts.autostart,
      onchange: (e) => { opts.autostart = e.target.checked; },
    }),
    el("span", {}, [t("service_autostart")]),
  ]));

  if (status !== "not_installed") {
    const ctrl = el("div", { class: "row-actions" });
    ctrl.appendChild(el("button", {
      class: "btn",
      onclick: () => serviceAction("start_service", main),
    }, [t("start")]));
    ctrl.appendChild(el("button", {
      class: "btn",
      onclick: () => serviceAction("stop_service", main),
    }, [t("stop")]));
    ctrl.appendChild(el("button", {
      class: "btn",
      onclick: () => serviceAction("restart_service", main),
    }, [t("restart")]));
    ctrl.appendChild(el("button", {
      class: "btn danger",
      onclick: () => serviceAction("remove_service", main),
    }, [t("remove")]));
    main.appendChild(ctrl);
  }

  setFooter({});
}

async function serviceAction(method, main) {
  try {
    const res = await callApi(method);
    window.APP_STATE.bootstrap.service_status = res.status;
    renderStep();
  } catch (err) {
    showAlert(main, "error", err.message);
  }
}

function renderSummary(main) {
  main.appendChild(el("h2", {}, [t("summary_title")]));
  main.appendChild(el("p", { class: "subtitle" }, [t("summary_subtitle")]));

  const s = window.APP_STATE.state;
  const opts = window.APP_STATE.options;
  const grid = el("dl", { class: "summary-grid" });

  const rows = [
    [t("summary_locale"), s.locale],
    [t("summary_network"), `${s.flask.host}:${s.flask.port}`],
    [t("summary_drivers"), s.application.drivers.join(", ") || "-"],
    [t("summary_ssl"), s.flask.sslcert ? `${s.flask.sslcert} / ${s.flask.sslkey}` : t("no")],
    [t("summary_service"),
      opts.install_service
        ? `${t("yes")} (${opts.autostart ? t("status_running") : t("status_stopped")})`
        : t("no")],
  ];
  rows.forEach(([k, v]) => {
    grid.appendChild(el("dt", {}, [k]));
    grid.appendChild(el("dd", {}, [v]));
  });
  main.appendChild(grid);

  const result = el("div", { style: "margin-top:18px" });
  main.appendChild(result);

  const applyBtn = el("button", { class: "btn primary" }, [t("apply")]);
  applyBtn.onclick = async () => {
    applyBtn.disabled = true;
    applyBtn.innerHTML = `<span class="spinner"></span>${t("applying")}`;
    try {
      const res = await callApi("apply_all", s, opts);
      result.innerHTML = "";
      result.appendChild(el("div", { class: "alert success" }, [t("applied_ok")]));
      window.APP_STATE.applied = true;
      setFooter({
        hideBack: true,
        nextLabel: t("finish"),
        nextHandler: () => callApi("quit"),
      });
    } catch (err) {
      result.innerHTML = "";
      result.appendChild(el("div", { class: "alert error" }, [err.message]));
      applyBtn.disabled = false;
      applyBtn.textContent = t("apply");
    }
  };

  setFooter({
    nextLabel: t("apply"),
    nextHandler: () => applyBtn.click(),
  });
  main.appendChild(applyBtn);
  applyBtn.style.display = "none";
}

function showAlert(container, kind, message) {
  const alert = el("div", { class: "alert " + kind }, [message]);
  container.insertBefore(alert, container.firstChild);
  setTimeout(() => alert.remove(), 5000);
}

async function init() {
  document.querySelectorAll("[data-lang]").forEach((btn) => {
    btn.addEventListener("click", () => setLanguage(btn.dataset.lang));
  });

  try {
    const data = await callApi("get_bootstrap");
    window.APP_STATE.bootstrap = data;
    window.APP_STATE.state = data.state;
    window.APP_STATE.driversMeta = data.drivers_meta;
    if (data.state.locale && window.I18N[data.state.locale]) {
      window.APP_STATE.locale = data.state.locale;
    }
    setLanguage(window.APP_STATE.locale);
    renderSidebar();
    renderStep();
  } catch (err) {
    document.querySelector("#main-content").innerHTML =
      `<div class="alert error">${err.message}</div>`;
  }
}

init();
