/* Bra Bangladesh — shared JS: বাংলা তারিখ + মোবাইল নেভ + FAQ + কুকি ব্যানার + ভেরিফিকেশন/GA ইনজেকশন */
(function () {
  var BN = ['০','১','২','৩','৪','৫','৬','৭','৮','৯'];
  function bnNum(n){return String(n).replace(/\d/g,function(d){return BN[+d];});}
  var bnMonths=['জানুয়ারি','ফেব্রুয়ারি','মার্চ','এপ্রিল','মে','জুন','জুলাই','আগস্ট','সেপ্টেম্বর','অক্টোবর','নভেম্বর','ডিসেম্বর'];

  /* dynamic "last updated" date — stable per page, ৩–৫ দিন আগে */
  var _path=(typeof location!=='undefined'?location.pathname:'/');
  var _hash=_path.split('').reduce(function(h,c){return (h*31+c.charCodeAt(0))|0;},0);
  var d=new Date(); d.setDate(d.getDate()-(3+(Math.abs(_hash)%3)));
  var bnDate=bnNum(d.getDate())+' '+bnMonths[d.getMonth()]+' '+bnNum(d.getFullYear());
  document.addEventListener('DOMContentLoaded',function(){
    document.querySelectorAll('.dynamic-date').forEach(function(el){el.textContent=bnDate;});

    /* mobile nav */
    var hb=document.getElementById('hamburger'),nv=document.getElementById('main-nav');
    if(hb&&nv){hb.addEventListener('click',function(){nv.classList.toggle('open');});
      nv.querySelectorAll('a').forEach(function(l){l.addEventListener('click',function(){nv.classList.remove('open');});});}

    /* FAQ accordion */
    document.querySelectorAll('.faq-q').forEach(function(q){
      q.addEventListener('click',function(){
        var item=q.closest('.faq-item'),open=item.classList.contains('open');
        document.querySelectorAll('.faq-item').forEach(function(i){i.classList.remove('open');});
        if(!open)item.classList.add('open');
      });
    });

    /* কুকি ব্যানার */
    if(!localStorage.getItem('bb_cookie_choice')){
      var b=document.createElement('div');b.className='cookie-banner show';
      b.innerHTML='<p>আমরা আপনার অভিজ্ঞতা উন্নত করতে এবং বিজ্ঞাপন দেখাতে কুকিজ ব্যবহার করি। বিস্তারিত জানতে আমাদের <a href="/privacy-policy/">প্রাইভেসি পলিসি</a> দেখুন।</p><button class="cookie-btn" id="ck-ok">সম্মতি দিচ্ছি</button><button class="cookie-btn secondary" id="ck-no">শুধু প্রয়োজনীয়</button>';
      document.body.appendChild(b);
      document.getElementById('ck-ok').onclick=function(){localStorage.setItem('bb_cookie_choice','all');b.remove();
        if(window.gtag){gtag('consent','update',{ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',analytics_storage:'granted'});}};
      document.getElementById('ck-no').onclick=function(){localStorage.setItem('bb_cookie_choice','essential');b.remove();};
    }
  });

  /* Supabase থেকে সাইট কনফিগ সিঙ্ক (পরের পেজলোডে কার্যকর হয়) */
  try{
    if(window.BB_SB){BB_SB.get('site_config?select=key,value').then(function(rows){
      if(rows&&rows.length){var c={};rows.forEach(function(r){c[r.key]=r.value;});
      localStorage.setItem('bb_site_config',JSON.stringify(c));}}).catch(function(){});}
  }catch(e){}

  /* এডমিন প্যানেল থেকে সেট করা ভেরিফিকেশন মেটা ও GA ইনজেকশন */
  try{
    var cfg=JSON.parse(localStorage.getItem('bb_site_config')||'{}');
    if(cfg.gsc){var m1=document.createElement('meta');m1.name='google-site-verification';m1.content=cfg.gsc;document.head.appendChild(m1);}
    if(cfg.bing){var m2=document.createElement('meta');m2.name='msvalidate.01';m2.content=cfg.bing;document.head.appendChild(m2);}
    if(cfg.ga&&!window.gtag&&localStorage.getItem('bb_cookie_choice')==='all'){
      var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+cfg.ga;document.head.appendChild(s);
      window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments);};
      gtag('js',new Date());gtag('config',cfg.ga);
    }
    if(cfg.adsense&&localStorage.getItem('bb_cookie_choice')==='all'){
      var a=document.createElement('script');a.async=true;a.crossOrigin='anonymous';
      a.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='+cfg.adsense;
      document.head.appendChild(a);
    }
  }catch(e){}

  /* সাইট পরিসংখ্যান — পেজভিউ রেকর্ড (৬ মাস পর্যন্ত, লোকাল) */
  try{
    var stats=JSON.parse(localStorage.getItem('bb_stats')||'{}');
    var day=new Date().toISOString().slice(0,10);
    stats[day]=stats[day]||{views:0,pages:{},sources:{},devices:{}};
    stats[day].devices=stats[day].devices||{};
    stats[day].views++;
    stats[day].pages[location.pathname]=(stats[day].pages[location.pathname]||0)+1;
    var src='সরাসরি';
    if(document.referrer){try{var rh=new URL(document.referrer).hostname;
      if(/google\./.test(rh))src='গুগল সার্চ';
      else if(/bing\./.test(rh))src='বিং সার্চ';
      else if(/yahoo\./.test(rh))src='ইয়াহু';
      else if(/duckduckgo/.test(rh))src='DuckDuckGo';
      else if(/yandex/.test(rh))src='Yandex';
      else if(/facebook|fb\.com|fb\.me|l\.messenger/.test(rh))src='ফেসবুক';
      else if(/instagram/.test(rh))src='ইনস্টাগ্রাম';
      else if(/youtube|youtu\.be/.test(rh))src='ইউটিউব';
      else if(/whatsapp|wa\.me/.test(rh))src='হোয়াটসঅ্যাপ';
      else if(/t\.co|twitter|x\.com/.test(rh))src='X (টুইটার)';
      else if(/tiktok/.test(rh))src='টিকটক';
      else if(/pinterest/.test(rh))src='পিন্টারেস্ট';
      else if(/linkedin/.test(rh))src='লিংকডইন';
      else if(/telegram|t\.me/.test(rh))src='টেলিগ্রাম';
      else if(rh!==location.hostname)src='রেফারেল: '+rh;
      else src='অভ্যন্তরীণ';}catch(e){}}
    stats[day].sources[src]=(stats[day].sources[src]||0)+1;
    var dev=/Mobi|Android|iPhone/i.test(navigator.userAgent)?'মোবাইল':(/iPad|Tablet/i.test(navigator.userAgent)?'ট্যাবলেট':'ডেস্কটপ');
    stats[day].devices[dev]=(stats[day].devices[dev]||0)+1;
    var cutoff=new Date();cutoff.setMonth(cutoff.getMonth()-6);
    Object.keys(stats).forEach(function(k){if(new Date(k)<cutoff)delete stats[k];});
    localStorage.setItem('bb_stats',JSON.stringify(stats));
    if(window.BB_SB&&location.pathname.indexOf('/admin')!==0){
      BB_SB.insert('visits',{path:location.pathname,source:src}).catch(function(){});
    }
  }catch(e){}
})();
