"""Source-extracted receipt projection regression; no native binaries required."""
import ast
import unittest
from pathlib import Path
from unittest import mock

SOURCE = Path(__file__).resolve().parents[1] / 'suite' / 'expanded.py'
source = SOURCE.read_text(encoding='utf-8')
tree = ast.parse(source, filename=str(SOURCE))
fn = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'tool_version_report')
namespace = {}
exec(compile(ast.Module(body=[fn], type_ignores=[]), str(SOURCE), 'exec'), namespace)
tool_version_report = namespace['tool_version_report']
Z = {'tool': 'z3', 'status': 'PASS', 'binary_sha256': 'a'*64, 'version_output': 'Z3 version 5.3.3'}
C = {'tool': 'cvc5', 'status': 'PASS', 'binary_sha256': 'b'*64, 'version_output': 'cvc5 version 1.4.2'}
T = {'tool': 'tlc', 'status': 'PASS', 'jar_sha256': 'c'*64, 'java_version_output': 'openjdk 21'}

class PostflightReceiptTests(unittest.TestCase):
    def test_both_verified(self):
        result = tool_version_report({'checks': [Z, C, T]}, {'checks': [Z, C, T]})
        self.assertEqual([result[k]['status'] for k in ('z3', 'cvc5', 'tlc_jar', 'java')],
                         ['VERIFIED', 'VERIFIED', 'VERIFIED', 'AVAILABLE_UNPINNED'])
    def test_post_failure_does_not_claim_verified(self):
        result = tool_version_report({'checks': [Z]}, {'checks': [{**Z, 'status': 'FAIL'}]})
        self.assertEqual(result['z3']['status'], 'REJECTED')
        self.assertIsNone(result['z3']['binary_sha256'])
    def test_post_hash_mismatch_rejected(self):
        result = tool_version_report({'checks': [Z]}, {'checks': [{**Z, 'binary_sha256': 'd'*64}]})
        self.assertEqual(result['z3']['status'], 'REJECTED')
    def test_post_missing_rejected(self):
        result = tool_version_report({'checks': [Z]}, {'checks': []})
        self.assertEqual(result['z3']['status'], 'REJECTED')
    def test_tlc_and_java_downgraded_together(self):
        result = tool_version_report({'checks': [T]}, {'checks': [{**T, 'status': 'FAIL'}]})
        self.assertEqual(result['tlc_jar']['status'], 'REJECTED')
        self.assertEqual(result['java']['status'], 'NOT_ATTESTED')
    def test_old_one_argument_signature(self):
        result = tool_version_report({'checks': [Z]})
        self.assertEqual(result['z3']['status'], 'VERIFIED')
        self.assertEqual(result['z3']['postflight_status'], 'NOT_PROVIDED')
    def test_no_native_subprocess(self):
        with mock.patch('subprocess.run', side_effect=AssertionError('untrusted tool')):
            result = tool_version_report({'checks': [Z, C, T]}, {'checks': [Z, C, T]})
        self.assertEqual(result['z3']['status'], 'VERIFIED')

if __name__ == '__main__':
    unittest.main()
