// --- USER: Paste your actual links here or edit in the file directly ---
const links = {
  linkedin: 'https://www.linkedin.com/in/sahil-sharma-155697349?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3B7y%2B2WZJsSRuJFmyM8jQkDA%3D%3D',
  github: 'https://github.com/Sahilsharma9024',
  twitter: 'https://x.com/Sahilsharma9024?t=gq1AdoLdHz1GwJ6lldpOFQ&s=09',
  email: 'sahilsharmaas2006@gmail.com',
  whatsapp: 'https://wa.me/+919024442872'
};

// Gmail compose URL helper (always opens Gmail compose in a new tab)
function gmailComposeUrl(email, subject = '', body = ''){
  return 'https://mail.google.com/mail/?view=cm&fs=1&to=' + encodeURIComponent(email)
         + (subject ? '&su=' + encodeURIComponent(subject) : '')
         + (body ? '&body=' + encodeURIComponent(body) : '');
}
const gmailCTA = gmailComposeUrl(links.email, 'Hello Sahil', 'Hi Sahil,\n\nI would love to connect with you regarding your work.');

// Attach header social links
document.getElementById('link-linkedin').href = links.linkedin;
document.getElementById('link-github').href = links.github;
document.getElementById('link-twitter').href = links.twitter;
document.getElementById('link-whatsapp').href = links.whatsapp;

// Update email anchors to open Gmail compose instead of mailto
const emailAnchors = document.querySelectorAll('#link-email, #emailText');
emailAnchors.forEach(a => {
  if(!a) return;
  a.href = gmailCTA;
  a.target = '_blank';
  a.rel = 'noopener';
  // if it's a visible text node, keep readable email text
  if(a.id === 'emailText') a.textContent = links.email;
});

const headerGmail = document.getElementById('link-gmail');
if(headerGmail){
  headerGmail.href = gmailCTA;
  headerGmail.target = '_blank';
  headerGmail.rel = 'noopener';
}

// attach social section links (if present)
const map = {
  'soc-twitter': links.twitter,
  'soc-github': links.github,
  'soc-linkedin': links.linkedin,
  'soc-whatsapp': links.whatsapp,
  'soc-gmail': gmailCTA
};
Object.entries(map).forEach(([id, href]) => {
  const el = document.getElementById(id);
  if(!el) return;
  el.href = href;
  el.target = '_blank';
  el.rel = 'noopener';
});

// Resume handling — if you want to add resume, set resumeURL to your file path or URL
const resumeURL = '#';
const resumeBtn = document.getElementById('resumeBtn');
const resumeDL = document.getElementById('resumeDL');
if (resumeURL && resumeURL !== '#') { resumeBtn.href = resumeURL; resumeDL.href = resumeURL; resumeDL.style.display='inline-block'; } else { resumeBtn.style.display='none'; }

function copyEmail(){
  const email = links.email;
  navigator.clipboard.writeText(email).then(()=>{ alert('Email copied — ' + email); }).catch(()=>{ alert('Copy failed — copy manually.'); })
}

// ----- Improved Project toggle behavior (merged into your script) -----
document.addEventListener('DOMContentLoaded', () => {
  const projects = document.querySelectorAll('.project');
  projects.forEach(p => {
    const title = p.querySelector('.project-title');
    const desc = p.querySelector('.project-desc');
    const arrow = p.querySelector('.project-arrow');

    function open(){
      p.classList.add('open');
      title.classList.add('open');
      title.setAttribute('aria-expanded','true');
      desc.setAttribute('aria-hidden','false');
      // set exact max-height for smooth transition
      const h = desc.scrollHeight;
      desc.style.maxHeight = h + 'px';
      if(arrow) arrow.textContent = '▴';
      // subtle pulse animation
      p.animate([{boxShadow:'0 0 0 rgba(110,231,255,0.0)'},{boxShadow:'0 20px 60px rgba(110,231,255,0.03)'}],{duration:420,easing:'ease-out'});
    }
    function close(){
      p.classList.remove('open');
      title.classList.remove('open');
      title.setAttribute('aria-expanded','false');
      desc.setAttribute('aria-hidden','true');
      desc.style.maxHeight = '0px';
      if(arrow) arrow.textContent = '▾';
    }
    function toggle(){ if(desc.style.maxHeight && desc.style.maxHeight !== '0px') close(); else open(); }

    title.addEventListener('click', toggle);
    title.addEventListener('keydown', (e)=>{ if(e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); } });

    // close if clicked outside (optional behaviour)
    document.addEventListener('click', (ev)=>{ if(!p.contains(ev.target) && p.classList.contains('open')) close(); });
  });
});

// Section navigator scroll + highlight
const navButtons = document.querySelectorAll('[data-scroll-target]');
const panelToggle = document.getElementById('panelToggle');
const sidePanel = document.getElementById('sidePanel');

function openPanel(){
  if(!sidePanel || !panelToggle) return;
  sidePanel.classList.add('open');
  panelToggle.classList.add('open');
  panelToggle.setAttribute('aria-expanded','true');
  sidePanel.setAttribute('aria-hidden','false');
}
function closePanel(){
  if(!sidePanel || !panelToggle) return;
  sidePanel.classList.remove('open');
  panelToggle.classList.remove('open');
  panelToggle.setAttribute('aria-expanded','false');
  sidePanel.setAttribute('aria-hidden','true');
}
function togglePanel(){
  if(sidePanel.classList.contains('open')) closePanel(); else openPanel();
}
if(panelToggle) panelToggle.addEventListener('click', (e)=>{ e.stopPropagation(); togglePanel(); });

document.addEventListener('click', (e)=>{
  if(!sidePanel || !panelToggle) return;
  if(sidePanel.contains(e.target) || panelToggle.contains(e.target)) return;
  closePanel();
});
document.addEventListener('keydown', (e)=>{ if(e.key === 'Escape') closePanel(); });

navButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    const targetId = btn.getAttribute('data-scroll-target');
    const target = document.getElementById(targetId);
    if(!target) return;
    target.scrollIntoView({behavior:'smooth', block:'start'});
    target.classList.remove('focus-pulse');
    void target.offsetWidth;
    target.classList.add('focus-pulse');
    setTimeout(() => target.classList.remove('focus-pulse'), 900);
    closePanel();
  });
});

