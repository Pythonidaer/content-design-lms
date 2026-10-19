from pathlib import Path
import json, copy
ROOT=Path(__file__).resolve().parent
base='https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/'
sources={
'understand':('Understand content design',base+'plan-manage-content/understand-content-design/'),
'standards':('Writing to GOV.UK standards',base),
'needs':('Identify user needs',base+'plan-manage-content/identify-user-needs/'),
'plan':('Plan new GOV.UK content',base+'plan-manage-content/plan-new-govuk-content/'),
'manage':('Manage existing GOV.UK content',base+'plan-manage-content/manage-existing-govuk-content/'),
'access':('Understand accessibility',base+'plan-manage-content/understand-accessibility/'),
'urls':('Follow URL standards',base+'plan-manage-content/follow-url-standards/'),
'localise':('Consider translations',base+'plan-manage-content/consider-translations/'),
'group':('Organise and group GOV.UK content',base+'plan-manage-content/organise-group-govuk-content/'),
'retire':('Retire outdated content',base+'plan-manage-content/retire-content/'),
'change':('Help users prepare for change',base+'help-users-prepare-change/'),
'tools':('Find tools and resources for analysing content',base+'find-tools-resources/'),
'write':('Write content to meet user needs',base+'writing-guidelines/meet-user-needs/'),
'structure':('Create a clear structure',base+'writing-guidelines/clear-structure/'),
'language':('Use clear language',base+'writing-guidelines/clear-language/'),
'govtone':('Use the right tone',base+'writing-guidelines/right-tone/'),
'links':('Write effective links',base+'writing-guidelines/add-links/'),
'titles':('Write clear titles',base+'writing-guidelines/clear-titles/'),
'summaries':('Write clear summaries',base+'writing-guidelines/summaries/'),
'notes':('Write change notes',base+'writing-guidelines/change-notes/'),
'style':('How to use the style guide',base+'style-guides/how-to-use/'),
'az':('A to Z style guide',base+'style-guides/a-to-z-style-guide/'),
'techaz':('Technical A to Z style guide',base+'style-guides/technical-a-to-z/'),
'dimensions':('NN/g: Four Dimensions of Tone of Voice','https://www.nngroup.com/articles/tone-of-voice-dimensions/'),
'samples':('NN/g: Tone-of-Voice Samples','https://www.nngroup.com/articles/tone-voice-samples/'),
'words':('NN/g: Tone-of-Voice Words','https://www.nngroup.com/articles/tone-voice-words/'),
'mailchimp':('Mailchimp: Voice and Tone','https://styleguide.mailchimp.com/voice-and-tone/')}
coverage={k:[] for k in sources}
def slide(id,title,body):return dict(id=id,title=title,body=body)
def lesson(id,title,src,principle,example,practice,check):
 for s in src:coverage[s].append(id)
 bodies=[(title,principle),('Example',example),('Try it',practice),('Review your answer',check),('Read further','\n\n'.join('['+sources[k][0]+']('+sources[k][1]+')' for k in src)+'\n\nThese links open in a new tab. Lessons are original summaries and examples; consult the guidance for detail.')]
 return dict(id=id,type='slides',title=title,slides=[slide(id+'-'+str(i+1),heading,body) for i,(heading,body) in enumerate(bodies)])
