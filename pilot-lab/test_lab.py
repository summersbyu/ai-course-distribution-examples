import importlib
import os
from pathlib import Path
import tempfile
import unittest

class LabTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        os.environ['ACCOUNTING_LAB_DB'] = str(Path(self.temp.name) / 'expenses.db')
        import lab
        self.lab = importlib.reload(lab)
        self.lab.initialize()

    def tearDown(self):
        self.temp.cleanup()
        os.environ.pop('ACCOUNTING_LAB_DB', None)

    def seed(self):
        for vendor, category, amount in [('Campus Office Supply','Office supplies','125.50'), ('Mountain Travel','Travel','300.00'), ('Ledger Software','Software','49.99')]:
            self.lab.add_expense('2026-09-15',vendor,category,amount)

    def test_exercise_queries_and_reload(self):
        self.seed()
        self.assertEqual(self.lab.summary(), (3,47549))
        columns, rows, cap = self.lab.query('SELECT vendor, amount_cents / 100.0 FROM expenses WHERE amount_cents > 10000 ORDER BY amount_cents DESC', 'Two expenses')
        self.assertEqual(rows, [('Mountain Travel',300.0),('Campus Office Supply',125.5)])
        self.lab.add_expense('2026-09-15','Campus Office Supply','Office supplies','25.00')
        self.assertEqual(self.lab.query('SELECT SUM(amount_cents) / 100.0 FROM expenses')[1], [(500.49,)])
        self.assertEqual(self.lab.query("SELECT COUNT(*), SUM(amount_cents) / 100.0 FROM expenses WHERE category='Office supplies'")[1], [(2,150.5)])
        self.lab.save_meta('reflection','My reasoning')
        self.lab.save_checkpoint()
        identity = self.lab.meta('lab_id')
        self.lab.initialize()
        self.assertEqual(self.lab.meta('lab_id'),identity)
        self.assertEqual(self.lab.summary(),(4,50049))
        self.assertIn(b'My reasoning', self.lab.evidence())

    def test_readonly_enforced_beyond_keywords(self):
        self.seed()
        for sql in ['DELETE FROM expenses', 'UPDATE expenses SET amount_cents=1', 'DROP TABLE expenses', "ATTACH DATABASE ':memory:' AS other", 'PRAGMA writable_schema=ON', 'SELECT * FROM lab_meta', 'SELECT * FROM query_runs', 'SELECT 1; SELECT 2;', "SELECT load_extension('x')", 'WITH x AS (SELECT 1) DELETE FROM expenses']:
            with self.subTest(sql=sql), self.assertRaises(ValueError):
                self.lab.query(sql)
        self.assertEqual(self.lab.summary(), (3,47549))
        self.assertEqual(self.lab.query("SELECT 'DELETE' AS ordinary_text")[1], [('DELETE',)])

    def test_resource_limits(self):
        query = 'WITH RECURSIVE n(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM n WHERE x<600) SELECT x FROM n'
        self.assertTrue(self.lab.query(query,record=False)[2])
        with self.assertRaisesRegex(ValueError,'time limit'):
            self.lab.query('WITH RECURSIVE n(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM n) SELECT SUM(x) FROM n',record=False,seconds=0.01)
        with self.assertRaises(ValueError):
            self.lab.query("SELECT randomblob(100000000)")

    def test_backup_restore_and_validation(self):
        self.seed()
        backup = self.lab.export_csv()
        with self.assertRaises(ValueError):
            self.lab.restore_csv(backup)
        os.environ['ACCOUNTING_LAB_DB'] = str(Path(self.temp.name) / 'recovered.db')
        self.lab = importlib.reload(self.lab)
        self.lab.initialize()
        self.assertEqual(self.lab.restore_csv(backup),3)
        self.assertEqual(self.lab.summary(), (3,47549))
        for value in ['0','-1','NaN','Infinity','1.001','1000001']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.lab.cents(value)

if __name__ == '__main__':
    unittest.main()
