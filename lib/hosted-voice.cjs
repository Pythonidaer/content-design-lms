const {createHash,createHmac,timingSafeEqual,randomBytes,randomUUID}=require('node:crypto');
const {session}=require('../voice-config.js');
const COOKIE='__Host-lms-voice',TTL=12*60*60;
const digest=v=>createHash('sha256').update(String(v)).digest();
function signature(payload,env){return createHmac('sha256',env.VOICE_SESSION_SECRET).update(env.VOICE_PASSWORD).update('\0').update(payload).digest('base64url')}
function configurationIssues(env){const issues=[];if(!String(env.OPENAI_API_KEY||'').trim())issues.push('OPENAI_API_KEY is missing');for(const [name,min]of [['VOICE_PASSWORD',16],['VOICE_SESSION_SECRET',32]]){const value=String(env[name]||'');if(!value)issues.push(name+' is missing');else if(value.length<min)issues.push(name+' must contain at least '+min+' characters')}return issues}
function configured(env){return configurationIssues(env).length===0}
function token(env,now){const payload=Buffer.from(JSON.stringify({exp:Math.floor(now/1000)+TTL,id:randomBytes(16).toString('hex')})).toString('base64url');return payload+'.'+signature(payload,env)}
function authorized(request,env,now){try{if(!configured(env))return false;const match=(request.headers.get('cookie')||'').split(';').map(v=>v.trim()).find(v=>v.startsWith(COOKIE+'='));if(!match)return false;const [payload,sig,...rest]=match.slice(COOKIE.length+1).split('.');if(rest.length||!payload||!sig)return false;const expected=signature(payload,env);if(!timingSafeEqual(digest(sig),digest(expected)))return false;const data=JSON.parse(Buffer.from(payload,'base64url'));return typeof data.id==='string'&&Number.isInteger(data.exp)&&data.exp>now/1000&&data.exp<=now/1000+TTL+10}catch{return false}}
function cookie(value,maxAge){return `${COOKIE}=${value}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=${maxAge}`}
async function readJSON(request){if(!request.headers.get('content-type')?.startsWith('application/json'))throw Error();const reader=request.body?.getReader();if(!reader)throw Error();let text='',size=0;const decoder=new TextDecoder();while(true){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;if(size>16000){await reader.cancel();throw Error()}text+=decoder.decode(value,{stream:true})}text+=decoder.decode();return JSON.parse(text)}
// Instance-local throttles are best effort, not a global/serverless quota. Configure Vercel Firewall too.
function createHandler({env=process.env,apiFetch=fetch,now=Date.now,logger=console.info}={}){
 const attempts=new Map();
 function throttle(key,limit,ms){const time=now();let v=attempts.get(key);if(!v||v.until<time){v={count:0,until:time+ms};attempts.set(key,v)}if(attempts.size>2000){for(const [k,v]of attempts)if(v.until<time)attempts.delete(k);if(attempts.size>2000)attempts.delete(attempts.keys().next().value)}return ++v.count>limit}
 return async function handle(request){
  const started=now(),requestId=randomUUID(),url=new URL(request.url),action=url.searchParams.get('action')||'status';
  const headers={'Cache-Control':'no-store','Content-Type':'application/json','X-Content-Type-Options':'nosniff','X-Request-Id':requestId};
  function result(status,data,event,extra={}){logger(JSON.stringify({event,requestId,status,durationMs:now()-started}));return new Response(JSON.stringify({...data,requestId}),{status,headers:{...headers,...extra}})}
  if(action==='status'&&request.method==='GET')return result(200,{configured:configured(env),configurationIssues:configurationIssues(env),authenticated:authorized(request,env,now())},'auth.status');
  if(!['login','logout','session'].includes(action))return result(404,{error:'Not found.'},'route.missing');
  if(request.method!=='POST')return result(405,{error:'POST required.'},'method.rejected',{'Allow':'POST'});
  const expectedOrigin=env.APP_ORIGIN||url.origin;
  if(request.headers.get('origin')!==expectedOrigin)return result(403,{error:'Origin not allowed.'},'origin.rejected');
  if(!configured(env))return result(503,{error:'Server setup needs attention: '+configurationIssues(env).join('; ')+'. Update Production environment variables and redeploy. Your entered password has not been checked.'},'config.missing');
  let input;try{input=await readJSON(request);if(!input||typeof input!=='object'||Array.isArray(input))throw Error()}catch{return result(400,{error:'Invalid request.'},'input.rejected')}
  if(action==='logout')return result(200,{authenticated:false},'auth.logout',{'Set-Cookie':cookie('',0)});
  if(action==='login'){
   const ip=request.headers.get('x-vercel-forwarded-for')||request.headers.get('x-forwarded-for')||'unknown';
   if(throttle('login:'+ip,5,60000))return result(429,{error:'Too many attempts. Wait a minute.'},'auth.throttled',{'Retry-After':'60'});
   if(typeof input.password!=='string'||!timingSafeEqual(digest(input.password),digest(env.VOICE_PASSWORD)))return result(401,{error:'Incorrect password.'},'auth.rejected');
   return result(200,{authenticated:true,expiresAt:now()+TTL*1000},'auth.login',{'Set-Cookie':cookie(token(env,now()),TTL)});
  }
  if(!authorized(request,env,now()))return result(401,{error:'Sign in to use voice.'},'auth.required');
  if(throttle('session',6,60000))return result(429,{error:'Wait a minute before starting another conversation.'},'session.throttled',{'Retry-After':'60'});
  if(typeof input.context!=='string'||input.context.length>6000)return result(400,{error:'Invalid slide context.'},'context.rejected');
  try{
   const upstream=await apiFetch('https://api.openai.com/v1/realtime/client_secrets',{method:'POST',headers:{Authorization:'Bearer '+env.OPENAI_API_KEY,'Content-Type':'application/json','OpenAI-Safety-Identifier':digest('content-design-private-owner').toString('hex')},body:JSON.stringify({expires_after:{anchor:'created_at',seconds:60},session:session(input.context)}),signal:AbortSignal.timeout(12000)});
   if(!upstream.ok)return result(502,{error:'OpenAI could not start voice. Check API billing and model access.'},'session.upstream_rejected');
   const data=await upstream.json();if(typeof data.value!=='string'||!data.value.startsWith('ek_'))throw Error();
   return result(200,{value:data.value,expires_at:data.expires_at},'session.created');
  }catch{return result(502,{error:'Voice connection could not be started. Try again.'},'session.failed')}
 };
}
module.exports={createHandler};