def quiz(id,title,skill,rows):return dict(id=id,type='quiz',title=title,skill=skill,questions=[dict(id=id+'-q'+str(i+1),prompt=r[0],options=r[1],answer=r[2],explanation=r[3]) for i,r in enumerate(rows)])
def sec(id,title,children):return dict(id=id,type='section',title=title,children=children)
start=[
lesson('orientation','How to use this course',['understand','standards'],
'Learn content design: deciding what people need, what to communicate, and how to make it understandable. The LMS is the delivery medium.\n\nFollow Start, then Explore, then Tone in practice. All lessons are available immediately.',
'A person needs to renew a membership. Useful content explains eligibility, price, required information, and the next action. A description of the organisation may not help them renew.',
'Choose one real page. Write the task its reader should be able to complete. Keep that page as your practice project.',
'A useful task names an outcome: “Renew my membership before it expires.” “Read our membership page” describes your delivery format, not the person’s goal. Lessons use fictional examples; exercises are self-assessed.'),
lesson('needs','Begin with a user need',['needs'],
'Identify who needs something, what they need to do, and why. Use research, enquiries, and observed behaviour. A stakeholder’s wish for a page is evidence to investigate, not proof of a user need.',
'“As a new member, I need to know whether equipment is included, so I can arrive prepared.” This can lead to a short preparation list rather than another marketing page.',
'Rewrite “We need a page promoting our premium plan” as a user need. What evidence would support it?',
'One possibility: “As a buyer, I need to compare plan limits so I can choose an affordable option.” Check support questions or observe people comparing plans. Treat an untested need as a hypothesis.'),
lesson('scope','Choose content and format',['understand','plan'],
'Check existing content before creating more. Decide what to include, remove, combine, or deliver elsewhere. Choose text, a form, a list, or another format based on the task. More content can create more work for readers.',
'A support page has a long essay about appointment booking. The task may need a booking form, preparation checklist, and short cancellation instructions instead.',
'For your practice page, identify one essential item, one distracting item, and a better format for a difficult explanation.',
'Keep information needed for decisions and actions. Remove or relocate organisational detail that does not support them. Test a changed format with users; do not assume a diagram or video is always clearer.'),
lesson('content-workflow','Draft and prototype together',['standards','write'],
'Content can begin in a document or spreadsheet. Put real wording into a prototype early, then revise wording and layout together. Content design includes selection, order, format, and maintenance as well as the final copy.',
'A form draft lists the field label, hint, validation rule, error, and confirmation. In a prototype, a long hint may need to become a separate explanation before the form.',
'Write a label, hint, and error for an email field. Check each in the space where it will appear.',
'Example: label “Email address”; hint “We’ll send your receipt here”; error “Enter an email address in the format name@example.com.” This is an authored example, not a universal form rule.'),
quiz('start-check','Start: knowledge check','User needs',[
('Which is a user outcome?',['Read our page','Find out whether I qualify','Publish a new section'],1,'Qualification supports a decision; reading and publishing describe activities.'),
('What should guide a content format?',['The user’s task and context','Always using slides','The longest available document'],0,'Choose a format that helps the person achieve their goal.'),
('When should real content enter a prototype?',['Only after launch','Early, with content and layout revised together','Never'],1,'Words and layout affect each other.')])]
explore=[]
def add(*args):explore.append(lesson(*args))
add('planning','Plan and organise',['plan','group'],'Plan where content belongs and how people will find it. Coordinate with existing pages and owners. Group related material using meaningful topics or steps. Navigation is one expression of that organisation, not the whole content plan.', 'A service has preparation, application, and follow-up tasks. A step-by-step route can connect them; unrelated policies need not interrupt the main journey.', 'Group your practice page’s information by task. Give each group a descriptive label.', 'Use labels readers recognise, then check whether they can find a specific answer. GOV.UK’s publishing structures are context-specific; adapt the principle rather than copying every government content type.')
add('structure','Structure for scanning',['structure'],'Put the most useful information first. Break content into short sections with meaningful headings. Use bullets for parallel items and numbered steps for ordered actions. Avoid repeating a summary in the opening paragraph.', 'Before: “Introduction”, followed by organisational history. After: “Renew your membership”, followed by cost, eligibility, and the renewal action.', 'Reorder an existing page so the reader sees the answer or next action before supporting detail.', 'A reader should understand the route from headings alone. Keep necessary context and exceptions near the relevant action; do not bury them simply to make a page shorter.')
add('language','Write in plain language',['language'],'Choose familiar words and concrete actions. Explain specialist terms when needed. Active voice usually makes the actor and action clearer. Plain language helps specialists too; it does not require removing accurate technical meaning.', 'Before: “Completion of the verification process is required prior to commencement.” After: “Verify your email before you start.”', 'Rewrite one long sentence from your page. Name the actor, use a direct verb, and remove words that add no meaning.', 'Check that the shorter version preserves the original condition. “You may apply” and “You must apply” are different; concise wording must remain accurate.')
add('titles','Write titles people recognise',['titles'],'A title should identify the subject or task with words readers search for. Make it specific enough to distinguish the page from similar pages. Put useful identifying words early.', '“Everything you need to know” reveals little. “Renew a library membership” tells a reader the task and the object.', 'Write two possible titles. Ask someone which page they would select to complete your intended task.', 'Prefer the title that predicts the content accurately. Search terms are evidence to consider, not a reason to repeat keywords unnaturally.')
add('summaries','Summarise without repeating',['summaries'],'Use a short summary to explain what a page helps someone do or understand. Add useful information beyond the title. Avoid opening the main text by repeating the same sentence.', 'Title: “Renew a membership”. Summary: “Check renewal costs and renew online before your membership expires.”', 'Draft a summary for your practice page. Remove anything already obvious from its title.', 'The summary should help a person decide whether this is the right page. Include material limits or audience details when they change that decision.')
add('links','Write useful link text',['links'],'A link should explain its destination or action without relying on surrounding text. Place links where they support a task. Avoid vague labels and competing routes that distract from the main action.', '“Read more” is ambiguous. “Check membership eligibility” predicts the destination. For a download, identify its format when that matters.', 'Replace three vague links with descriptive labels. Read each label in isolation.', 'A reader should be able to predict the destination. Do not imply a link submits information if it only opens another page.')
add('accessibility','Design accessible content',['access'],'Accessibility affects language, structure, formats, and alternatives. Use meaningful headings and descriptive links. Give useful text alternatives for informative images. Do not make meaning depend only on colour, position, or sound.', 'A chart’s green line means “approved”, but the caption also names the status and key finding. An audio explanation includes a transcript.', 'Find one visual or audio-only explanation on your page. Write an equivalent text explanation.', 'Describe the information needed for the task, not every decorative detail. Check the result with relevant accessibility guidance and users; an automated score alone does not establish usability.')
add('translations','Plan for translation',['localise'],'Consider language needs using evidence about the audience and task. Decide what needs translating and how translated versions stay current. Clear source content and stable terminology make translation easier.', 'A translated eligibility guide still shows last year’s threshold. The language is correct, but the information can lead to the wrong decision.', 'Identify who owns updates to each language version of your practice content.', 'Record review responsibility and the trigger for updating every version. Machine translation alone is not a quality or accuracy check.')
add('urls','Use understandable URLs',['urls'],'A URL should be stable, descriptive, and consistent with the site’s standards. Avoid unnecessary words and avoid changing addresses without considering existing links. GOV.UK’s exact URL rules apply to its publishing system.', 'A durable address describes the task, such as /membership/renew. An address tied to a temporary campaign may become misleading.', 'Suggest a stable path for your page. What would happen to existing links if you changed it?', 'Plan redirects and ownership when moving published content. A readable URL supports orientation; it does not replace a clear page title.')
add('maintenance','Maintain existing content',['manage'],'Content needs an accountable owner and a review plan. Audit what exists, identify duplication and outdated information, and use evidence to decide what to improve. Publication is the start of maintenance.', 'Two pages list different renewal prices. Fixing one sentence is not enough if another owner continues updating the duplicate page.', 'Record the owner, review trigger, and source of truth for your practice page.', 'Review when policy or service details change, not only on a calendar date. Where duplication causes conflict, coordinate consolidation and links.')
add('retirement','Retire outdated material',['retire'],'Decide whether old information should remain as a record, be withdrawn, or be removed. Explain what replaces it when readers still arrive. GOV.UK distinguishes retirement options within its publishing workflow.', 'A closed application page remains discoverable. A clear closure notice and link to the current programme can prevent wasted effort.', 'Choose one obsolete page. Explain what a visitor should see and where they should go instead.', 'Consider historical value, continuing user needs, redirects, and organisational requirements. Do not delete content solely because it is old.')
add('changes','Explain changes before they happen',['change'],'Help readers understand what is changing, who is affected, when it happens, and what they need to do. Explain the practical consequence rather than only announcing an internal policy name.', '“Our process is changing” gives no action. “From 1 June, renew online. Bring your current membership number” gives a date and a next step.', 'Draft a short notice with a date, affected audience, and required action.', 'Check whether someone can act before the change. Link to the current process and explain any transitional arrangement when needed.')
add('change-notes','Write useful change notes',['notes'],'When an update needs a change note, describe the substantive difference and its effect on users. Follow the publisher’s rules about which changes need notes. Avoid an unexplained “updated”.', '“Updated guidance” hides the change. “Added the new renewal fee for applications received from 1 June” explains what changed.', 'Write a change note for a revised eligibility threshold.', 'Name the changed rule and relevant date. Minor spelling fixes may not need a public note; check the publishing policy.')
add('style-guides','Use style guides as references',['style','az','techaz'],'Style guides provide consistent conventions for words, numbers, punctuation, and technical terms. Consult entries as needed rather than memorising an entire alphabetical list. Separate a publisher’s house style from a universal requirement.', 'A team decides how to format dates, refer to products, and introduce abbreviations. A shared reference avoids inconsistent choices across pages.', 'Look up one uncertain term in the A to Z guide and one in the technical guide. Record the decision and its context.', 'The complete guides are linked as reference material, not reproduced or exhaustively taught. Apply a house-style rule deliberately; retain accurate names and technical meaning.')
add('evaluate','Evaluate and improve',['tools','needs'],'Combine research with evidence such as support enquiries, search behaviour, and task performance. Analytics can reveal a problem but rarely explain it alone. Test whether people understand the content and can act.', 'Many visits to a help page could mean useful guidance or repeated confusion. Observing the task helps distinguish them.', 'Ask a person to use your page to make a decision. Observe hesitation before explaining anything.', 'Record what they misunderstood, revise the relevant content, and test again. Avoid treating reading time, clicks, or a readability score as proof of understanding.')
explore.append(quiz('explore-check','Explore: knowledge check','Content practice',[
('What belongs near the start of task guidance?',['The most useful answer or action','Organisational history by default','A repeated summary'],0,'Prioritise the reader’s task.'),
('Which link label best predicts a destination?',['Here','More','Check renewal costs'],2,'The label identifies the information the link opens.'),
('What supports ongoing content accuracy?',['Publication alone','An owner and review triggers','A decorative updated badge'],1,'Ownership and review support reliable maintenance.'),
('A page has high traffic. What follows?',['It must be clear','Investigate task success and user behaviour','Remove it immediately'],1,'Traffic alone does not explain whether a need is met.'),
('How should a house-style rule be treated?',['As an intentional publishing convention','As a law for every website','As more important than accurate meaning'],0,'Understand its scope before adopting it.')]))
tone=[
lesson('voice-tone','Separate voice from tone',['mailchimp'],
'Voice is a relatively consistent identity. Tone changes with the situation and the reader’s likely state. A friendly organisation can sound calm during a failure and more celebratory after an achievement.',
'A service may normally sound conversational. When payment fails, it should explain the problem and recovery action without joking about the user’s money.',
'Write one confirmation and one failure message for the same service. Preserve its identity while changing emotional intensity.',
'Check what readers need at that moment. A friendly failure message still needs a cause, next step, and accurate account of what happened.'),
lesson('tone-dimensions','Compare tone along four dimensions',['dimensions'],
'NN/g offers four spectrums: formal/casual, serious/funny, respectful/irreverent, and matter-of-fact/enthusiastic. These qualities can combine. A position on a spectrum is a design choice, not a universal ranking.',
'Authored comparison: “Your draft was saved.” is matter-of-fact. “Your draft is saved. You’re ready to continue.” adds encouragement without changing the saved state.',
'Choose a message. Describe its position on the four dimensions, then change only one dimension.',
'Keep the underlying information constant so you can judge the tone change. Test whether readers perceive the intended qualities; your intended tone may differ from theirs.'),
lesson('gov-voice','Understand GOV.UK’s tone',['govtone'],
'GOV.UK aims for useful, direct, restrained communication with human authority. It addresses readers directly and avoids unnecessary ceremony. This is a particular public-service voice; it is not a requirement that every brand sound identical.',
'Authored example: “You can renew online until 30 June” gives a clear action and limit. “We are delighted to announce an exciting renewal opportunity” adds enthusiasm without helping the task.',
'Rewrite a promotional introduction as practical service guidance. Keep any eligibility conditions and deadlines.',
'Check clarity, precision, respectful wording, and who “we” refers to. Do not confuse brevity with withholding information a reader needs.'),
lesson('tone-testing','Compare and test tone',['samples','words'],
'Compare versions with the same facts and actions. Choose a few target qualities and qualities to avoid. Ask readers how the content sounds and whether they can complete the task.',
'Authored targets: authoritative without being condescending; encouraging without exaggerating; playful without blaming the reader. A tone label is a hypothesis about how writing will be perceived.',
'Write two versions of a reminder. Ask someone to describe each and explain what they would do next.',
'Use the published NN/g samples as a comparison reference. Our examples here are newly written. Evaluate comprehension and appropriateness as well as preference.')]
qualities=[
('Reassuring','Reduce uncertainty using accurate information.','Your draft is saved. You can return later.','Do not promise safety or recovery you cannot verify.','A file upload is still processing. Write a reassuring status without claiming it has finished.'),
('Authoritative','Communicate expertise with precise, supported guidance.','Use descriptive labels so readers can identify each link.','Authority does not require jargon or commands without explanation.','Explain why a vague link label needs revision without talking down to its writer.'),
('Instructional','Help someone perform an action in the right order.','Select a chapter, then choose a lesson.','Avoid vague verbs when a specific action matters.','Write the first two steps of a password reset.'),
('Conversational','Sound natural and approachable while remaining clear.','Where would you like to start?','Casual wording should not hide conditions or consequences.','Rewrite a formal welcome as a short conversation opener.'),
('Encouraging','Support progress with specific, truthful feedback.','The structure is correct. Check the value types next.','Avoid praise that claims mastery without evidence.','Give feedback after a partly correct answer.'),
('Empathetic','Acknowledge the situation and offer useful help.','Losing work is frustrating. Here are your recovery options.','Do not assume everyone feels the same emotion.','Write a response to a missed deadline that acknowledges the problem and explains options.'),
('Playful','Use lightness where the stakes and audience permit it.','Pip found the depot. The parcel needs a better label.','Humour should not blame readers or obscure important failures.','Add lightness to an optional practice activity, preserving its instructions.'),
('Urgent','Communicate a real time-sensitive consequence.','Your session expires in two minutes. Save your work.','Do not invent scarcity or use urgency to pressure a decision.','Write a reminder for a genuine approaching deadline.'),
('Neutral','Present information without added emotional intensity.','Three lessons remain.','Neutral does not mean vague or unhelpful.','Rewrite an exaggerated update as a factual status.'),
('Celebratory','Recognise an actual achievement proportionately.','Chapter completed. You identified all six value types.','Keep the achievement specific and avoid overstating capability.','Write a completion message that names what was accomplished.')]
reference=[]
for i,(name,purpose,example,caution,exercise) in enumerate(qualities):
 reference.append(slide('tone-quality-'+str(i+1),name,purpose+'\n\n**Example:** '+example+'\n\n**Watch for:** '+caution+'\n\n**Try:** '+exercise))
