import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from catalog import unit_cost, validate, load, url_valid, eligible, overview_offer, recommendation, read, fresh, TODAY
from monitor import PublicRedirect

class CatalogTests(unittest.TestCase):
    def plan(self,reset,months=12):
        return {'reset':reset,'traffic_gb':200,'billing_months':months,'price':240,'multiplier':1,'fee_percent':None}
    def test_annual_reset_distinction(self):
        self.assertEqual(unit_cost(self.plan('monthly')),10)
        self.assertEqual(unit_cost(self.plan('total')),120)
    def test_forever_pack(self):
        self.assertEqual(unit_cost(self.plan('total',None)),120)
    def test_fee_multiplier(self):
        p=self.plan('monthly'); p.update(fee_percent=5,multiplier=2)
        self.assertEqual(unit_cost(p),21)
    def test_unlimited_excluded(self):
        p=self.plan('unlimited'); p['traffic_gb']=None
        self.assertIsNone(unit_cost(p))
    def test_blocked_provider_excluded(self):
        p={'status':'watch'}
        self.assertFalse(eligible(p,{'verified_at':'2026-10-13'}))
    def test_invalid_urls(self):
        for url in ['http://example.com','https://127.0.0.1','https://localhost','https://192.168.1.1','https://user:pass@example.com','https://example.com/?token=secret']:
            with self.subTest(url=url), self.assertRaises(ValueError): url_valid(url)
    def test_repository_integrity(self): validate()
    def test_invalid_monthly_period(self):
        ps=copy.deepcopy(load()); ps[0]['plans'][0].update(reset='monthly',billing_months=None)
        with self.assertRaises(AssertionError): validate(ps)
    def test_referrals_not_imported(self):
        for p in load():
            if p['official_url']:
                self.assertNotIn('?',p['official_url']); self.assertNotIn('#',p['official_url'])
    def test_private_redirect(self):
        with self.assertRaises(ValueError):
            PublicRedirect().redirect_request(None,None,302,'',{},'https://127.0.0.1/')
    def test_overview_price_quota_same_plan(self):
        p=next(p for p in load() if p['id']=='youtu')
        price,quota=overview_offer(p)
        self.assertIn('199 CNY/年',price)
        self.assertEqual(quota,'200 GB/年总量')
    def test_monthly_reset_annual_payment(self):
        p=next(p for p in load() if p['id']=='boostnet')
        price,quota=overview_offer(p)
        self.assertIn('200 CNY/年',price)
        self.assertEqual(quota,'20 GB/月')
    def test_candidate_does_not_claim_free_price(self):
        p=next(p for p in load() if p['id']=='dengta')
        price,quota=overview_offer(p)
        self.assertEqual(price,'待核验'); self.assertIn('活动记录',quota)
    def test_recommendation_issue_overrides_source(self):
        p=next(p for p in load() if p['id']=='wandayun')
        self.assertEqual(recommendation(p),'1/5 · 暂缓')
    def test_editorial_tier_does_not_claim_measurement(self):
        p=next(p for p in load() if p['id']=='boostnet')
        self.assertIn('来源主推',recommendation(p)); self.assertNotIn('实测',recommendation(p))
    def test_real_measurement_with_current_evidence(self):
        p=copy.deepcopy(load()[0]); p['status']='active'
        p['quality']={'tested_at':TODAY.isoformat(),'stability':80,'speed':80,'unlock':80,'support':80}
        self.assertEqual(recommendation(p),'4.0/5 · 实测')
    def test_source_lists_fully_mapped(self):
        items=read('config/coverage.json')['items']
        counts={key:sum(x['source']==key and x['section']==section for x in items) for key,section in [('hwanz-paid','当前推荐名单'),('panda','套餐对比表'),('hwanz-free','免费／试用名单')]}
        self.assertEqual(counts,{'hwanz-paid':12,'panda':17,'hwanz-free':62})
    def test_ambiguous_billing_excluded_from_cost(self):
        p=copy.deepcopy(next(p for p in load() if p['id']=='dageyun'))
        x=next(x for x in p['plans'] if x['price']==69)
        x['billing_ambiguous']=True
        self.assertIsNone(unit_cost(x))
        self.assertNotIn('69 CNY',overview_offer(p)[0])
    def test_owner_confirmed_quarterly_plan(self):
        p=copy.deepcopy(next(p for p in load() if p['id']=='dageyun'))
        x=next(x for x in p['plans'] if x['price']==69)
        self.assertEqual(x['billing_months'],3)
        self.assertFalse(x['billing_ambiguous'])
        self.assertEqual(unit_cost(x),11.5)
        p['plans']=[x]
        price,quota=overview_offer(p)
        self.assertIn('69 CNY/季',price); self.assertIn('23.00/月',price)
        self.assertEqual(quota,'200 GB/月')
    def test_screenshot_annual_quotas_reset_monthly(self):
        p=next(p for p in load() if p['id']=='dageyun')
        x=next(x for x in p['plans'] if x['price']==299)
        self.assertEqual(x['reset'],'monthly')
        self.assertAlmostEqual(unit_cost(x),299/(500*12)*100)
    def test_owner_primary_requires_personal_label(self):
        p=copy.deepcopy(next(p for p in load() if p['id']=='dageyun'))
        self.assertEqual(recommendation(p),'★★★★★ · 维护者主力')
        self.assertIsNone(p['quality'])
        p['status']='watch'; self.assertEqual(recommendation(p),'1/5 · 暂缓')

if __name__=='__main__': unittest.main()
