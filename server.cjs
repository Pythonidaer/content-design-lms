const http=require('node:http'),fs=require('node:fs/promises'),path=require('node:path'),os=require('node:os');
const {session}=require('./voice-config.js');
const publicFiles=new Set(['index.html','lms.css','content-theme.css','lms-runtime.js','lesson-markdown.js','voice-config.js','voice-access.js','voice.js','vendor/marked.umd.js','course.json','source-manifest.json']);
function createServer({apiFetch=fetch,apiKey=process.env.OPENAI_API_KEY,configPath=path.join(os.homedir(),'.config','content-design-lms','voice.json')}={}){
return http.createServer(async(req,res)=>{
 const host=req.headers.host||'';const trusted=/^(127\.0\.0\.1|localhost):\d+$/.test(host);if(!trusted){res.writeHead(403);res.end('Local access only.');return}
 res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Referrer-Policy','no-referrer');
 const pathname=new URL(req.url,'http://'+host).pathname;
 const origin=req.headers.origin;
 const allowed=!origin||origin==='http://'+host||origin==='https://pythonidaer.github.io';
 const privateRoute=pathname==='/session'||pathname==='/config';
 if(privateRoute){
  res.setHeader('Cache-Control','no-store');
  if(!allowed){res.writeHead(403);res.end('Origin not allowed.');return}
  if(origin){res.setHeader('Access-Control-Allow-Origin',origin);res.setHeader('Vary','Origin');res.setHeader('Access-Control-Allow-Methods','GET, POST, DELETE, OPTIONS');res.setHeader('Access-Control-Allow-Headers','Content-Type');res.setHeader('Access-Control-Allow-Private-Network','true')}
  if(req.method==='OPTIONS'){res.writeHead(204);res.end();return}
 }
 async function savedKey(){try{return String(JSON.parse(await fs.readFile(configPath,'utf8')).apiKey||'')}catch(e){if(e.code==='ENOENT')return '';throw e}}
 async function inputJSON(){if(!String(req.headers['content-type']).startsWith('application/json'))throw Error('JSON required');let body='';for await(const chunk of req){body+=chunk;if(body.length>16000)throw Error('limit')}return JSON.parse(body)}
 if(pathname==='/config'){
  try{
   if(req.method==='GET'){res.setHeader('Content-Type','application/json');res.end(JSON.stringify({saved:!!await savedKey(),environment:!!apiKey}));return}
   if(req.method==='POST'){const input=await inputJSON();const key=String(input.apiKey||'').trim();if(!/^sk-[A-Za-z0-9_-]+$/.test(key))throw Error('Invalid key');await fs.mkdir(path.dirname(configPath),{recursive:true,mode:0o700});const handle=await fs.open(configPath,require('node:fs').constants.O_WRONLY|require('node:fs').constants.O_CREAT|require('node:fs').constants.O_NOFOLLOW,0o600);try{await handle.chmod(0o600);await handle.truncate(0);await handle.writeFile(JSON.stringify({apiKey:key})+'\n')}finally{await handle.close()}res.writeHead(204);res.end();return}
   if(req.method==='DELETE'){await inputJSON();await fs.rm(configPath,{force:true});res.writeHead(204);res.end();return}
   res.writeHead(405);res.end();
  }catch{res.writeHead(400);res.end('Could not update local voice configuration.')}return;
 }

 if(pathname==='/session'){
  res.setHeader('Cache-Control','no-store');
  if(req.method!=='POST'||!String(req.headers['content-type']).startsWith('application/json')){res.writeHead(403);res.end('JSON POST required.');return}
  try{const input=await inputJSON();const key=String(input.apiKey||apiKey||await savedKey()||'').trim();if(!key.startsWith('sk-')){res.writeHead(400,{'Content-Type':'application/json'});res.end(JSON.stringify({error:'An OpenAI API key is required on the local helper.'}));return}
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
if(require.main===module){const port=Number(process.env.PORT)||8787;createServer().listen(port,'127.0.0.1',()=>console.log('Content design LMS: http://127.0.0.1:'+port+'\nVoice keys can be saved from the modal to your private local configuration.'))}
