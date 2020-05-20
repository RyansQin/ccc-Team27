import json
import os
import test as t

#- - - - - - - - -- - - - - - - - - Handler for the age distribution data - - - - - - - - - - - - - - -- - - - - - - - #
dic = {"tot_pop_denom":0, "_50_54_years_percent":6.2,"_65_69_years_percent":5.1,"_0_4_years_percent":6.2,"_80_84_years_percent":2.3,"_35_39_years_percent":6.1,"_45_49_years_percent":6.1,"_55_59_years_percent":6.3,"_40_44_years_percent":6.2,"_15_19_years_percent":7.1,"_25_29_years_percent":7.0,"_5_9_years_percent":6.0,"_10_14_years_percent":6.2,"_20_24_years_percent":7.8,"_85_years_over_percent":2.4,"_30_34_years_percent":6.4,"_60_64_years_percent":5.7,"_75_79_years_percent":3.0,"_70_74_years_percent":4.0}

region = ['qld', 'nsw', 'vic', 'act', 'wa', 'sa', 'nt', 'tas']

def initDict():
    res = {}
    for key in dic:
        res[key] = 0
    return res
res = {}
for r in region:
    res[r] = initDict()


file = open('age_distribution.json', encoding='utf8')
lst = file.read()
lst = json.loads(lst)
for p in lst['features']:
    popLst = p['properties']
    ans = res[popLst['ste_name']]
    for key in ans:
        if key is not 'tot_pop_denom':
            try:
                ans[key] += popLst[key]*float(popLst['tot_pop_denom'])/100
            except:
                print('skip none value')
        else:
            ans [key] += popLst["tot_pop_denom"]
    res[popLst['ste_name']] = ans
print(res)
for rt in res:
    r = res[rt]
    for key in r:
        if key is not 'tot_pop_denom':
            r[key] = 100*r[key]/r['tot_pop_denom']
    res[rt] = r
keySet = []
valueSet = []
locRes = []
finalRes = {}
for rt in res:
    locRes = []
    keySet = []
    valueSet = []
    locRes.append(rt)
    r = res[rt]
    for key in r:
        keySet.append(key)
        valueSet.append(r[key])
    locRes.append(keySet)
    locRes.append(valueSet)
    finalRes[rt] = locRes

print (finalRes)
t.testAddTweet('aurin_data', finalRes, "age_distribution")

#- - - - - - - - - - - -- - Handler for Tourism - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - #


resTourism = {}
resTourism['qld'] = 3.6 * 2360241
resTourism['nsw'] = 3.4 * 5131326
resTourism['vic'] = 3.3 * 5000000
resTourism['nt'] = 5.2 * 148564
resTourism['wa'] = 2.4 * 2059484
resTourism['act'] = 6.9 * 403208
resTourism['tas'] = 6.6 * 222000
resTourism['sa'] = 2.8 * 1345777
t.testAddTweet('aurin_data', resTourism, 'tourism')


# - - - - - - - - - - - - - - Handler for population density - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


resDensity = {}
resDensity['sa'] = 1345777/3258
resDensity['qld'] = 2360241/15826
resDensity['vic'] = 5000000/9900
resDensity['nsw'] = 5131326/12368
resDensity['nt'] = 148564/3164
resDensity['tas'] = 222000/1696
resDensity['wa'] = 2059484/6418
resDensity['act'] = 403208/2395


t.testAddTweet('aurin_data', resDensity, 'population_density')
