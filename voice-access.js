/* Authentication is server-enforced. The shortcut only keeps admin UI out of the learner view. */
(()=>{
 const legacy=['localhost','127.0.0.1','pythonidaer.github.io'].includes(location.hostname);
 let authenticated=legacy,configured=legacy;
 function sync(){document.querySelectorAll('[data-voice-open]').forEach(b=>b.hidden=!authenticated);document.dispatchEvent(new CustomEvent('voice:access',{detail:{authenticated,hosted:!legacy}}))}
 async function refresh(){if(legacy){sync();return true}try{const r=await fetch('/api/voice?action=status',{credentials:'same-origin',cache:'no-store',signal:AbortSignal.timeout(8000)});if(!r.ok)throw Error();const data=await r.json();configured=data.configured===true;authenticated=data.authenticated===true}catch{authenticated=false;configured=false}sync();return authenticated}
 async function request(action,body){const r=await fetch('/api/voice?action='+action,{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),signal:AbortSignal.timeout(15000)});let data;try{data=await r.json()}catch{throw Error('Voice server is unavailable.')}if(!r.ok){if(r.status===401){authenticated=false;sync()}throw Error(data.error||'Voice request failed.')}return data}
 window.VoiceAccess={hosted:!legacy,isAuthenticated:()=>authenticated,refresh,session:context=>request('session',{context}),logout:async()=>{await request('logout',{});authenticated=false;sync()}};
 document.addEventListener('DOMContentLoaded',()=>{
  const dlg=document.createElement('dialog');dlg.className='voice-dialog';dlg.id='voice-login';dlg.setAttribute('aria-labelledby','voice-login-title');
  dlg.innerHTML='<div class="voice-heading"><h2 id="voice-login-title">Private voice access</h2><button type="button" id="voice-login-close" aria-label="Close login"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg></button></div><form id="voice-login-form"><label for="voice-password">Password</label><input id="voice-password" name="password" type="password" autocomplete="current-password" required maxlength="200"><div class="voice-controls"><button id="voice-login-submit" type="submit">Sign in</button></div><p id="voice-login-status" role="status"></p></form>';
  document.body.append(dlg);let returnFocus=null;
  function showLogin(){if(legacy)return;returnFocus=document.activeElement;if(!dlg.open)dlg.showModal();dlg.querySelector('#voice-password').focus();dlg.querySelector('#voice-login-status').textContent=authenticated?'Already signed in. Close this window to use the microphone icon.':configured?'':'If sign-in is unavailable, check the Vercel environment configuration.'}
  document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.shiftKey&&e.code==='KeyL'){e.preventDefault();showLogin()}});
  function hashLogin(){if(location.hash==='#voice-login')showLogin()};window.addEventListener('hashchange',hashLogin);
  dlg.querySelector('#voice-login-close').onclick=()=>dlg.close();dlg.addEventListener('close',()=>{dlg.querySelector('#voice-password').value='';if(location.hash==='#voice-login')history.replaceState(null,'',location.pathname+location.search+'#learn');returnFocus?.focus?.()});
  dlg.querySelector('form').onsubmit=async e=>{e.preventDefault();const button=dlg.querySelector('#voice-login-submit');button.disabled=true;const password=dlg.querySelector('#voice-password').value;dlg.querySelector('#voice-password').value='';try{await request('login',{password});authenticated=true;configured=true;sync();dlg.close();document.querySelector('[data-voice-open]')?.focus()}catch(error){dlg.querySelector('#voice-login-status').textContent=error.message}finally{button.disabled=false}};
  document.addEventListener('lms:render',()=>document.querySelectorAll('[data-voice-open]').forEach(b=>b.hidden=!authenticated));
  sync();refresh().then(hashLogin);
  window.addEventListener('focus',refresh);
 });
})();
