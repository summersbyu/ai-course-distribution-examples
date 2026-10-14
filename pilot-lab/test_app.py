"""Exercise the student UI without spending Codespaces or AI credit."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from streamlit.testing.v1 import AppTest

sys.path.insert(0, str(Path(__file__).parent))

class StudentWorkflow(unittest.TestCase):
    def test_form_query_evidence_and_new_app_session(self):
        with tempfile.TemporaryDirectory() as folder:
            os.environ['ACCOUNTING_LAB_DB'] = str(Path(folder) / 'expenses.db')
            import lab
            lab.DB_PATH = Path(os.environ['ACCOUNTING_LAB_DB'])
            at = AppTest.from_file(str(Path(__file__).parent / 'app.py')).run(timeout=20)
            self.assertFalse(at.exception)
            at.radio(key='section').set_value('Enter expenses').run()
            for vendor,category,amount in [('Campus Office Supply','Office supplies',125.50),('Mountain Travel','Travel',300.00),('Ledger Software','Software',49.99)]:
                at.text_input(key='vendor').set_value(vendor)
                at.selectbox(key='category').set_value(category)
                at.number_input(key='amount').set_value(amount)
                at.button[0].click().run()
                self.assertFalse(at.exception)
                self.assertTrue(at.success)
            at.radio(key='section').set_value('SQL practice').run()
            at.text_area(key='prediction').set_value('The total is 475.49')
            at.text_area(key='sql').set_value('SELECT SUM(amount_cents) / 100.0 AS total_dollars FROM expenses;')
            at.button[0].click().run()
            self.assertEqual(float(at.dataframe[0].value.iloc[0,0]),475.49)
            at.text_area(key='sql').set_value('DELETE FROM expenses;')
            at.button[0].click().run()
            self.assertTrue(at.error)
            self.assertEqual(lab.summary(),(3,47549))
            at.radio(key='section').set_value('Save and resume').run()
            at.text_area(key='reflection_input').set_value('I checked the total independently.')
            at.button[0].click().run()
            at.button[1].click().run()
            self.assertFalse(at.exception)
            self.assertIn(b'I checked the total independently.',lab.evidence())
            identity = lab.meta('lab_id')
            # A fresh app session simulates a new browser connection, not a live Codespaces lifecycle.
            resumed = AppTest.from_file(str(Path(__file__).parent / 'app.py')).run(timeout=20)
            self.assertFalse(resumed.exception)
            self.assertEqual(lab.meta('lab_id'),identity)
            self.assertEqual(lab.summary(),(3,47549))
            resumed.radio(key='section').set_value('Help').run()
            self.assertFalse(resumed.exception)
            os.environ.pop('ACCOUNTING_LAB_DB',None)

if __name__ == '__main__':
    unittest.main()
