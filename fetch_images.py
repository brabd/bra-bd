# -*- coding: utf-8 -*-
"""Pexels থেকে আর্টিকেল ইমেজ ডাউনলোড (কপিরাইট-ফ্রি, Pexels লাইসেন্স)।"""
import urllib.request, json, os

KEY = 'IGUNbIfmJROBXikVXNGjOa98NEsriqoa9OgPDCaqEkQ6gZwcI9uvlRUU'
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site', 'images')

# slug -> (folder, search query)  — শালীন ও প্রাসঙ্গিক কোয়েরি
IMAGES = {
 'bra-size-measurement-guide': ('size-fitting','measuring tape tailor'),
 'wrong-bra-size-signs': ('size-fitting','woman mirror dressing room'),
 'cup-size-band-size-explained': ('size-fitting','clothing store rack sizes'),
 'bra-types-guide': ('bra-types','lingerie shop display'),
 'sports-bra-guide': ('bra-types','woman jogging exercise outdoor'),
 'tshirt-bra-vs-pushup': ('bra-types','folded clothes fabric pastel'),
 'how-to-wash-bra': ('care-cleaning','hand washing clothes basin'),
 'bra-storage-tips': ('care-cleaning','organized drawer clothes'),
 'when-to-replace-bra': ('care-cleaning','laundry clothesline drying'),
 'first-bra-guide': ('health-comfort','mother teenage daughter shopping'),
 'maternity-nursing-bra': ('health-comfort','mother newborn baby'),
 'bra-myths': ('health-comfort','woman thinking reading'),
}

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': KEY, 'User-Agent':'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=30).read()

for slug,(folder,q) in IMAGES.items():
    dest = os.path.join(ROOT,'articles',folder,slug+'.jpg')
    if os.path.exists(dest): print('skip',slug); continue
    try:
        data = json.loads(get('https://api.pexels.com/v1/search?query='+urllib.parse.quote(q)+'&per_page=3&orientation=landscape'))
        photos = data.get('photos',[])
        if not photos: print('NONE:',slug,q); continue
        src = photos[0]['src']['large']
        img = urllib.request.urlopen(urllib.request.Request(src,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read()
        os.makedirs(os.path.dirname(dest),exist_ok=True)
        open(dest,'wb').write(img)
        print('OK:',slug,len(img)//1024,'KB','photographer:',photos[0].get('photographer'))
    except Exception as e:
        print('ERR:',slug,e)
print('done')