reference.insert(0,slide('tone-reference-intro','A practical tone reference','The next ten slides are an authored teaching reference, not an official GOV.UK taxonomy or an exhaustive set of tones. Qualities overlap and can combine.\n\nUse context, purpose, audience, and testing to choose. Sources: [NN/g dimensions]('+sources['dimensions'][1]+') and [Mailchimp voice and tone]('+sources['mailchimp'][1]+').'))
tone.append(dict(id='tone-reference',type='slides',title='Ten tone qualities',slides=reference))
tone.append(lesson('capstone','Apply content design end to end',['understand','standards'],
'Bring the decisions together: need, evidence, content, structure, format, tone, and maintenance. The aim is a useful outcome for a reader rather than a particular writing style.',
'Fictional brief: a community centre changes its membership renewal process. Members need to know eligibility, costs, deadlines, and what to do if they cannot renew online.',
'Draft a title, summary, three headings, action label, failure message, and change notice. Explain your tone choices. Assign an owner and review trigger.',
'Self-check: can a member find the right action, understand its conditions, and recover from failure? Are facts verified, alternatives accessible, and ownership clear? Test the draft in its real layout. This exercise is self-assessed, not automatically graded.'))
tone.append(quiz('tone-check','Tone: knowledge check','Voice and tone',[
('What changes most with a reader’s situation?',['Tone','Every factual requirement','The definition of a link'],0,'Tone adapts while accuracy and useful information remain essential.'),
('Which is a tone dimension in NN/g’s framework?',['Formal to casual','Blue to green','Desktop to mobile'],0,'Formality is one of the framework’s four dimensions.'),
('Which message suits an interrupted payment?',['You broke it!','Payment failed. No charge was made. Try again.','Great news, something happened!'],1,'Clear recovery guidance is useful. In a real service, verify the no-charge statement before using it.'),
('How should tone qualities be used?',['As a fixed universal taxonomy','As overlapping design targets tested in context','As a substitute for facts'],1,'The ten qualities are a practical authored reference, not a universal list.')]))
# Resource decks retain both starting URLs and all inventoried direct writing-standards guidance.
resources=[]
for group,keys in [('Start resources',['understand','standards']),('Explore: plan and manage',['needs','plan','manage','access','urls','localise','group','retire','change','tools']),('Explore: writing guidance',['write','structure','language','govtone','links','titles','summaries','notes']),('Explore: reference guides',['style','az','techaz']),('Tone resources',['dimensions','samples','words','mailchimp'])]:
 sid='resources-'+str(len(resources)+1)
 resources.append(slide(sid,group,'\n\n'.join('['+sources[k][0]+']('+sources[k][1]+')' for k in keys)+'\n\nExternal resources open in a new tab. Use these to explore detail beyond the short lessons.'))
