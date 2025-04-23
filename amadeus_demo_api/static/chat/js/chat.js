"use strict";
(() => {
  var b = "fs-attributes";
  var P = "cmsattribute";
  var f = "formsubmit";
  var U = "support";
  var $ = async (...t) => {
    var r;
    let e = [];
    for (let o of t) {
      let s = await ((r = window.fsAttributes[o]) == null ? void 0 : r.loading);
      e.push(s);
    }
    return e;
  };
  var A = () => {};
  function R(t, e, r, o) {
    return t
      ? (t.addEventListener(e, r, o), () => t.removeEventListener(e, r, o))
      : A;
  }
  var x = {
    formBlock: "w-form",
    checkboxField: "w-checkbox",
    checkboxInput: "w-checkbox-input",
    radioField: "w-radio",
    radioInput: "w-radio-input",
    checkboxOrRadioLabel: "w-form-label",
    checkboxOrRadioFocus: "w--redirected-focus",
    checkboxOrRadioChecked: "w--redirected-checked",
    successMessage: "w-form-done",
    errorMessage: "w-form-fail",
  };
  var B = (t, e) => (
    Array.isArray(e) || (e = [e]),
    e.map((o) => t.dispatchEvent(new Event(o, { bubbles: !0 }))).every((o) => o)
  );
  var L = (t) => t instanceof HTMLInputElement;
  var C = (t) => t != null;
  var T = (t) => typeof t == "string";
  var N = (t) => {
    let e = t.split("-"),
      r = parseInt(e[e.length - 1]);
    if (!isNaN(r)) return r;
  };
  function V(t, e, r) {
    var s;
    let o = window.fsAttributes[t];
    return (o.destroy = r || A), (s = o.resolve) == null || s.call(o, e), e;
  }
  var D = (t, e = "1", r = "iife") => {
    let s = `${t}${r === "esm" ? ".esm" : ""}.js`;
    return `https://cdn.jsdelivr.net/npm/@finsweet/attributes-${t}@${e}/${s}`;
  };
  var ce = `${b}-${U}`,
    K = async () => {
      var s;
      let { fsAttributes: t, location: e } = window,
        { host: r, searchParams: o } = new URL(e.href);
      return !r.includes("webflow.io") || !o.has(ce)
        ? !1
        : (s = t.import) == null
        ? void 0
        : s.call(t, U, "1");
    };
  var _ = (t) => (e) => `${t}${e ? `-${e}` : ""}`,
    I = (t) => {
      let e = (s, n, i) => {
        let c = t[s],
          { key: l, values: d } = c,
          u;
        if (!n) return `[${l}]`;
        let E = d == null ? void 0 : d[n];
        T(E)
          ? (u = E)
          : (u = E(i && "instanceIndex" in i ? i.instanceIndex : void 0));
        let p = i && "caseInsensitive" in i && i.caseInsensitive ? "i" : "";
        if (!(i != null && i.operator)) return `[${l}="${u}"${p}]`;
        switch (i.operator) {
          case "prefixed":
            return `[${l}^="${u}"${p}]`;
          case "suffixed":
            return `[${l}$="${u}"${p}]`;
          case "contains":
            return `[${l}*="${u}"${p}]`;
        }
      };
      function r(s, n) {
        let i = e("element", s, n),
          c = (n == null ? void 0 : n.scope) || document;
        return n != null && n.all
          ? [...c.querySelectorAll(i)]
          : c.querySelector(i);
      }
      return [
        e,
        r,
        (s, n) => {
          let i = t[n];
          return i ? s.getAttribute(i.key) : null;
        },
      ];
    };
  var S = {
      preventLoad: { key: `${b}-preventload` },
      debugMode: { key: `${b}-debug` },
      src: { key: "src", values: { finsweet: "@finsweet/attributes" } },
      dev: { key: `${b}-dev` },
    },
    [F, ct] = I(S);
  var H = (t) => {
    let { currentScript: e } = document,
      r = {};
    if (!e) return { attributes: r, preventsLoad: !1 };
    let s = {
      preventsLoad: T(e.getAttribute(S.preventLoad.key)),
      attributes: r,
    };
    for (let n in t) {
      let i = e.getAttribute(t[n]);
      s.attributes[n] = i;
    }
    return s;
  };
  var G = ({ scriptAttributes: t, attributeKey: e, version: r, init: o }) => {
      var c;
      ae(), (c = window.fsAttributes)[e] || (c[e] = {});
      let { preventsLoad: s, attributes: n } = H(t),
        i = window.fsAttributes[e];
      (i.version = r),
        (i.init = o),
        s ||
          (window.Webflow || (window.Webflow = []),
          window.Webflow.push(() => o(n)));
    },
    ae = () => {
      let t = le();
      if (window.fsAttributes && !Array.isArray(window.fsAttributes)) {
        M(window.fsAttributes, t);
        return;
      }
      let e = ue(t);
      M(e, t),
        me(e),
        (window.fsAttributes = e),
        (window.FsAttributes = window.fsAttributes),
        K();
    },
    ue = (t) => {
      let e = {
        cms: {},
        push(...r) {
          var o, s;
          for (let [n, i] of r)
            (s = (o = this[n]) == null ? void 0 : o.loading) == null ||
              s.then(i);
        },
        async import(r, o) {
          let s = e[r];
          return (
            s ||
            new Promise((n) => {
              let i = document.createElement("script");
              (i.src = D(r, o)),
                (i.async = !0),
                (i.onload = () => {
                  let [c] = M(e, [r]);
                  n(c);
                }),
                document.head.append(i);
            })
          );
        },
        destroy() {
          var r, o;
          for (let s of t)
            (o = (r = window.fsAttributes[s]) == null ? void 0 : r.destroy) ==
              null || o.call(r);
        },
      };
      return e;
    },
    le = () => {
      let t = F("src", "finsweet", { operator: "contains" }),
        e = F("dev");
      return [...document.querySelectorAll(`script${t}, script${e}`)].reduce(
        (s, n) => {
          var c;
          let i =
            n.getAttribute(S.dev.key) ||
            ((c = n.src.match(/[\w-. ]+(?=(\.js)$)/)) == null ? void 0 : c[0]);
          return i && !s.includes(i) && s.push(i), s;
        },
        []
      );
    },
    M = (t, e) =>
      e.map((o) => {
        let s = t[o];
        return (
          s ||
          ((t[o] = {}),
          (s = t[o]),
          (s.loading = new Promise((n) => {
            s.resolve = (i) => {
              n(i), delete s.resolve;
            };
          })),
          s)
        );
      }),
    me = (t) => {
      let e = Array.isArray(window.fsAttributes) ? window.fsAttributes : [];
      t.push(...e);
    };
  var q = "1.4.1";
  var Y = (t, e) => {
    let r = t.getAttribute(e);
    return r ? N(r) : void 0;
  };
  var k = (t, e) => {
    e ? window.open(t, "_blank") : (window.location.href = t);
  };
  var m = `fs-${f}`,
    Te = "form",
    de = "reset",
    Ee = "ix-trigger",
    be = "reset",
    fe = { true: "true" },
    Ae = "preventreset",
    xe = { true: "true" },
    Se = "reload",
    ye = { true: "true" },
    Re = "redirect",
    _e = { true: "true" },
    Ie = "redirecturl",
    we = "redirectnewtab",
    he = { true: "true" },
    ge = "enhance",
    ve = { true: "true" },
    Ue = "disable",
    Be = { true: "true" },
    a = {
      element: {
        key: `${m}-element`,
        values: { form: _(Te), reset: _(de), ixTrigger: _(Ee) },
      },
      reset: { key: `${m}-${be}`, values: fe },
      preventReset: { key: `${m}-${Ae}`, values: xe },
      reload: { key: `${m}-${Se}`, values: ye },
      redirect: { key: `${m}-${Re}`, values: _e },
      redirectUrl: { key: `${m}-${Ie}` },
      redirectNewTab: { key: `${m}-${we}`, values: he },
      disable: { key: `${m}-${Ue}`, values: Be },
      enhance: { key: `${m}-${ge}`, values: ve },
    },
    [j, y] = I(a);
  var O = ({ form: t, successMessage: e, errorMessage: r }, o = []) => {
      t.reset();
      for (let { element: s, value: n, checked: i } of o)
        (s.value = n), L(s) && i && (s.checked = i);
      (e.style.display = "none"),
        (r.style.display = "none"),
        (t.style.display = "");
    },
    X = (t) =>
      [...t.querySelectorAll("input, select, textarea")].reduce((o, s) => {
        if (!s.closest(j("preventReset"))) return o;
        let { value: i } = s,
          c = L(s) ? s.checked : void 0;
        return o.push({ element: s, value: i, checked: c }), o;
      }, []);
  var W = async (t, e, r) => {
    let o = new FormData(t),
      s = new URL(e);
    if (r === "get") for (let [i, c] of o) !T(c) || s.searchParams.append(i, c);
    let n = r === "post" ? o : void 0;
    try {
      return (await fetch(s.toString(), { method: r, body: n })).ok;
    } catch (i) {
      return !1;
    }
  };
  var z = ({ successMessage: t, errorMessage: e }) =>
      new Promise((r) => {
        let o = new MutationObserver(([{ target: n }]) => {
            r(n === t);
          }),
          s = { attributes: !0, attributeFilter: ["style"] };
        o.observe(t, s), o.observe(e, s);
      }),
    Q = ({ errorMessage: t }) => {
      t.style.display = "block";
    },
    J = ({ errorMessage: t }) => {
      t.style.display = "none";
    },
    Z = ({ form: t, successMessage: e, errorMessage: r }) => {
      (t.style.display = "none"),
        (r.style.display = "none"),
        (e.style.display = "block");
    },
    ee = ({ submitButtons: t }) => {
      let e = t.reduce((r, o) => {
        let { value: s, dataset: n } = o,
          i = n.wait;
        return (
          !s ||
            !i ||
            ((o.value = i),
            r.push(() => {
              o.value = s;
            })),
          r
        );
      }, []);
      return () => {
        for (let r of e) r();
      };
    };
  var w = class {
    constructor({
      form: e,
      formBlock: r,
      reset: o,
      resetTimeout: s,
      reload: n,
      reloadTimeout: i,
      redirect: c,
      redirectTimeout: l,
      redirectUrl: d,
      redirectToNewTab: u,
      enhance: E,
      disable: p,
      ixTriggers: g,
      resetButtons: v,
    }) {
      (this.form = e),
        (this.formBlock = r),
        (this.successMessage = r.querySelector(`.${x.successMessage}`)),
        (this.errorMessage = r.querySelector(`.${x.errorMessage}`)),
        (this.submitButtons = [...e.querySelectorAll('input[type="submit"]')]),
        (this.redirect = c),
        (this.redirectTimeout = l),
        (this.redirectUrl = d),
        (this.redirectToNewTab = u),
        (this.reset = o),
        (this.resetTimeout = s),
        (this.reload = n),
        (this.reloadTimeout = i),
        (this.enhance = E),
        (this.disabled = p),
        (this.ixTriggers = g),
        (this.resetButtons = v),
        (this.destroy = this.listenEvents());
    }
    listenEvents() {
      let { form: e, resetButtons: r } = this,
        o = R(e, "submit", (n) => this.handleSubmit(n)),
        s = r.map((n) => R(n, "click", () => this.handleReset(!1)));
      return () => {
        o();
        for (let n of s) n();
      };
    }
    async handleSubmit(e) {
      let { reset: r, redirect: o, reload: s, enhance: n, disabled: i } = this,
        c;
      (i || n) && (e.preventDefault(), e.stopImmediatePropagation()),
        !i &&
          (n ? (c = await this.handleEnhancedSubmit()) : (c = await z(this)),
          c &&
            (r && this.handleReset(),
            o && this.handleRedirect(),
            s && this.handleReload(),
            this.triggerIx()));
    }
    handleReset(e = !0) {
      let { form: r, resetTimeout: o, currentResetTimeout: s } = this;
      clearTimeout(s), (this.currentResetTimeout = void 0);
      let n = X(r);
      e && o
        ? (this.currentResetTimeout = setTimeout(() => O(this, n), o))
        : O(this, n);
    }
    handleRedirect() {
      let {
        redirectUrl: e,
        redirectTimeout: r,
        redirectToNewTab: o,
        currentRedirectTimeout: s,
      } = this;
      !e ||
        (clearTimeout(s),
        (this.currentRedirectTimeout = void 0),
        r
          ? (this.currentRedirectTimeout = setTimeout(() => k(e, o), r))
          : k(e, o));
    }
    handleReload() {
      let { reloadTimeout: e, currentReloadTimeout: r } = this,
        { location: o } = window;
      clearTimeout(r),
        (this.currentReloadTimeout = void 0),
        e ? (this.currentReloadTimeout = setTimeout(o.reload, e)) : o.reload();
    }
    async handleEnhancedSubmit() {
      let { form: e } = this,
        { action: r, method: o } = e;
      if (!r) return !1;
      J(this);
      let s = ee(this),
        n = await W(e, r, o);
      return n ? Z(this) : Q(this), s(), n;
    }
    triggerIx() {
      for (let e of this.ixTriggers) B(e, "click");
    }
  };
  var h = (t) => {
    let e = T(t),
      r;
    if (e) {
      let o = parseInt(t);
      isNaN(o) || (r = o);
    }
    return [e, r];
  };
  var te = (t) => {
    let e = t.closest(`.${x.formBlock}`);
    if (!e) return;
    let r = e.querySelector("form");
    if (!r) return;
    let o = Y(t, a.element.key),
      s = y("ixTrigger", { instanceIndex: o, all: !0 }),
      n = y("reset", { instanceIndex: o, all: !0 }),
      i = t.getAttribute(a.reset.key),
      [c, l] = h(i),
      d = t.getAttribute(a.reload.key),
      [u, E] = h(d),
      p = t.getAttribute(a.redirect.key),
      [g, v] = h(p),
      oe = t.getAttribute(a.redirectUrl.key),
      se =
        t.getAttribute(a.redirectNewTab.key) === a.redirectNewTab.values.true,
      ne = t.getAttribute(a.disable.key) === a.disable.values.true,
      ie = t.getAttribute(a.enhance.key) === a.enhance.values.true;
    return new w({
      form: r,
      formBlock: e,
      reset: c,
      resetTimeout: l,
      reload: u,
      reloadTimeout: E,
      redirect: g,
      redirectUrl: oe,
      redirectTimeout: v,
      redirectToNewTab: se,
      enhance: ie,
      disable: ne,
      ixTriggers: s,
      resetButtons: n,
    });
  };
  var re = async () => {
    await $(P);
    let e = y("form", { all: !0, operator: "prefixed" }).map(te).filter(C);
    return V(f, e, () => {
      for (let r of e) r.destroy();
    });
  };
  G({ init: re, version: q, attributeKey: f });
})();
