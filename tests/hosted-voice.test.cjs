const {test}=require('node:test'),assert=require('node:assert/strict');
const {createHandler}=require('../lib/hosted-voice.cjs');
const env={OPENAI_API_KEY:'sk-test-never-real',VOICE_PASSWORD:'a-long-private-test-password',VOICE_SESSION_SECRET:'test-session-signing-secret-at-least-32-chars'};
const origin='https://course.example';
const request=(action,body,extra={})=>new Request(origin+'/api/voice?action='+action,{method:body===undefined?'GET':'POST',headers:{Origin:origin,'Content-Type':'application/json',...extra},body:body===undefined?undefined:JSON.stringify(body)});
test('hosted login gates paid calls with signed, expiring cookies and origin validation',async()=>{
 let clock=Date.now(),calls=0,captured,logs=[];const handler=createHandler({env,now:()=>clock,logger:v=>logs.push(v),apiFetch:async(url,o)=>{calls++;captured=o;return {ok:true,json:async()=>({value:'ek_test-secret',expires_at:123})}}});
 assert.equal((await handler(request('status'))).status,200);assert.equal((await (await handler(request('status'))).json()).authenticated,false);
 assert.equal((await handler(request('session',{context:'visible'}))).status,401);assert.equal(calls,0);
 assert.equal((await handler(request('login',{password:env.VOICE_PASSWORD},{Origin:'https://evil.example'}))).status,403);
 assert.equal((await handler(request('login',{password:'wrong'}))).status,401);
 let r=await handler(request('login',{password:env.VOICE_PASSWORD}));assert.equal(r.status,200);const set=r.headers.get('set-cookie');for(const value of ['HttpOnly','Secure','SameSite=Strict','Path=/','Max-Age=43200'])assert.ok(set.includes(value));const Cookie=set.split(';')[0];assert.ok(!set.includes(env.VOICE_PASSWORD));
 assert.equal((await (await handler(request('status',undefined,{Cookie}))).json()).authenticated,true);
 r=await handler(request('session',{context:'Only visible text',voice:'echo'},{Cookie}));assert.equal(r.status,200);assert.equal((await r.json()).value,'ek_test-secret');assert.equal(captured.headers.Authorization,'Bearer '+env.OPENAI_API_KEY);assert.ok(JSON.parse(captured.body).session.instructions.includes('Only visible text'));assert.equal(JSON.parse(captured.body).session.audio.output.voice,'echo');assert.equal((await handler(request('session',{context:'ok',voice:'unsupported'},{Cookie}))).status,400);assert.equal(r.headers.get('cache-control'),'no-store');
 assert.equal((await handler(request('session',{context:'x'.repeat(6001)},{Cookie}))).status,400);assert.equal((await handler(request('session',{context:'ok'},{Cookie:Cookie+'bad'}))).status,401);
 assert.equal((await handler(request('session',{context:'ok'},{Cookie,Origin:'https://evil.example'}))).status,403);
 r=await handler(request('logout',{}, {Cookie}));assert.equal(r.status,200);assert.match(r.headers.get('set-cookie'),/Max-Age=0/);
 clock+=43200001;assert.equal((await handler(request('session',{context:'ok'},{Cookie}))).status,401);
 assert.equal(calls,1);const log=logs.join('');for(const secret of [env.OPENAI_API_KEY,env.VOICE_PASSWORD,env.VOICE_SESSION_SECRET,'ek_test-secret','Only visible text'])assert.ok(!log.includes(secret));assert.match(log,/session.created/);
});
test('hosted configuration fails closed, rejects oversized bodies, and throttles login attempts',async()=>{
 const silent=()=>{};const handler=createHandler({env:{},logger:silent,apiFetch:()=>{throw Error('must not call')}});assert.equal((await handler(request('login',{password:'x'}))).status,503);assert.equal((await (await handler(request('status'))).json()).configured,false);
 const live=createHandler({env,logger:silent});for(let i=0;i<5;i++)assert.equal((await live(request('login',{password:'wrong'}))).status,401);assert.equal((await live(request('login',{password:env.VOICE_PASSWORD}))).status,429);
 assert.equal((await live(request('login',{password:'x'.repeat(17000)}))).status,400);
 const r=await live(new Request(origin+'/api/voice?action=login',{method:'POST',headers:{Origin:origin,'Content-Type':'text/plain'},body:'{}'}));assert.equal(r.status,400);
});
test('rotating password or signing secret invalidates existing sessions; upstream failures do not expose details',async()=>{
 const mutable={...env};const handler=createHandler({env:mutable,logger:()=>{},apiFetch:async()=>({ok:false,status:401,text:async()=>env.OPENAI_API_KEY})});let r=await handler(request('login',{password:env.VOICE_PASSWORD}));const Cookie=r.headers.get('set-cookie').split(';')[0];r=await handler(request('session',{context:'ok'},{Cookie}));assert.equal(r.status,502);assert.ok(!(await r.text()).includes(env.OPENAI_API_KEY));mutable.VOICE_PASSWORD+='changed';assert.equal((await (await handler(request('status',undefined,{Cookie}))).json()).authenticated,false);
 mutable.VOICE_PASSWORD=env.VOICE_PASSWORD;mutable.VOICE_SESSION_SECRET+='changed';assert.equal((await (await handler(request('status',undefined,{Cookie}))).json()).authenticated,false);
});
test('configuration diagnostics identify missing or short variables without returning secret values',async()=>{
 const custom={...env,VOICE_PASSWORD:'short',VOICE_SESSION_SECRET:''};const handler=createHandler({env:custom,logger:()=>{}});const data=await (await handler(request('status'))).json();assert.equal(data.configured,false);assert.deepEqual(data.configurationIssues,['VOICE_PASSWORD must contain at least 16 characters','VOICE_SESSION_SECRET is missing']);const response=await handler(request('login',{password:'anything'}));assert.equal(response.status,503);const text=await response.text();assert.match(text,/password has not been checked/);assert.match(text,/redeploy/);for(const secret of [env.OPENAI_API_KEY,custom.VOICE_PASSWORD])assert.ok(!text.includes(secret));
});
