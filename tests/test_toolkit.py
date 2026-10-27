import contextlib,io,json,os,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
from document_toolkit.__main__ import ROOT,demo,inspect_sources

class DocumentToolkitTests(unittest.TestCase):
    def test_all_historical_python_programs_parse_and_are_indexed(self):
        rows=inspect_sources()
        self.assertEqual(len(rows),55)
        self.assertEqual(sum(x['syntax']=='Python syntax passed' for x in rows),50)

    def test_sensitive_archive_classes_cannot_execute_directly(self):
        paths=['career/fetch_ppt_references.py','scholarship/整理说明与索引/工具/organize.py','scholarship/国家奖学金申请表_填写版/04_按原格式去除修订并转DOCX.py']
        with tempfile.TemporaryDirectory() as td:
            for relative in paths:
                p=subprocess.run([sys.executable,str(ROOT/'archive'/relative)],cwd=td,env={**os.environ,'PYTHONPATH':str(ROOT)},capture_output=True)
                self.assertNotEqual(p.returncode,0)
                self.assertIn(b'disabled by default',p.stderr)
            self.assertEqual(list(Path(td).iterdir()),[])

    def test_full_preserved_resume_flow_generates_four_synthetic_docx(self):
        with tempfile.TemporaryDirectory() as td:
            output=Path(td)/'new-output'
            # The historical generator configures stdout; use its normal subprocess entry point.
            p=subprocess.run([sys.executable,'-m','document_toolkit','demo','--output',str(output)],cwd=ROOT,capture_output=True)
            self.assertEqual(p.returncode,0,p.stderr.decode(errors='replace'))
            result=json.loads((output/'demo-result.json').read_text(encoding='utf-8'))
            self.assertEqual(len(result['documents']),4)
            self.assertFalse(result['office_automation_run']);self.assertEqual(result['network_requests'],0)
            for item in result['documents']:
                path=output/'review/downloads'/item['name']
                with zipfile.ZipFile(path) as package:
                    xml=package.read('word/document.xml').decode('utf-8')
                    self.assertIn('[示例电话]',xml);self.assertIn('student@example.com',xml);self.assertNotIn('C:\\Users\\',xml)
            snapshot=(output/'demo-result.json').read_bytes()
            again=subprocess.run([sys.executable,'-m','document_toolkit','demo','--output',str(output)],cwd=ROOT,capture_output=True)
            self.assertEqual(again.returncode,2)
            self.assertEqual((output/'demo-result.json').read_bytes(),snapshot)

if __name__=='__main__':unittest.main()
