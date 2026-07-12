/* Bra Bangladesh — Supabase REST helper (publishable key, RLS enabled) */
window.BB_SB = (function(){
  var URL='https://glkvgagzaitkdofcfjuu.supabase.co/rest/v1/';
  var KEY='sb_publishable_BpTy9z9Q4I6fhDpeLY6amg_aPZoRgAo';
  function req(path,method,body,prefer){
    return fetch(URL+path,{method:method||'GET',
      headers:{apikey:KEY,Authorization:'Bearer '+KEY,'Content-Type':'application/json',Prefer:prefer||(method==='POST'?'return=minimal':'')},
      body:body?JSON.stringify(body):undefined})
      .then(function(r){return r.ok?(r.status===204||method==='POST'&&!prefer?null:r.json()):Promise.reject(r.status);});
  }
  return {
    get:function(q){return req(q);},
    insert:function(table,row){return req(table,'POST',row);},
    upsert:function(table,rows){return req(table,'POST',rows,'resolution=merge-duplicates,return=minimal');}
  };
})();
