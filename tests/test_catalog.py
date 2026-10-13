import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from catalog import unit_cost, validate, load, url_valid, eligible
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
            self.assertNotIn('?',p['official_url']); self.assertNotIn('#',p['official_url'])
    def test_private_redirect(self):
        with self.assertRaises(ValueError):
            PublicRedirect().redirect_request(None,None,302,'',{},'https://127.0.0.1/')

if __name__=='__main__': unittest.main()
