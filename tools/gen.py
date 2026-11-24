import csv, glob, json, re, sys
base = '/home/claude/trb-tribute-platform/TRB_Research/TRB_Dedication-Pricing/'
files = [base+'TRB_Dedication-Pricing-Master-Dataset.csv'] + sorted(glob.glob(base+'workstreams/track-05/*Batch*.csv'))
GROUP = {'senior_living':'senior','private_residential':'neighborhood','municipality':'city',
 'botanical_garden':'garden','arboretum':'garden','conservancy':'garden','public_park':'garden',
 'nature_center':'garden','cultural_institution':'garden','university':'campus','club':'club','resort':'club','other':'garden'}
COUNTRY = {'US':'','UK':'England','CA':'Canada','NZ':'New Zealand','IE':'Ireland','AU':'Australia'}
SYM = {'USD':'$','GBP':'£','CAD':'C$','EUR':'€','AUD':'A$','NZD':'NZ$'}
CURNAME = {'GBP':'British pounds','CAD':'Canadian dollars','EUR':'euros','AUD':'Australian dollars','NZD':'New Zealand dollars'}
def money(c,v): return SYM.get(c,'')+f"{int(float(v)):,}"
places = {}
seen=set()
for f in files:
  for r in csv.DictReader(open(f)):
    if r['record_id'] in seen: continue
    seen.add(r['record_id'])
    ts=r['tree_status']
    gift = 'new' if ts in ('new','new_or_recent') else 'existing' if ts.startswith('existing_') and ts!='existing_or_new' else 'either' if ts=='existing_or_new' else 'unclear'
    size = {'existing_heritage':'Landmark tree','existing_established':'Mature tree','existing_recent':'Recently planted','new_or_recent':'Young tree'}.get(ts,'')
    tt=r['term_type']; ty=r['term_years']
    if tt in ('fixed','minimum_fixed') and ty: term=('years',f"{ty} years" + (' or more' if tt=='minimum_fixed' else ''))
    elif tt in ('tree_life','tree_life_minimum'): term=('life','Life of the tree')
    elif tt in ('perpetual','permanent_wording'): term=('permanent','Called permanent')
    else: term=('unknown','Length not stated')
    phys=r['physical_recognition'].strip(); dig=r['digital_recognition'].strip()
    noplaque = (not phys) or re.search(r'^(no |none)|digital only|prohibited|typically no|no site plaque|no marker|no plaque',phys,re.I)
    plaque = not noplaque
    online = bool(dig)
    c=r['currency']; pb=r['price_basis']; lo=r['price_min']; hi=r['price_max']
    if pb in ('fixed',) or (lo and hi==lo): price=money(c,lo)
    elif pb in ('minimum','component_minimum'): price='From '+money(c,lo)
    elif pb=='estimated_range': price='About '+money(c,lo)+'–'+money(c,hi).replace(SYM.get(c,''),'')
    elif pb=='range': price=money(c,lo)+'–'+money(c,hi).replace(SYM.get(c,''),'')
    else: price=money(c,lo) if lo else 'Ask'
    extra=[]
    if pb=='component_minimum': extra.append('Price is for the plaque only')
    if r['availability']=='unknown': extra.append('Availability not confirmed')
    if c!='USD': extra.append('In '+CURNAME.get(c,c))
    region=r['region']; country=COUNTRY.get(r['country'],r['country'])
    where = region if r['country']=='US' else (region+', '+country if region!=country else country)
    key=r['organization']
    p=places.setdefault(key,{'name':key,'type':GROUP[r['segment']],'where':where,'us':r['country']=='US','checked':r['checked_on'],'offers':[]})
    details=[]
    gets=[x for x in [phys if plaque else (('No plaque' if phys else '')), ('Online: '+dig) if dig else ''] if x]
    if gets: details.append(['What the donor gets','; '.join(gets)])
    if r['selection']: details.append(['Choosing the tree',r['selection']])
    if r['payment']: details.append(['Paying',r['payment']])
    if r['death_policy']: details.append(['If the tree dies',r['death_policy']])
    p['offers'].append({'name':r['offering'],'gift':gift,'size':size,'term':term[0],'termLabel':term[1],
      'plaque':plaque,'online':online,'price':price,'usd':float(lo) if (c=='USD' and lo and pb!='component_minimum') else None,
      'extra':extra,'details':details})
# Programs with no posted price (my own words, from the coverage log)
ask=[('The Pines at Davidson','senior','NC','Level I arboretum. Donors pick from species and spots set by the landscape architect.'),
     ('Presbyterian Village Cobb','senior','GA','About 90 honor and memorial trees, with a QR-linked tree list and map.'),
     ('Kendal at Oberlin','senior','OH','Arboretum committee runs a commemorative tree program.'),
     ('Herons Glen Recreation District','neighborhood','FL','Donor pays the actual cost of the tree or palm and planting.')]
for n,t,w,d in ask:
  places[n]={'name':n,'type':t,'where':w,'us':True,'checked':'2026-11-23','ask':d,'offers':[]}
data=list(places.values())
if sys.argv[1]=="--json":
  open(sys.argv[2],"w").write(json.dumps(data,ensure_ascii=False,indent=0)); print(len(data),"places",sum(len(p["offers"]) for p in data),"offers"); sys.exit()
tpl=open(sys.argv[1]).read()
out=tpl.replace('__DATA__',json.dumps(data,ensure_ascii=False))
open(sys.argv[2],'w').write(out)
print(len(data),'places',sum(len(p['offers']) for p in data),'offers')