# Split resource slides to keep link lists short.
resources=[]
for i in range(0,len(sources),4):
 keys=list(sources)[i:i+4];resources.append(slide('resource-list-'+str(i),'Source directory '+str(i//4+1),'\n\n'.join('['+sources[k][0]+']('+sources[k][1]+')' for k in keys)+'\n\nOriginal sources. Open in a new tab.'))
resources.insert(0,slide('resource-scope','What the sources cover','Start with Understand content design, then explore Writing to GOV.UK standards. This course adapts the core planning and writing topics linked directly from that section.\n\nThe full A to Z and technical style guides remain lookup references. We do not claim to reproduce every GOV.UK publication, publishing-tool instruction, or alphabetical entry.'))
sections=[sec('stage-start','1 Start',start),sec('stage-explore','2 Explore',explore),sec('stage-tone','3 Tone in practice',tone),sec('stage-sources','4 Sources',[dict(id='source-directory',type='slides',title='Source directory and scope',slides=resources)])]
final=[]
for s in sections:
 for n in s['children']:
  if n['type']=='quiz':
   for q in n['questions']:
    q=copy.deepcopy(q);q['id']='final-'+q['id'];final.append(q)
course=dict(schemaVersion=1,id='content-design-course-v1',title='Content design',description='Learn user-centred content design through GOV.UK guidance, original practice, and context-sensitive voice and tone.',sections=sections,settings=dict(passScore=80,allowRetakes=True,showLessonDetails=False,unlockAll=True,sequential=False,requireLessons=True,brand='#1d70b8',background='#ffffff',surface='#f3f2f1',text='#0b0c0c',muted='#505a5f',border='#b1b4b6',fontScale=1,spacing=24,contentWidth=850,radius=2,font='system',headingFont='system',lineHeight=1.6),finalQuiz=dict(id='content-design-final',type='quiz',title='Final review',skill='Content design review',questions=final))
(ROOT/'course.json').write_text(json.dumps(course,indent=2,ensure_ascii=False)+'\n')
manifest=dict(retrieved='2026-10-18',scope='Core content-design principles and the directly linked writing-standards planning/writing guidance. A to Z and technical A to Z are linked lookup references. Original summaries, original practice, no complete-site reproduction.',sources=[dict(id=k,title=t,url=u,lessonIds=coverage[k],coverage='reference' if k in ['az','techaz'] else 'adapted-orientation' if k=='standards' else 'adapted') for k,(t,u) in sources.items()])
(ROOT/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
html='''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0b0c0c"><meta name="description" content="A content design course based on GOV.UK guidance with examples, practice, and voice and tone lessons."><title>Content design</title><link rel="stylesheet" href="lms.css"><link rel="stylesheet" href="content-theme.css"><script src="vendor/marked.umd.js" defer></script><script src="lesson-markdown.js" defer></script><script src="lms-runtime.js" defer></script><script src="voice-config.js" defer></script><script src="voice-access.js" defer></script><script src="voice.js" defer></script></head><body class="lms-export-body"><div id="lms-root"></div><script id="lms-course-data" type="application/json">'''+json.dumps(course,ensure_ascii=False).replace('<','\\u003c')+'''</script></body></html>\n'''
(ROOT/'index.html').write_text(html)
print(json.dumps({'lessons':sum(n['type']=='slides' for s in sections for n in s['children']),'slides':sum(len(n.get('slides',[])) for s in sections for n in s['children']),'sources':len(sources),'reviewQuestions':len(final)}))
