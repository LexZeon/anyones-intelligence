
const modes=[...document.querySelectorAll('[data-set-mode]')];
modes.forEach(button=>button.addEventListener('click',()=>{document.body.dataset.mode=button.dataset.setMode;modes.forEach(x=>x.setAttribute('aria-pressed',String(x===button)));}));
const tocDialog=document.querySelector('#toc-dialog');
document.querySelector('.menu-button').addEventListener('click',()=>tocDialog.showModal());
document.querySelectorAll('[data-close]').forEach(button=>button.addEventListener('click',()=>button.closest('dialog').close()));
document.querySelectorAll('dialog').forEach(dialog=>dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();}));
document.querySelectorAll('.toc a').forEach(a=>a.addEventListener('click',()=>{if(tocDialog.open)tocDialog.close();}));
const zoom=document.querySelector('#figure-dialog');
document.querySelectorAll('.figure-button').forEach(button=>button.addEventListener('click',()=>{const img=button.querySelector('img').cloneNode(true);document.querySelector('.zoom-content').replaceChildren(img);zoom.showModal();}));
zoom.addEventListener('close',()=>document.querySelector('.zoom-content').replaceChildren());
const sections=[...document.querySelectorAll('.content-section')];
function sync(){if(!sections.length)return;const y=window.scrollY,total=document.documentElement.scrollHeight-innerHeight;document.querySelector('.progress').style.width=(total?100*y/total:0)+'%';let active=sections[0];for(const section of sections){if(section.getBoundingClientRect().top<180)active=section;}document.querySelectorAll('.toc a').forEach(a=>a.classList.toggle('active',a.hash==='#'+active.id));}
window.addEventListener('scroll',sync,{passive:true});sync();

document.querySelectorAll('.language-link').forEach(a=>a.addEventListener('click',()=>{if(location.hash)a.href=a.getAttribute('href').split('#')[0]+location.hash;}));
