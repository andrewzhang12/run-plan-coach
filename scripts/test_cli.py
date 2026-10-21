import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from test_validator import fixture

SCRIPTS = Path(__file__).resolve().parent


def invoke(script, data):
    with tempfile.TemporaryDirectory() as folder:
        p=Path(folder)/'input.json';p.write_text(json.dumps(data))
        return subprocess.run([sys.executable,str(SCRIPTS/script),str(p)],capture_output=True,text=True)


class CLITests(unittest.TestCase):
    def test_intake_unknown_runner(self):
        r=invoke('intake.py',{});self.assertEqual(r.returncode,0);self.assertEqual(len(json.loads(r.stdout)['questions']),4)
    def test_consistent_exit_zero(self):
        r=invoke('validate_plan.py',fixture());self.assertEqual(r.returncode,0);self.assertEqual(json.loads(r.stdout)['physiological_validation'],'not_assessed')
    def test_unknown_exit_one(self):
        r=invoke('validate_plan.py',{});self.assertEqual(r.returncode,1)
    def test_invalid_exit_two(self):
        r=invoke('validate_plan.py',[]);self.assertEqual(r.returncode,2);self.assertIn('input_error',json.loads(r.stdout))

if __name__=='__main__':unittest.main()
