/* Bra Bangladesh — অ্যাড সিস্টেম: ডামি/কাস্টম/AdSense অ্যাড রেন্ডার + ভিউ ও ক্লিক ট্র্যাকিং */
(function(){
  var DEFAULT_ADS={
    header:{enabled:true,type:'dummy',html:'',label:'হেডার ব্যানার (728×90)'},
    inArticle1:{enabled:true,type:'dummy',html:'',label:'আর্টিকেল অ্যাড ১'},
    inArticle2:{enabled:true,type:'dummy',html:'',label:'আর্টিকেল অ্যাড ২'},
    sidebar:{enabled:true,type:'dummy',html:'',label:'সাইডবার (300×250)'},
    footer:{enabled:true,type:'dummy',html:'',label:'ফুটার ব্যানার'}
  };
  function getAds(){try{var a=JSON.parse(localStorage.getItem('bb_ads')||'null');return a||DEFAULT_ADS;}catch(e){return DEFAULT_ADS;}}
  function track(slot,kind){
    try{var t=JSON.parse(localStorage.getItem('bb_ad_stats')||'{}');
    t[slot]=t[slot]||{views:0,clicks:0};t[slot][kind]++;
    localStorage.setItem('bb_ad_stats',JSON.stringify(t));}catch(e){}
  }
  document.addEventListener('DOMContentLoaded',function(){
    var ads=getAds();
    var cfg={};try{cfg=JSON.parse(localStorage.getItem('bb_site_config')||'{}');}catch(e){}
    document.querySelectorAll('[data-ad-slot]').forEach(function(el){
      var slot=el.getAttribute('data-ad-slot');
      var ad=ads[slot];
      if(!ad||!ad.enabled){el.style.display='none';return;}
      var box=slot==='sidebar';
      var inner;
      if(ad.type==='custom'&&ad.html){inner=ad.html;}
      else if(ad.type==='adsense'&&cfg.adsense){
        inner='<ins class="adsbygoogle" style="display:block" data-ad-client="'+cfg.adsense+'" data-ad-format="auto" data-full-width-responsive="true"></ins>';
      } else {
        inner='<div class="ad-dummy'+(box?' ad-box':'')+'">📢 বিজ্ঞাপনের স্থান — '+(ad.label||slot)+'</div>';
      }
      el.innerHTML='<div class="ad-slot-label">বিজ্ঞাপন</div>'+inner;
      track(slot,'views');
      el.addEventListener('click',function(){track(slot,'clicks');});
      if(ad.type==='adsense'&&window.adsbygoogle){try{(adsbygoogle=window.adsbygoogle||[]).push({});}catch(e){}}
    });
  });
})();
