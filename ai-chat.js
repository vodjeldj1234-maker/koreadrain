/* AI 상담 채팅창 (홈페이지제작 53째방, 2026-11-23) — 포스원·윤슬 공용.
   <script src="/ai-chat.js" data-site="koreadrain" data-name="포스원종합공사" data-phone="01012345678" data-endpoint="https://….workers.dev" defer></script>
   data-endpoint 가 비면 아무것도 그리지 않는다. 대화는 이 탭에서만 기억한다(sessionStorage). */
(function () {
  var me = document.currentScript;
  if (!me) return;
  var EP = me.getAttribute("data-endpoint"), SITE = me.getAttribute("data-site"),
      NAME = me.getAttribute("data-name") || "", PHONE = me.getAttribute("data-phone") || "";
  if (!EP || !SITE) return;
  var KEY = "aichat_" + SITE, MAXLEN = 600;
  var state = { msgs: [], summary: "", cid: "" };
  try { var s = sessionStorage.getItem(KEY); if (s) state = JSON.parse(s); } catch (e) {}
  if (!state.cid) state.cid = (Date.now().toString(36) + Math.random().toString(36).slice(2, 10)).replace(/[^a-z0-9]/g, "").slice(0, 24);
  function save() { try { sessionStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }
  function ga(ev) { try { if (window.gtag) gtag("event", ev, { site: SITE }); } catch (e) {} }

  var css = ""
    + ".aic-btn{position:fixed;right:14px;bottom:86px;z-index:9998;border:0;border-radius:28px;padding:13px 18px;font:800 15px/1 system-ui,sans-serif;"
    + "background:#1f6feb;color:#fff;box-shadow:0 6px 18px rgba(0,0,0,.25);cursor:pointer;letter-spacing:-.3px}"
    + "@media(min-width:900px){.aic-btn{bottom:24px}}"
    + ".aic-panel{position:fixed;right:12px;bottom:86px;z-index:9999;width:min(380px,calc(100vw - 24px));height:min(560px,calc(100vh - 120px));"
    + "background:#fff;color:#1b1f24;border-radius:14px;box-shadow:0 12px 40px rgba(0,0,0,.3);display:none;flex-direction:column;overflow:hidden;font:15px/1.55 system-ui,sans-serif}"
    + "@media(min-width:900px){.aic-panel{bottom:24px}}"
    + ".aic-panel.on{display:flex}.aic-hd{background:#1f6feb;color:#fff;padding:12px 14px;display:flex;align-items:center;gap:8px}"
    + ".aic-hd b{flex:1;font-size:15.5px}.aic-hd small{display:block;font-weight:400;opacity:.85;font-size:12px}"
    + ".aic-x{background:none;border:0;color:#fff;font-size:22px;cursor:pointer;line-height:1}"
    + ".aic-log{flex:1;overflow-y:auto;padding:12px;background:#f4f6f8}"
    + ".aic-m{max-width:86%;margin:0 0 9px;padding:9px 12px;border-radius:12px;white-space:pre-wrap;word-break:keep-all;overflow-wrap:anywhere}"
    + ".aic-a{background:#fff;border:1px solid #e1e5ea}.aic-u{background:#1f6feb;color:#fff;margin-left:auto}"
    + ".aic-wait{color:#7a8490;font-size:13px;margin:0 0 8px}"
    + ".aic-sms{display:block;margin:0 12px 8px;padding:11px;border-radius:10px;background:#16a34a;color:#fff;text-align:center;font-weight:800;text-decoration:none}"
    + ".aic-f{display:flex;gap:6px;padding:8px 10px 10px;border-top:1px solid #e1e5ea;background:#fff}"
    + ".aic-f textarea{flex:1;resize:none;border:1px solid #cfd6de;border-radius:10px;padding:9px 10px;font:15px/1.4 system-ui,sans-serif;height:44px;color:#1b1f24;background:#fff}"
    + ".aic-f button{border:0;border-radius:10px;background:#1f6feb;color:#fff;font-weight:800;padding:0 14px;cursor:pointer}"
    + ".aic-note{font-size:11.5px;color:#7a8490;padding:0 12px 6px;background:#fff}";
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  var btn = document.createElement("button");
  btn.className = "aic-btn"; btn.type = "button"; btn.textContent = "💬 AI 견적 접수";
  var p = document.createElement("div");
  p.className = "aic-panel"; p.setAttribute("role", "dialog"); p.setAttribute("aria-label", "AI 상담");
  p.innerHTML = '<div class="aic-hd"><b>AI 견적 접수<small>' + NAME + ' · 24시간 접수</small></b>'
    + '<button class="aic-x" type="button" aria-label="닫기">×</button></div>'
    + '<div class="aic-log"></div><a class="aic-sms" href="#">📩 문자로 사진 보내기</a>'
    + '<div class="aic-note">AI 접수 직원이 내용을 정리해 대표님께 전달합니다. 남기신 연락처는 견적 연락에만 쓰고 90일 뒤 지웁니다.</div>'
    + '<form class="aic-f"><textarea maxlength="' + MAXLEN + '" placeholder="예: 천안 2층 상가 선홈통이 새요" aria-label="문의 내용"></textarea><button type="submit">보내기</button></form>';
  document.body.appendChild(btn); document.body.appendChild(p);
  var log = p.querySelector(".aic-log"), ta = p.querySelector("textarea"), form = p.querySelector("form"), sms = p.querySelector(".aic-sms");
  var busy = false;

  var HELLO = "안녕하세요, " + NAME + " 견적 접수입니다. 대표님이 현장에 계셔서 제가 내용을 받아 전달해 드립니다. 어떤 공사가 필요하신지, 지역(시·동)과 함께 적어 주세요.";

  function bubble(role, text) {
    var d = document.createElement("div");
    d.className = "aic-m " + (role === "user" ? "aic-u" : "aic-a");
    d.textContent = text; log.appendChild(d); log.scrollTop = log.scrollHeight;
  }
  function render() {
    log.innerHTML = ""; bubble("assistant", HELLO);
    for (var i = 0; i < state.msgs.length; i++) bubble(state.msgs[i].role, state.msgs[i].content);
    setSms();
  }
  function setSms() {
    var ios = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
    var body = "[견적 문의]\n" + (state.summary ? state.summary + "\n" : "② 지역(시·동): \n③ 원하시는 작업: \n") + "(현장 사진 2~3장 첨부)";
    sms.href = "sms:" + PHONE + (ios ? "&" : "?") + "body=" + encodeURIComponent(body);
  }
  sms.addEventListener("click", function () {
    ga("ai_chat_sms");
    try { fetch(EP, { method: "POST", headers: { "Content-Type": "application/json" }, keepalive: true,
      body: JSON.stringify({ site: SITE, cid: state.cid, event: "sms" }) }); } catch (e) {}
  });

  function send(text) {
    if (busy) return;
    text = (text || "").trim().slice(0, MAXLEN);
    if (!text) return;
    busy = true; ta.value = "";
    state.msgs.push({ role: "user", content: text }); save(); bubble("user", text);
    var w = document.createElement("div"); w.className = "aic-wait"; w.textContent = "답을 쓰는 중…"; log.appendChild(w); log.scrollTop = log.scrollHeight;
    ga("ai_chat_send");
    fetch(EP, { method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ site: SITE, cid: state.cid, page: location.pathname, messages: state.msgs.slice(-24) }) })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        var reply = (d && d.reply) || "지금 상담 연결이 원활하지 않습니다. 아래 초록 버튼으로 사진과 지역을 문자로 보내 주세요.";
        state.msgs.push({ role: "assistant", content: reply });
        if (d && d.summary) state.summary = d.summary;
        save(); w.remove(); bubble("assistant", reply); setSms();
      })
      .catch(function () {
        w.remove(); bubble("assistant", "연결이 끊겼습니다. 아래 초록 버튼으로 사진과 지역을 문자로 보내 주세요.");
      })
      .then(function () { busy = false; });
  }
  form.addEventListener("submit", function (e) { e.preventDefault(); send(ta.value); });
  ta.addEventListener("keydown", function (e) { if (e.key === "Enter" && !e.shiftKey && !e.isComposing) { e.preventDefault(); send(ta.value); } });
  btn.addEventListener("click", function () { p.classList.add("on"); btn.style.display = "none"; render(); ta.focus(); ga("ai_chat_open"); });
  p.querySelector(".aic-x").addEventListener("click", function () { p.classList.remove("on"); btn.style.display = ""; });
})();
