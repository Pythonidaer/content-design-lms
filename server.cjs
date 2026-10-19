const http=require('node:http'),fs=require('node:fs/promises'),path=require('node:path');
const {session}=require('./voice-config.js');
const publicFiles=new Set(['index.html','lms.css','content-theme.css','lms-runtime.js','lesson-markdown.js','voice-config.js','voice.js','vendor/marked.umd.js','course.json','source-manifest.json']);
function createServer({apiFetch=fetch,apiKey=process.env.OPENAI_API_KEY}={}){
return http.createServer(async(req,res)=>{
 const host=req.headers.host||'';const trusted=/^(127\.0\.0\.1|localhost):\d+$/.test(host);if(!trusted){res.writeHead(403);res.end('Local access only.');return}
 res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Referrer-Policy','no-referrer');
 const pathname=new URL(req.url,'http://'+host).pathname;
 if(pathname==='/session'){
  res.setHeader('Cache-Control','no-store');
  if(req.method!=='POST'||!String(req.headers['content-type']).startsWith('application/json')||(req.headers.origin&&req.headers.origin!=='http://'+host)){res.writeHead(403);res.end('Same-origin JSON POST required.');return}
  let body='';try{for await(const chunk of req){body+=chunk;if(body.length>16000)throw Error('limit')}const input=JSON.parse(body);const key=String(apiKey||input.apiKey||'').trim();body='';if(!key.startsWith('sk-')){res.writeHead(400,{'Content-Type':'application/json'});res.end(JSON.stringify({error:'An OpenAI API key is required on the local helper.'}));return}
   const r=await apiFetch('https://api.openai.com/v1/realtime/client_secrets',{method:'POST',headers:{Authorization:'Bearer '+key,'Content-Type':'application/json'},body:JSON.stringify({expires_after:{anchor:'created_at',seconds:60},session:session(input.context)}),signal:AbortSignal.timeout(12000)});
   if(!r.ok){res.writeHead(r.status===401?401:502,{'Content-Type':'application/json'});res.end(JSON.stringify({error:'Could not create voice token. Check API credentials, billing, and model access.'}));return}
   const data=await r.json();res.writeHead(200,{'Content-Type':'application/json'});res.end(JSON.stringify({value:data.value,expires_at:data.expires_at}));
  }catch{res.writeHead(400,{'Content-Type':'application/json'});res.end(JSON.stringify({error:'Could not create the session. Check input or try again.'}))}return;
 }
 if(req.method!=='GET'&&req.method!=='HEAD'){res.writeHead(405);res.end();return}
 const file=pathname==='/'?'index.html':pathname.slice(1);if(!publicFiles.has(file)){res.writeHead(404);res.end('Not found');return}
 try{const data=await fs.readFile(path.join(__dirname,file));res.setHeader('Content-Type',file.endsWith('.css')?'text/css':file.endsWith('.js')?'text/javascript':file.endsWith('.json')?'application/json':'text/html; charset=utf-8');res.writeHead(200);res.end(req.method==='HEAD'?undefined:data)}catch{res.writeHead(404);res.end('Not found')}
});}
module.exports={createServer};
if(require.main===module){const port=Number(process.env.PORT)||8787;createServer().listen(port,'127.0.0.1',()=>console.log('Content design LMS: http://127.0.0.1:'+port+'\nVoice uses a server-side OPENAI_API_KEY or an unsaved key entered locally.'))}
